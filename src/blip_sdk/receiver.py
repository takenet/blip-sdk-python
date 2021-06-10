from typing import Callable
from uuid import uuid4

from lime_python import Envelope


class Receiver:
    """Receiver base class."""

    def __init__(
        self,
        predicate: Callable[[Envelope], bool],
        callback: Callable[[Envelope], None]
    ) -> None:
        self.predicate: Callable[[Envelope], bool] = predicate
        self.callback: Callable[[Envelope], None] = callback
        self.id = str(uuid4())

    def __eq__(self, other: object) -> bool:  # noqa: D105
        if isinstance(other, Receiver):
            return self.id == other.id
        return False

    def __hash__(self) -> int:  # noqa: D105
        return hash(self.id)

    @property
    def predicate(self) -> Callable[[Envelope], bool]:  # noqa: D102
        return self.__predicate

    @predicate.setter
    def predicate(self, value: Callable[[Envelope], bool]) -> None:
        if not isinstance(value, Callable):
            self.__predicate = lambda _: value in [True, None]  # noqa: WPS510
            return
        self.__predicate = value
