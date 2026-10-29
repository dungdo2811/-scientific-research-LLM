from google import genai
from google.genai import types

from llm_app.config import load_settings
from llm_app.schemas import LLMResponse, TokenUsage
from llm_app.schemas import ChatTurn


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


class ChatSession:
    def __init__(
        self,
        client: genai.Client,
        model: str,
        config: types.GenerateContentConfig,
    ) -> None:
        self._client = client
        self._model = model
        self._config = config
        self.history: list[ChatTurn] = []
        self._chat = self._client.chats.create(
            model=self._model,
            config=self._config,
        )

    def send_message(self, user_message: str) -> str:
        cleaned_message = user_message.strip()
        if not cleaned_message:
            raise ValueError("Tin nhắn không được để trống.")

        response = self._chat.send_message(cleaned_message)
        answer = (response.text or "").strip()
        if not answer:
            raise ValueError("Mô hình không trả về nội dung text.")

        self.history.extend(
            [
                ChatTurn(role="user", text=cleaned_message),
                ChatTurn(role="model", text=answer),
            ]
        )
        return answer

    def clear(self) -> None:
        self._chat = self._client.chats.create(
            model=self._model,
            config=self._config,
        )
        self.history.clear()

    def print_history(self) -> None:
        if not self.history:
            print("Lịch sử chat trống.")
            return

        for turn in self.history:
            label = "Bạn" if turn.role == "user" else "AI"
            print(f"{label}: {turn.text}")


def main() -> None:
    settings = load_settings()
    config = types.GenerateContentConfig(
        system_instruction="Bạn là trợ giảng LLM. Hãy trả lời bằng tiếng Việt.",
        temperature=0.3,
    )

    with genai.Client(api_key=settings.api_key) as client:
        session = ChatSession(
            client=client,
            model=settings.model_name,
            config=config,
        )

        print("Lệnh: exit | clear | history")
        while True:
            user_message = input("Bạn: ").strip()
            command = user_message.lower()

            if command in {"exit", "quit", "thoát"}:
                break
            if command == "clear":
                session.clear()
                print("Đã xóa lịch sử chat.")
                continue
            if command == "history":
                session.print_history()
                continue
            if not user_message:
                print("Vui lòng nhập tin nhắn.")
                continue

            answer = session.send_message(user_message)
            print(f"AI: {answer}")


if __name__ == "__main__":
    main()
