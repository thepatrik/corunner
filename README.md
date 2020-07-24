# corunner

![Build Status](https://github.com/thepatrik/corunner/workflows/corunner/badge.svg)

A simple runner for Python coroutines.

```python
import asyncio

import corunner

co_group = corunner.Group()


@co_group
async def f_1():
    await asyncio.sleep(0.1)


@co_group
async def f_2():
    await asyncio.sleep(0.2)


@co_group
async def f_3():
    await asyncio.sleep(0.5)


@co_group
async def f_4():
    raise ValueError('Whoops...')

report = corunner.run(co_group, duration=2, users=5) # runs for 2 seconds with 5 virtual users (default)
corunner.echo(report)
```

Running the above produces something like this:

```console
$ python main.py

Summary:
  Count:        16
  OK:           12 (75 %)
  Errored:      4
  Duration:     2.0 secs
  Slowest:      504 ms
  Fastest:      102 ms
  Average:      270
  Exec/sec:     5.96

Errors:
  ValueError: Whoops... (4)

Latency distribution: 
  10 in 104.915 ms
  25 in 105.135 ms
  50 in 203.378 ms
  75 in 503.264 ms
  90 in 503.901 ms

Histogram: 
  102.117 ms      [1]      | ∎∎∎∎∎∎∎∎∎∎
  112.162 ms      [3]      | ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
  202.563 ms      [1]      | ∎∎∎∎∎∎∎∎∎∎
  212.608 ms      [3]      | ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
  503.901 ms      [4]      | ∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎∎
```
