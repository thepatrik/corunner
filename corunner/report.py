from collections import Counter
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple

from . import stats


@dataclass(frozen=True)
class Execution:
    id: str
    start_time: float
    end_time: float
    latency: float
    error: Optional[Exception]


class Report:

    def __init__(self, executions: List[Execution]):
        if not executions or len(executions) == 0:
            raise ValueError('missing executions')
        self._executions = executions

    def count(self, include_errored: bool = False) -> int:
        return len(self.executions(include_errored=include_errored))

    def executions(
            self,
            execution_id: str = '',
            reverse: bool = False,
            include_errored: bool = False) -> List[Execution]:
        executions = self._executions
        if execution_id:
            executions = [
                e for e in executions if e.id == execution_id]
        if not include_errored:
            executions = [
                e for e in executions if not e.error]
        return sorted(executions, key=lambda x: x.latency, reverse=reverse)

    def child_report(self, execution_id: str) -> 'Report':
        if not self.has_execution(execution_id, include_errored=True):
            raise ValueError('could not find: ' + execution_id)
        return Report(
            self.executions(
                execution_id=execution_id,
                include_errored=True))

    def child_reports(self, include_errored: bool = False) -> List['Report']:
        reports = []
        for id in self.execution_ids(include_errored):
            report = Report(
                self.executions(
                    execution_id=id,
                    include_errored=include_errored))
            reports.append(report)

        return reports

    def errors(self) -> List[Tuple[str, int]]:
        errors = [
            f'{type(e.error).__name__}: {str(e.error)}' for e in self.executions(
                include_errored=True) if e.error]
        err_count = []
        counter = Counter(errors)
        for c in Counter(errors):
            err_count.append((c, counter[c]))

        return err_count

    def has_execution(
            self,
            execution_id: str,
            include_errored: bool = False) -> bool:
        return execution_id in self.execution_ids(include_errored)

    def execution_ids(self, include_errored: bool = False) -> Set[str]:
        return set([e.id for e in self.executions(
            include_errored=include_errored)])

    def average(self, include_errored: bool = False) -> Optional[float]:
        count = self.count(include_errored)
        if count > 0:
            return self.latency_sum(
                include_errored=include_errored) / count
        return None

    def fastest(self, include_errored: bool = False) -> Optional[Execution]:
        executions = self.executions(include_errored=include_errored)
        if len(executions) > 0:
            return executions[0]
        return None

    def slowest(self, include_errored: bool = False) -> Optional[Execution]:
        executions = self.executions(
            reverse=True,
            include_errored=include_errored)
        if len(executions) > 0:
            return executions[0]
        return None

    def success_rate(self) -> float:
        return self.count() / self.count(include_errored=True)

    def latencies(self, include_errored: bool = False) -> List[float]:
        return [
            e.latency for e in self.executions(
                include_errored=include_errored)]

    def latency_sum(self, include_errored: bool = False) -> float:
        return sum(
            e.latency for e in self.executions(
                include_errored=include_errored))

    def eps(self, include_errored: bool = False) -> Optional[float]:
        count = self.count(include_errored=include_errored)
        time = self.execution_time(include_errored=include_errored)
        if time and count > 0:
            return count / (time / 1000)
        return None

    def distributions(
            self, include_errored: bool = False) -> List[stats.Distribution]:
        return stats.distributions(
            self.latencies(
                include_errored=include_errored))

    def histogram(
            self, include_errored: bool = False) -> Optional[List[stats.Bucket]]:
        count = self.count(include_errored=include_errored)
        if count > 0:
            return stats.histogram(
                self.latencies(
                    include_errored=include_errored))
        return None

    def execution_time(self, include_errored: bool = False) -> Optional[float]:
        executions = self.executions(include_errored=include_errored)
        if len(executions) > 0:
            start_time = min(e.start_time for e in executions)
            end_time = max(e.end_time for e in executions)
            return end_time - start_time
        return None
