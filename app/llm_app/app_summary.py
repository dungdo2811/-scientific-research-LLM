from llm_app.config import load_settings
from llm_app.llm_client import GeminiLLMClient, LLMError
from llm_app.logging_config import configure_logging
from llm_app.schemas import ChatTurn, SessionState
import os 
import json


def main() -> None:
    configure_logging()
    settings = load_settings()
    llm = GeminiLLMClient(settings)
    session = SessionState()

    os.chdir("E:/Siencentific_Research/vnexpress-2026-11-04_07-04-30")
    content_news= []
    for type_news in os.listdir():
        for news in os.listdir(type_news):
            path_news= os.path.join(type_news,news)
            with open(path_news, "r", encoding="utf-8") as f:
                content_news.append( f.read())

    try:

        for i in range (2) :
            content = content_news[i]
            try:
                result = llm.generate_summary(content)
            except (ValueError, LLMError) as error:
                print(f"Lỗi: {error}")
            print (result.text)

            session.history.extend(
                [
                    ChatTurn(role="user", text=content),
                    ChatTurn(role="model", text=result.text),
                ]
            )
            print(f"AI: {result.text}")
            print(
                f"(Mô hình: {result.model} | "
                f"Thời gian: {result.latency_ms / 1000:.2f} giây | "
                f"Token: {result.usage.total_tokens})")

    finally:
        llm.close()


if __name__ == "__main__":
    main()
