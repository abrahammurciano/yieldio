from typing import Any, Generator, Generic, TypeVar

T = TypeVar("T")


class PromiseState(Generic[T]):
    def __init__(self, generator: Generator[Any, Any, T]) -> None:
        self.gen = generator
        self.resolved = False
        self.result: T
