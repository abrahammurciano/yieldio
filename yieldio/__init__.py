from typing import Any, Generator, Iterable, TypeVar

from yieldio.loop import Loop
from yieldio.promise import Promise

T = TypeVar("T")


_loop: Loop[Any] | None = None


def loop() -> Loop[Any]:
    if _loop is None:
        raise LoopNotRunningError
    return _loop


def run(generator: Generator[Any, Any, T]) -> T:
    global _loop
    assert _loop is None, "Loop is already running"
    _loop = Loop()
    result = _loop.run(generator)
    _loop = None
    return result


def gather(
    generators: Iterable[Generator[Any, Any, Any]]
) -> Generator[Any, Any, tuple[Any, ...]]:
    l = loop()
    promises = tuple(l.schedule(gen) for gen in generators)
    while not all(p.resolved for p in promises):
        yield
    return tuple(p.result for p in promises)


def schedule(generator: Generator[Any, Any, T]) -> Promise[T]:
    return loop().schedule(generator)


class LoopNotRunningError(Exception):
    def __str__(self) -> str:
        return "No loop is currently running"
