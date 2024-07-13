from typing import Any, Generator, Generic, MutableMapping, TypeVar

from typed_data_structures import Queue, Stack

from yieldio.promise import Promise
from yieldio.promise_state import PromiseState

T = TypeVar("T")
U = TypeVar("U")


class Loop(Generic[T]):
    def __init__(self) -> None:
        self._queue: Queue[Stack[PromiseState[Any]]] = Queue()
        self._to_send: MutableMapping[Stack[Any], Any] = {}

    def run(self, generator: Generator[Any, Any, T]) -> T:
        main = self._add_generator(generator)
        while self._queue:
            stack = self._queue.pop()
            self._advance(stack)
            if stack:
                self._queue.push(stack)
        return main.result

    def schedule(self, generator: Generator[Any, Any, U]) -> Promise[U]:
        return Promise(self._add_generator(generator))

    def _add_generator(self, gen: Generator[Any, Any, U]) -> PromiseState[U]:
        state = PromiseState(gen)
        self._queue.push(Stack((state,)))
        return state

    def _advance(self, stack: Stack[PromiseState[Any]]) -> None:
        state = stack.pop()
        try:
            yielded = state.gen.send(self._to_send.pop(stack, None))
        except StopIteration as e:
            self._on_return(stack, state, e.value)
        else:
            self._on_yield(stack, state, yielded)

    def _on_yield(
        self, stack: Stack[PromiseState[Any]], state: PromiseState[Any], value: Any
    ) -> None:
        stack.push(state)
        if isinstance(value, Generator):
            stack.push(PromiseState(value))
        elif value is not None:
            raise NotAGeneratorError(value)

    def _on_return(
        self, stack: Stack[PromiseState[Any]], state: PromiseState[Any], value: Any
    ) -> None:
        self._to_send[stack] = value
        state.result = value
        state.resolved = True


class NotAGeneratorError(Exception):
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"Value yielded from yieldio generator must be a generator or None: Got {self.value!r} of type {type(self.value).__name__}"
