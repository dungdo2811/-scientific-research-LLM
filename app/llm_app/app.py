from llm_app.config import load_settings
from llm_app.llm_client import GeminiLLMClient, LLMError
from llm_app.logging_config import configure_logging
from llm_app.schemas import ChatTurn, SessionState


def main() -> None:
    configure_logging()
    settings = load_settings()
    llm = GeminiLLMClient(settings)
    session = SessionState()

    try:
        while True:
            print("=== LLM CHAT CLI ===")
            print("Lệnh: exit | clear | history | stats")
            user_input = input("Bạn: ").strip()

            if not user_input:
                print("Vui lòng nhập câu hỏi.")
                continue

            command = user_input.lower()
            if command in {"exit", "quit", "thoát"}:
                print("Đã kết thúc chương trình.")
                break

            if command == "clear":
                # llm.clear_history()
                session.clear()
                print("Đã xóa lịch sử chat và thống kê phiên.")
                continue

            if command == "history":
                if not session.history:
                    print("Lịch sử chat trống.")
                    continue

                for turn in session.history:
                    label = "Bạn" if turn.role == "user" else "AI"
                    print(f"{label}: {turn.text}")
                continue

            if command == "stats":
                print(
                    f"Số request: {session.request_count}; "
                    f"Tổng token: {session.total_tokens}"
                )
                continue

            try:
                result = llm.generate(user_input)
            except (ValueError, LLMError) as error:
                print(f"Lỗi: {error}")
                continue

            session.history.extend(
                [
                    ChatTurn(role="user", text=user_input),
                    ChatTurn(role="model", text=result.text),
                ]
            )
            session.request_count += 1
            session.total_tokens += result.usage.total_tokens

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
