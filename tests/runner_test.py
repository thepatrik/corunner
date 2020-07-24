import asyncio

import corunner
from corunner import runner


def test_halt_and_catch_fire():
    group = corunner.Group()
    group._add_coro(_sleep_func)
    group._add_coro(_raise_err_func)

    caught_err = False
    try:
        runner.run(group, logger=None, halt_and_catch_fire=True)
    except BaseException:
        caught_err = True

    assert caught_err


async def _sleep_func():
    await asyncio.sleep(0.1)


async def _raise_err_func():
    raise ValueError('Whooops')
