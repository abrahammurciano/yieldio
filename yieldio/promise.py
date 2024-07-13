from typing import Any, Generator, Generic, TypeVar, overload

from yieldio.promise_state import PromiseState

T = TypeVar("T")


class Promise(Generic[T]):
    @overload
    def __init__(self, generator: Generator[Any, Any, T], /) -> None: ...
    @overload
    def __init__(self, state: PromiseState[T], /) -> None: ...
    def __init__(self, arg: Generator[Any, Any, T] | PromiseState[T], /) -> None:
        self._state = arg if isinstance(arg, PromiseState) else PromiseState(arg)

    @property
    def result(self) -> T:
        assert self.resolved, "Promise hasn't been resolved yet"
        return self._state.result

    @property
    def resolved(self) -> bool:
        return self._state.resolved


class PromiseResolvedError(Exception):
    def __str__(self) -> str:
        return "Promise has already been resolved"
