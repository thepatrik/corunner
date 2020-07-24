from .group import Group
from .report import Report
from .report_parser import str_parse
from .runner import run


def echo(report: Report):
    report_str = str_parse(report)
    print(report_str)
