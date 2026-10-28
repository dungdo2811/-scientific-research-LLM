from typing import Protocol

from llm_app.schemas import LLMResponse


class LLMError(RuntimeError):
    """Lỗi đã được chuẩn hóa ở tầng ứng dụng."""


class LLMClientProtocol(Protocol):
    def generate(self, prompt: str) -> LLMResponse:
        ...
