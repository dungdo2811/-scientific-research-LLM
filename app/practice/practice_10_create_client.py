from __future__ import annotations
from time import perf_counter
from uuid import uuid4

from google import genai
from google.genai import types

from llm_app.config import Settings
from llm_app.schemas import LLMResponse, TokenUsage
from llm_app.llm_client import LLMClientProtocol, LLMError

class GeminiLLMClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = genai.Client(api_key=settings.api_key)

    def close(self) -> None:
        self._client.close()

    def generate(self, prompt: str) -> LLMResponse:
        cleaned_prompt = prompt.strip()
        if not cleaned_prompt:
            raise ValueError("Prompt không được để trống.")

        request_id = str(uuid4())
        started = perf_counter()

        try:
            response = self._client.models.generate_content(
                model=self._settings.model_name,
                contents=cleaned_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "Bạn là trợ giảng LLM. Trả lời tiếng Việt, "
                        "rõ ràng và không tự tạo số liệu."
                    ),
                    temperature=0.3,
                    max_output_tokens=800,
                ),
            )
        except Exception as error:
            raise LLMError(
                f"Không thể gọi LLM API. request_id={request_id}"
            ) from error

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
