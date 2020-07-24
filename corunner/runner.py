import asyncio
import contextlib
import inspect
import time
from typing import Any, Awaitable, Callable, List

import click_spinner

from .exceptions import CancelledError
from .report import Execution, Report


def run(*groups,
        users: int = 5,
        duration: int = 0,
        logger=None,
        show_progress_bar: bool = False,
        halt_and_catch_fire: bool = False) -> Report:
    cm = contextlib.nullcontext()
    if show_progress_bar and not logger:
        cm = click_spinner.spinner()
    with cm:
        started = time.time()
        executions = []
        if duration:
            while time.time() - started <= duration:
                res = _run(*groups, users=users, logger=logger,
                           halt_and_catch_fire=halt_and_catch_fire)
                executions.extend(res)
        else:
            res = _run(*groups, users=users, logger=logger,
                       halt_and_catch_fire=halt_and_catch_fire)
            executions.extend(res)

        return Report(executions)


def _run(
    *groups,
    users: int,
    logger,
        halt_and_catch_fire: bool) -> List[Execution]:
    asyncio_semaphore = asyncio.Semaphore(users)
    coros = []
    for c in [c for group in groups for c in group._coros]:
        i = 0
        while i < c.count:
            coros.append(_run_coro(c.id, c.f, asyncio_semaphore,
                                   halt_and_catch_fire, logger))
            i += 1

    async def runner(coros) -> Awaitable:
        return await asyncio.gather(*coros)

    return _run_until_complete(runner(coros))


def _run_until_complete(f: Awaitable[Any], close: bool = False):
    loop = asyncio.get_event_loop()
    try:
        return loop.run_until_complete(f)
    except KeyboardInterrupt:
        raise CancelledError()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        for task in asyncio.all_tasks(loop=loop):
            task.cancel()
        if close:
            loop.close()


async def _run_coro(id: str, f: Callable[..., Any], semaphore: asyncio.Semaphore,
                    halt_and_catch_fire: bool, callback, *args, **kw):
    async with semaphore:
        error = None
        ts = time.time()
        try:
            await f(*args, **kw)
        except Exception as e:
            error = e
        te = time.time()
        execution = Execution(id=id, error=error, start_time=ts * 1000,
                              end_time=te * 1000, latency=(te - ts) * 1000)
        if callback:
            if inspect.iscoroutinefunction(callback):
                await callback(execution)
            else:
                callback(execution)

        if error and halt_and_catch_fire:
            raise error

        return execution
