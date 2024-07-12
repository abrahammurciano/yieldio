from collections import deque
from typing import Any, Generator, Generic, TypeVar

from yieldio.promise import Promise

T = TypeVar("T")
U = TypeVar("U")


class Loop(Generic[T]):
    def __init__(self, generator: Generator[Any, Any, T]) -> None:
        self._main = Promise(generator)
        self._queue: deque[Promise[Any]] = deque()
        self._queue.append(self._main)

    def run(self) -> T:
        while self._queue:
            promise = self._queue.popleft()
            promise.resume()
            if promise.resolved:
                if promise.awaited_by:
                    self._queue.append(promise.awaited_by)
            else:
                self._queue.append(
                    promise.waiting_for if promise.waiting_for else promise
                )
        return self._main.result

    def schedule(self, generator: Generator[Any, Any, U]) -> Promise[U]:
        promise = Promise(generator)
        self._queue.append(promise)
        return promise
