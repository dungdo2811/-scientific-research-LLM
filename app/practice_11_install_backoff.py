import random
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def call_with_backoff(
    operation: Callable[[], T],
    is_transient: Callable[[Exception], bool],
    max_attempts: int = 4,
    base_delay: float = 1.0,
) -> T:
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except Exception as error:
            if attempt == max_attempts or not is_transient(error):
                raise

            delay = base_delay * (2 ** (attempt - 1))
            jitter = random.uniform(0, 0.25 * delay)
            time.sleep(delay + jitter)

    raise RuntimeError("Unreachable")
