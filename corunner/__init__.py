from .group import Group  # noqa
from .report import Report
from .report_parser import str_parse
from .runner import run  # noqa


def echo(report: Report):
    report_str = str_parse(report)
    print(report_str)
