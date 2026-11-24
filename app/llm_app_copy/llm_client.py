import random
import json
from time import perf_counter, sleep
from typing import List, Protocol, Union, TypeVar
from uuid import uuid4
from collections.abc import Callable

from google import genai
from google.genai import types

from llm_app_copy.config import Settings
from llm_app_copy.schemas import LLMResponse, UserInfo, BatchSummaryResponse, TokenUsage


T = TypeVar("T")


class LLMError(RuntimeError):
    """Lỗi đã được chuẩn hóa ở tầng ứng dụng."""


with open(
    r"E:\Siencentific_Research\app\llm_app\system_instruction_summary.txt",
    "r",
    encoding="utf-8",
) as f:
    system_instruction_summary = f.read()

ONE_SHOT_EXAMPLE = """### VÍ DỤ MẪU (ONE-SHOT):
Đầu vào:
<article id="mau/vd_01.txt">
Sáng 15/10, Bộ Giao thông Vận tải phối hợp với UBND tỉnh Đồng Nai tổ chức lễ khởi công dự án thành phần 1A thuộc tuyến đường Vành đai 3 TP HCM. Dự án có tổng chiều dài 8,22 km, điểm đầu giao với đường tỉnh 25B tại huyện Nhơn Trạch và điểm cuối giao với cao tốc TP HCM - Long Thành - Dầu Giây tại TP Thủ Đức. Tổng mức đầu tư của dự án hơn 6.955 tỷ đồng từ nguồn vốn vay ODA của Chính phủ Hàn Quốc và vốn đối ứng trong nước. Theo kế hoạch, công trình sẽ hoàn thành vào tháng 9/2025, góp phần rút ngắn thời gian di chuyển từ Đồng Nai sang TP HCM và giảm ùn tắc cho cao tốc hiện hữu.
</article>

Đầu ra JSON chuẩn:
{
  "results": [
    {
      "article_id": "mau/vd_01.txt",
      "summary": "Sáng 15/10, Bộ Giao thông Vận tải và UBND tỉnh Đồng Nai khởi công dự án thành phần 1A thuộc tuyến đường Vành đai 3 TP HCM. Tuyến đường dài 8,22 km, nối từ đường tỉnh 25B tại huyện Nhơn Trạch đến cao tốc TP HCM - Long Thành - Dầu Giây tại TP Thủ Đức. Dự án có tổng mức đầu tư hơn 6.955 tỷ đồng từ vốn vay ODA của Chính phủ Hàn Quốc và vốn đối ứng trong nước. Công trình dự kiến hoàn thành vào tháng 9/2025 nhằm rút ngắn thời gian di chuyển từ Đồng Nai sang TP HCM và giảm ùn tắc giao thông."
    }
  ]
}
### HẾT VÍ DỤ MẪU. BẮT ĐẦU XỬ LÝ DỮ LIỆU THẬT DƯỚI ĐÂY:
"""


class LLMClientProtocol(Protocol):
    def generate(self, prompt: str) -> LLMResponse:
        ...


class GeminiLLMClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = genai.Client(api_key=settings.api_key)
        self._config = types.GenerateContentConfig(
            system_instruction=(
                "Bạn là trợ giảng LLM. Trả lời tiếng Việt, "
                "rõ ràng và không tự tạo số liệu."
            ),
            temperature=0.3,
            max_output_tokens=800,
            response_mime_type="application/json",
            response_schema=UserInfo,
        )

    def _create_chat(self):
        return self._client.chats.create(
            model=self._settings.model_name,
            config=self._config,
        )

    def clear_history(self):
        self._client_chats = self._create_chat()

    def close(self) -> None:
        self._client.close()

    def _call_with_backoff(
        self,
        operation: Callable[[], T],
        is_transient: Callable[[Exception], bool],
        max_attempts: int = 5,
        base_delay: float = 1.0,
    ) -> T:
        for attempt in range(1, max_attempts + 1):
            try:
                return operation()
            except Exception as error:
                if attempt == max_attempts or not is_transient(error):
                    raise

                delay = base_delay * (2 ** (attempt - 1))
                jitter = random.uniform(0, 0.25 * delay)
                sleep(delay + jitter)

    def generate_summary(self, articles: List[dict[str, str]]) -> LLMResponse:
        """
        Nhận danh sách n bài báo dạng [{"id": "the-thao/bai_1.txt", "content": "..."}]
        và trả về LLMResponse chứa chuỗi JSON đã xác thực theo BatchSummaryResponse.
        """
        request_id = str(uuid4())
        started = perf_counter()

        if not articles:
            raise ValueError("Danh sách bài báo đầu vào không được rỗng.")

        blocks = [
            f'<article id="{item["id"]}">\n{item["content"].strip()}\n</article>'
            for item in articles
        ]
        prompt = ONE_SHOT_EXAMPLE + "\n\n".join(blocks)

        config = types.GenerateContentConfig(
            system_instruction=system_instruction_summary,
            temperature=0.15,
            max_output_tokens=max(1500, len(articles) * 500),
            response_mime_type="application/json",
            response_schema=BatchSummaryResponse,
        )

        def _invoke_and_validate():
            resp = self._client.models.generate_content(
                model=self._settings.model_name,
                contents=[prompt],
                config=config,
            )
            raw_text = (resp.text or "").strip()
            if not raw_text:
                raise ValueError("Mô hình trả về chuỗi rỗng.")
            # Ép kiểm tra schema ngay tại đây để tự động retry nếu JSON bị lỗi/cắt cụt
            BatchSummaryResponse.model_validate_json(raw_text)
            return resp

        try:
            response = self._call_with_backoff(
                operation=_invoke_and_validate,
                is_transient=lambda error: isinstance(error, Exception),
            )
        except Exception as error:
            raise LLMError(f"Không thể gọi LLM API. request_id={request_id}") from error

        latency_ms = (perf_counter() - started) * 1000
        text = (response.text or "").strip()

        metadata = response.usage_metadata
        usage = TokenUsage(
            prompt_tokens=int(
                getattr(metadata, "prompt_token_count", 0) or 0
            ),
            output_tokens=int(
                getattr(metadata, "candidates_token_count", 0) or 0
            ),
            total_tokens=int(
                getattr(metadata, "total_token_count", 0) or 0
            ),
            thoughts_tokens=int(
                getattr(metadata, "thoughts_token_count", 0) or 0
            ),
        )

        return LLMResponse(
            text=text,
            model=self._settings.model_name,
            latency_ms=latency_ms,
            usage=usage,
            request_id=request_id,
        )

    def generate(self, contents: Union[str, List[Union[str, types.File]]]) -> LLMResponse:
        request_id = str(uuid4())
        started = perf_counter()

        try:
            response = self._call_with_backoff(
                operation=lambda: self._client.models.generate_content(
                    model=self._settings.model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=(
                            "Bạn là trợ giảng LLM. Trả lời tiếng Việt, "
                            "rõ ràng và không tự tạo số liệu."
                        ),
                        temperature=0.3,
                        max_output_tokens=800,
                    ),
                ),
                is_transient=lambda error: isinstance(error, Exception),
            )
        except Exception as error:
            raise LLMError(f"Không thể gọi LLM API. request_id={request_id}") from error

        latency_ms = (perf_counter() - started) * 1000
        text = (response.text or "").strip()
        if not text:
            raise LLMError(
                f"Mô hình không trả text. request_id={request_id}"
            )

        metadata = response.usage_metadata
        usage = TokenUsage(
            prompt_tokens=int(
                getattr(metadata, "prompt_token_count", 0) or 0
            ),
            output_tokens=int(
                getattr(metadata, "candidates_token_count", 0) or 0
            ),
            total_tokens=int(
                getattr(metadata, "total_token_count", 0) or 0
            ),
            thoughts_tokens=int(
                getattr(metadata, "thoughts_token_count", 0) or 0
            ),
        )

        return LLMResponse(
            text=text,
            model=self._settings.model_name,
            latency_ms=latency_ms,
            usage=usage,
            request_id=request_id,
        )