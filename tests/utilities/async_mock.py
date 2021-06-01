from asyncio import Future
from typing import Any, Awaitable


def async_return(result: Any) -> Awaitable[Any]:
    """Create an async return.

    Args:
        result (Any): the mock result

    Returns:
        Any: the async result response
    """
    fut = Future()
    fut.set_result(result)
    return fut
