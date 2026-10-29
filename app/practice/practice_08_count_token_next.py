from google.genai import types
from openai import chat
from ..llm_app.llm_client import settings

next_message = types.UserContent(
    parts=[types.Part(text="Hãy tóm tắt cuộc trao đổi.")]
)
contents = [*chat.get_history(), next_message]

count = client.models.count_tokens(
    model=settings.model_name,
    contents=contents,
)
print("Token cho lượt tiếp theo:", count.total_tokens)