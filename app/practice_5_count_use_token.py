from google import genai

from llm_app.config import load_setting

settings = load_setting()
prompt = "Giải thích context window trong 5 câu."

with genai.Client(api_key=settings.api_key) as client:
    count = client.models.count_tokens(
        model=settings.model_name,
        contents=prompt,
    )
    print("Input tokens dự kiến:", count.total_tokens)

    response = client.models.generate_content(
        model=settings.model_name,
        contents=prompt,
    )
    print("Usage sau request:", response.usage_metadata)
