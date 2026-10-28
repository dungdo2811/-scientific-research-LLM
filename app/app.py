from google import genai
from google.genai import types
from llm_app.config import load_settings

settings = load_settings()
config = types.GenerateContentConfig(
    system_instruction=(
        "Bạn là trợ giảng LLM. Hãy nhớ thông tin người học "
        "đã cung cấp trong phiên hiện tại."
    ),
    temperature=0.3,
)
with genai.Client(api_key=settings.api_key) as client:
    chat = client.chats.create(
        model=settings.model_name,
        config=config,
    )

    first = chat.send_message(
        "Tôi đang xây dựng một hệ thống RAG cho giáo trình."
    )
    print("AI:", first.text)

    second = chat.send_message(
        "Hệ thống tôi đang xây dựng dùng để làm gì?"
    )
    print("AI:", second.text)

    for message in chat.get_history():
        print("Role:", message.role)
        for part in message.parts or []:
            print("Text:", getattr(part, "text", None))
    # print("Số message trong history:", len(chat.get_history()))
