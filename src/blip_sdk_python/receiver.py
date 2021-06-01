from typing import Any, Callable


class Receiver:
    """Receiver base class."""

    def __init__(
        self,
        predicate: Callable[[Any], bool],
        callback: Callable[[Any], None]
    ) -> None:
        self.predicate: Callable[[Any], bool] = predicate
        self.callback: Callable[[Any], None] = callback
