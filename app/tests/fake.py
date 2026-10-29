from llm_app.schemas import LLMResponse, TokenUsage


class FakeLLMClient:
    def __init__(self, answer: str = "Câu trả lời mẫu") -> None:
        self.answer = answer
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> LLMResponse:
        self.prompts.append(prompt)
        return LLMResponse(
            text=self.answer,
            model="fake-model",
            latency_ms=1.0,
            usage=TokenUsage(
                prompt_tokens=5,
                output_tokens=4,
                total_tokens=9,
            ),
            request_id="test-request-id",
        )
