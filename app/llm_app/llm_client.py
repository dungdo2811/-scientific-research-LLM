import random
import json 
from time import perf_counter, sleep
from typing import List, Protocol, Union
from uuid import uuid4
from collections.abc import Callable
from typing import TypeVar

from google import genai
from google.genai import types
from pytest import File
from google.api_core.exceptions import GoogleAPICallError

from llm_app.config import Settings
from llm_app.schemas import LLMResponse, UserInfo, Result_summary
from llm_app.schemas import TokenUsage


T = TypeVar("T")
class LLMError(RuntimeError):
    """Lỗi đã được chuẩn hóa ở tầng ứng dụng."""

# Fake client để đỡ tốn phí khi kiểm thử client.

with open("E:\\Siencentific_Research\\app\\llm_app\\system_instruction_summary.txt", "r", encoding="utf-8") as f:
    system_instruction_summary = f.read()
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
        operation: Callable[[],T],
        is_transient: Callable[[Exception], bool],
        max_attempts: int = 5,
        base_delay: float = 1.0
    ) ->  T:
        for attempt in range(1, max_attempts + 1):
            try:
                return operation()
            except Exception as error:
                if attempt == max_attempts or not is_transient(error):
                    raise
                
                delay= base_delay* (2**(attempt-1))
                jitter= random.uniform(0, 0.25*delay)
                sleep(delay + jitter)

    def generate_summary(self, content: Union[str, File]) -> LLMResponse:
        request_id = str(uuid4())
        started = perf_counter()

        if content is None:
            raise ValueError("File content không được None.")
        
        config = types.GenerateContentConfig(
            system_instruction=system_instruction_summary,
            temperature=0.3,
            max_output_tokens=400,
            response_mime_type="application/json",
            response_schema=Result_summary,
            )
        
        try:
            response = self._call_with_backoff(
                operation=lambda: self._client.models.generate_content(
                    model=self._settings.model_name,
                    contents=[content],
                    config=config,
                ),
                is_transient= lambda error: isinstance(error, Exception)
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


    def generate(self, contents: Union[str, List[Union[str, File]]]) -> LLMResponse:

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
                is_transient= lambda error: isinstance(error, Exception)
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