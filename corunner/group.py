import inspect
from dataclasses import dataclass
from typing import Any, Callable, List

from . import stats


@dataclass(frozen=True)
class Coro:
    id: str
    f: Callable[..., Any]
    count: int


class Group:

    def __init__(self):
        self._coros: List[Coro] = []

    def __call__(self, *args):
        self._add_coro(args[0])

    def _add_coro(self, func: Callable[..., Any],
                  id: str = '', iterations: int = 1):
        if not inspect.iscoroutinefunction(func):
            raise ValueError(
                'a coroutine was expected, got {!r}'.format(func))

        f = Coro(id or func.__name__, func, iterations)
        self._coros.append(f)

    def add(self, id: str = '', iterations: int = 1) -> Callable[..., Any]:

        def decorator(func: Callable[..., Any]):
            self._add_coro(func, id=id, iterations=iterations)

        return decorator
