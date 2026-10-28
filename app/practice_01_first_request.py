from google import genai
from llm_app.config import load_setting
setting= load_setting()

def main() -> None:
    setting= load_setting()
    contents= (
                "hi"
            )
    while contents.strip():
        print("Nội dung yêu cầu không được để trống. Vui lòng nhập lại.")
        contents= input("Nhập nội dung yêu cầu: ")

    with genai.Client(api_key=setting.api_key) as client:
        response= client.models.generate_content(
            model=setting.model_name,
            contents=contents,
        )

    if not response.text:
        raise RuntimeError("Không nhận được phản hồi từ LLM.")

    print ("Phản hồi từ LLM:")
    print(response.text)


if __name__ == "__main__":
    main()
