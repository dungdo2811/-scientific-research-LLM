from tests.fake import FakeLLMClient


def ask_once(client: FakeLLMClient, question: str) -> str:
    cleaned = question.strip()
    if not cleaned:
        raise ValueError("Câu hỏi không được để trống.")
    return client.generate(cleaned).text


def test_ask_once_returns_fake_answer() -> None:
    client = FakeLLMClient(answer="LLM là mô hình ngôn ngữ lớn.")

    answer = ask_once(client, "LLM là gì?")

    assert answer == "LLM là mô hình ngôn ngữ lớn."
    assert client.prompts == ["LLM là gì?"]


def test_ask_once_rejects_empty_question() -> None:
    client = FakeLLMClient()

    try:
        ask_once(client, "   ")
        assert False, "Phải phát sinh ValueError"
    except ValueError:
        assert client.prompts == []
