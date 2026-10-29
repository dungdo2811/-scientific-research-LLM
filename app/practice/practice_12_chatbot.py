from dataclasses import dataclass, field

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

