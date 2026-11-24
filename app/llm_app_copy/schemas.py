from dataclasses import dataclass, field
from pydantic import BaseModel, Field


@dataclass(frozen=True)
class TokenUsage:
    prompt_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    thoughts_tokens: int = 0


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    latency_ms: float
    usage: TokenUsage = field(default_factory=TokenUsage)
    request_id: str = ""


# Quản lí thứ tự các lượt chat, số lượng request và tổng token đã sử dụng trong một phiên chat
@dataclass
class ChatTurn:
    role: str
    text: str


@dataclass
class SessionState:
    history: list[ChatTurn] = field(default_factory=list)
    request_count: int = 0
    total_tokens: int = 0

    def clear(self) -> None:
        self.history.clear()
        self.request_count = 0
        self.total_tokens = 0


class UserInfo(BaseModel):
    name: str
    age: int
    skill: list[str]


class ArticleSummaryItem(BaseModel):
    article_id: str = Field(
        ...,
        description="Mã định danh chính xác của bài báo lấy từ thuộc tính id của thẻ <article> đầu vào.",
    )
    summary: str = Field(
        ...,
        description=(
            "Chỉ chứa nội dung văn bản tóm tắt (1 đoạn văn 3-4 câu, 90-120 từ), "
            "giữ nguyên từ khóa gốc, số liệu, tên riêng và trình tự sự kiện; "
            "không chứa tiêu đề, gạch đầu dòng hay lời giải thích."
        ),
    )


class BatchSummaryResponse(BaseModel):
    results: list[ArticleSummaryItem] = Field(
        ...,
        description="Danh sách kết quả tóm tắt độc lập cho từng bài báo trong lô đầu vào, giữ đúng thứ tự và đủ số lượng.",
    )