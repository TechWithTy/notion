"""Decorators for enhancing Notion API client functionality."""

import asyncio
import logging
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any

from app.core.integrations.notion.exceptions import (
    NotionRateLimitError,
    NotionServiceUnavailableError,
)

# * Configure logging
logger = logging.getLogger(__name__)


def retry(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
) -> Callable[..., Callable[..., Coroutine[Any, Any, Any]]]:
    """
    A decorator to retry an async function with exponential backoff.

    Args:
        max_retries: The maximum number of retries.
        initial_delay: The initial delay between retries in seconds.
        backoff_factor: The factor by which the delay increases each retry.

    Returns:
        A decorated coroutine function.
    """

    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = initial_delay
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except (
                    NotionRateLimitError,
                    NotionServiceUnavailableError,
                    asyncio.TimeoutError,
                ) as e:
                    if attempt == max_retries:
                        logger.error(
                            "Function %s failed after %d retries.",
                            func.__name__,
                            max_retries,
                        )
                        raise e

                    logger.warning(
                        "Attempt %d/%d failed for %s. Retrying in %.2f seconds...",
                        attempt + 1,
                        max_retries,
                        func.__name__,
                        delay,
                    )
                    await asyncio.sleep(delay)
                    delay *= backoff_factor

        return wrapper

    return decorator
