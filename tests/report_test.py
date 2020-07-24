import time

from corunner.report import Execution, Report


def test_fastest():
    report = _get_report()

    assert report.fastest().latency == 100.0
    assert report.fastest(include_errored=True).latency == 1.0


def test_slowest():
    report = _get_report()

    assert report.slowest().latency == 100.0
    assert report.slowest(include_errored=True).latency == 100.0


def test_count():
    report = _get_report()

    assert report.count() == 1
    assert report.count(include_errored=True) == 2


def test_average():
    report = _get_report()

    assert report.average() == 100.0
    assert report.average(include_errored=True) == 50.5


def test_execution_ids():
    report = _get_report()
    ids = report.execution_ids()
    ids_with_err = report.execution_ids(include_errored=True)

    assert len(ids) == 1
    assert 'test1' in ids

    assert len(ids_with_err) == 2
    assert 'test1' in ids_with_err
    assert 'test2' in ids_with_err


def test_latencies():
    report = _get_report()

    assert report.latencies() == [100.0]
    assert report.latencies(include_errored=True) == [1.0, 100.0]


def test_latency_sum():
    report = _get_report()

    assert report.latency_sum() == 100.0
    assert report.latency_sum(include_errored=True) == 101.0


def test_execution_time():
    report = _get_report()

    assert report.execution_time() == 100.0
    assert report.execution_time(include_errored=True) == 101.0


def test_has_execution():
    report = _get_report()

    assert report.has_execution('test1')
    assert report.has_execution('test2') == False
    assert report.has_execution('test2', include_errored=True)
    assert report.has_execution('kalle', include_errored=False) == False


def test_child_report():
    report = _get_report()
    caught_err = False
    try:
        report.child_report('test3')
    except BaseException:
        caught_err = True

    assert report.child_report('test1')

    assert caught_err


def test_success_rate():
    assert _get_report().success_rate() == 0.5


def test_errors():
    assert len(_get_report().errors()) == 1


def _get_report():
    latency = 100.0
    ts = time.time() * 1000
    e1 = Execution('test1', ts, ts + latency, latency, None)

    ts = ts + latency
    latency = 1.0
    e2 = Execution('test2', ts, ts + latency, latency, ValueError('Nooo'))

    return Report([e1, e2])
