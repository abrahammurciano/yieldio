import sys
import time
from random import randint
from typing import Any, Generator

import yieldio


def sleep(seconds: int) -> Generator[Any, Any, None]:
    end = time.time() + seconds
    while time.time() < end:
        yield


def random_number() -> Generator[Any, Any, int]:
    yield sleep(randint(1, 5))
    return randint(1, 100)


def worker(name: str, iterations: int) -> Generator[Any, Any, int]:
    print(f"{name} is starting")
    total = 0
    for _ in range(iterations):
        num = yield random_number()
        total += num
        print(f"{name} got {num}")
    print(f"{name} is done with a total of {total}")
    return total


def main() -> Generator[Any, Any, None]:
    workers = (worker(name, randint(3, 8)) for name in sys.argv[1:])
    totals = yield yieldio.gather(workers)
    print(totals)


if __name__ == "__main__":
    yieldio.run(main())
