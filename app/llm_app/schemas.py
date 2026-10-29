from dataclasses import dataclass, field


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
