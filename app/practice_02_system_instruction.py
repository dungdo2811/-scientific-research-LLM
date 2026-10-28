from google import genai
from streamlit import form
from google.genai import types

from llm_app.config import load_settings

settings= load_settings()

def get_text_or_raise(response: object) -> str:
    text = getattr(response, "text", None)
    if not text or not text.strip():
        raise RuntimeError(
            "Không nhận được câu trả lời văn bản từ mô hình."
        )
    return text.strip()

config= types.GenerateContentConfig(
    system_instruction= (
        "Bạn là trợ giảng về LLM. Trả lời bằng tiếng Việt, "
        "giải thích dễ hiểu, có một ví dụ và tối đa 150 từ. "
        "Nếu không chắc, hãy nói rõ giới hạn."
    ),
    temperature= 0.3,
    max_output_tokens= 500,
)

with genai.Client(api_key= settings.api_key) as client :
    response = client.models.generate_content(
        model= settings.model_name,
        contents= "Phân biệt mô hình llm và ứng dụng chat bot",
        config= config,
    )
print(response.text)