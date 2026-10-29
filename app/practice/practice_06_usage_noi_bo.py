from dataclasses import dataclass


@dataclass(frozen=True)
class TokenUsage:
    prompt_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    thoughts_tokens: int = 0


def parse_usage(metadata: object | None) -> TokenUsage:
    if metadata is None:
        return TokenUsage()

    return TokenUsage(
        prompt_tokens=int(
            getattr(metadata, "prompt_token_count", 0) or 0
        ),
        output_tokens=int(
            getattr(metadata, "candidates_token_count", 0) or 0
        ),
        total_tokens=int(
            getattr(metadata, "total_token_count", 0) or 0
        ),
        thoughts_tokens=int(
            getattr(metadata, "thoughts_token_count", 0) or 0
        ),
    )
