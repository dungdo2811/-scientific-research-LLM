from llm_app.config import load_settings
from llm_app.llm_client import GeminiLLMClient, LLMError
from llm_app.logging_config import configure_logging


def main() -> None:
    configure_logging()
    settings = load_settings()
    llm = GeminiLLMClient(settings)

    print("=== LLM CHAT CLI ===")
    print("Lệnh: exit | clear | history | stats")

    try:
        while True:
            user_input = input("Bạn: ").strip()

            if not user_input:
                print("Vui lòng nhập câu hỏi.")
                continue

            command = user_input.lower()
            if command in {"exit", "quit", "thoát"}:
                print("Đã kết thúc chương trình.")
                break

            # Phiên bản tối giản: các lệnh session sẽ được bổ sung
            # trong bài thực hành 5.12.
            try:
                result = llm.generate(user_input)
            except (ValueError, LLMError) as error:
                print(f"Lỗi: {error}")
                continue

            print(f"AI: {result.text}")
            print(
                f"[model={result.model}; "
                f"latency={result.latency_ms:.0f} ms; "
                f"tokens={result.usage.total_tokens}]"
            )
    finally:
        llm.close()


if __name__ == "__main__":
    main()
