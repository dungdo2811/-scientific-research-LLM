from ast import List
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

#Quản lí thứ tự các lượt chat, số lượng request và tổng token đã sử dụng trong một phiên chat

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

@dataclass
class UserInfo(BaseModel):
    name: str
    age: int
    skill: list[str]

@dataclass
class Result_summary(BaseModel):
    title: str  = Field(description="Tiêu đề chính thức của bài báo")
    published_date: str = Field(description="Ngày xuất bản bài báo, định dạng YYYY-MM-DD")
    author: str = Field(description="Tên tác giả của bài báo")
    category: str = Field(description="Chủ đề chính của bài báo")
    summary: str =  Field(
        description=(
            "Bản tóm tắt súc tích nội dung cốt lõi của bài báo, độ dài khoảng"
            " 3-5 câu."
        )
    )
    key_points: list[str] = Field(
        description=(
            "Danh sách các ý chính, số liệu nổi bật hoặc sự kiện quan trọng rút"
            " ra từ bài báo."
        )
    ) 
    sentiment: str  = Field(
        description=(
            "Sắc thái bài báo. Mặc định là neutral nếu bài viết đưa tin khách"
            " quan, chỉ chọn positive hoặc negative khi có biểu hiện cảm xúc"
            " rõ rệt."
        )
    )