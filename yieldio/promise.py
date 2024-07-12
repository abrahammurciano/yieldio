from __future__ import annotations

from typing import Any, Generator, Generic, TypeVar, cast, overload

T = TypeVar("T")


class Promise(Generic[T]):
    @overload
    def __init__(self: Promise[None], generator: None = None) -> None: ...
    @overload
    def __init__(self, generator: Generator[Any, Any, T]) -> None: ...
    def __init__(self, generator: Generator[Any, Any, T] | None = None) -> None:
        self._gen = generator
        self._resolved = False
        self._result: T | None = None
        self._waiting_for: Promise[Any] | None = None
        self._awaited_by: Promise[Any] | None = None

    def resume(self) -> None:
        if self.resolved:
            raise PromiseResolvedError
        if not self._can_resume:
            return
        to_send = self._waiting_for.result if self._waiting_for else None
        try:
            if self._gen:
                self._waiting_for = Promise(self._gen.send(to_send))
                self._waiting_for._awaited_by = self
            else:
                cast(Promise[None], self)._resolve(None)
        except StopIteration as e:
            self._resolve(e.value)

    @property
    def result(self) -> T:
        assert self.resolved, "Promise hasn't been resolved yet"
        return cast(T, self._result)

    @property
    def resolved(self) -> bool:
        return self._resolved

    @property
    def awaited_by(self) -> Promise[Any] | None:
        return self._awaited_by

    @property
    def waiting_for(self) -> Promise[Any] | None:
        return self._waiting_for

    def _resolve(self, result: T) -> None:
        self._resolved = True
        self._result = result

    @property
    def _can_resume(self) -> bool:
        return not self._waiting_for or self._waiting_for.resolved


class PromiseResolvedError(Exception):
    def __str__(self) -> str:
        return "Promise has already been resolved"
