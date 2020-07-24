import time

from corunner.report import Execution, Report
from corunner.report_parser import str_parse


def test_execution_time():
    report = _get_err_report()

    assert str_parse(report)


def _get_err_report():
    latency = 100.0
    ts = time.time() * 1000
    latency = 1.0
    e = Execution('test2', ts, ts + latency, latency, ValueError('Nooo'))

    return Report([e])
