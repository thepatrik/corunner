from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Distribution:
    percentile: int = 0
    latency: float = 0.0


def distributions(
    latencies: List[float],
    percentiles: List[int] = [
        10,
        25,
        50,
        75,
        90,
        95,
        99]) -> List[Distribution]:
    latencies.sort()
    data = [0.0] * len(percentiles)
    i, j = 0, 0
    while i < len(latencies) and j < len(percentiles):
        current = i * 100 / len(latencies)

        if current >= percentiles[j]:
            data[j] = latencies[i]
            j += 1
        i += 1

    dists = [Distribution(percentile) for percentile in percentiles]
    i = 0
    while i < len(percentiles):
        if data[i] > 0:
            lat = data[i]
            dists[i] = Distribution(percentiles[i], lat)
        i += 1
    return dists


@dataclass(frozen=True)
class Bucket:
    mark: float = 0.0
    count: int = 0
    frequency: float = 0.0


def histogram(latencies: List[float], resolution=40) -> List[Bucket]:
    latencies.sort()
    fastest = latencies[0]
    slowest = latencies[len(latencies) - 1]

    bc = resolution
    buckets = [0.0] * (bc + 1)
    counts = [0] * (bc + 1)
    bs = (slowest - fastest) / bc

    i = 0
    while i < bc:
        buckets[i] = fastest + (bs * i)
        i += 1

    buckets[bc] = slowest
    bi = 0
    max = 0
    i = 0
    while i < len(latencies):
        if latencies[i] <= buckets[bi]:
            i += 1
            counts[bi] += 1
            if max < counts[bi]:
                max = counts[bi]
        elif bi < len(buckets) - 1:
            bi += 1

    res = [Bucket()] * len(buckets)
    latencyCount = len(latencies)
    i = 0
    if latencyCount > 0:
        while i < len(buckets):
            res[i] = Bucket(buckets[i], counts[i], counts[i] / latencyCount)
            i += 1

    return res


def histogram_str(
        buckets: List[Bucket],
        resolution=40,
        bar_char: str = '∎') -> str:
    max = 0

    for b in buckets:
        if b.count > max:
            max = b.count

    histo_str = ''
    for b in buckets:
        # Normalize bar lengths.
        bar_len = 0
        if max > 0:
            bar_len = int((b.count * resolution + max / 2) / max)

        if b.count > 0:
            str_count = f'[{b.count}]'
            latency = str(round(b.mark, 3)) + ' ms'
            histo_str += f'\n  {latency:<15} {str_count:<8} | {bar_char*bar_len}'

    return histo_str
