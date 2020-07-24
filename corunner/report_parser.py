from colorama import Fore, Style

from . import stats
from .report import Report


def str_parse(report: Report,
              show_colors: bool = True,
              show_summary: bool = True,
              show_errors: bool = True,
              show_distribution: bool = True,
              show_histogram: bool = True) -> str:
    include_errored = False

    report_str = ''
    if show_summary:
        count = report.count(include_errored=True)
        ok = report.count(include_errored=False)
        success_rate = round(report.success_rate() * 100)
        success_rate_str = f'{success_rate} %'
        if show_colors:
            success_rate_str = f'{_color(success_rate==100)}{success_rate_str}{Style.RESET_ALL}'

        execution_time_str = ''
        execution_time = report.execution_time(include_errored=include_errored)
        if execution_time:
            execution_time_str = f'{round(execution_time/1000, 1)} secs'

        slowest_str = ''
        slowest = report.slowest(include_errored=include_errored)
        if slowest:
            slowest_str = f'{round(slowest.latency)} ms'

        fastest_str = ''
        fastest = report.fastest(include_errored=include_errored)
        if fastest:
            fastest_str = f'{round(fastest.latency)} ms'

        avg_str = ''
        avg = report.average(include_errored=include_errored)
        if avg:
            avg_str = f'{round(avg)}'

        eps_str = ''
        eps = report.eps(include_errored=include_errored)
        if eps:
            eps_str = f'{round(eps, 2)}'

        report_str += f'''
Summary:
  Count:        {count}
  OK:           {ok} ({success_rate_str})
  Errored:      {count-ok}
  Duration:     {execution_time_str or '-'}
  Slowest:      {slowest_str or '-'}
  Fastest:      {fastest_str or '-'}
  Average:      {avg_str or '-'}
  Exec/sec:     {eps_str or '-'}'''

    if show_errors and count - ok != 0:
        if len(report_str) > 0:
            report_str += '\n'
        errors = ''
        for error in report.errors():
            errors += f'\n  {error[0]} ({error[1]})'
        report_str += f'''
Errors:{errors}'''

    if show_distribution:
        if len(report_str) > 0:
            report_str += '\n'
        distributions = ''
        for dist in report.distributions(include_errored=include_errored):
            if dist.percentile > 0 and dist.latency > 0:
                distributions += f'\n  {dist.percentile} in {round(dist.latency, 3)} ms'

        report_str += f'''
Latency distribution: {distributions or '-'}'''

    if show_histogram:
        if len(report_str) > 0:
            report_str += '\n'

        histogram = report.histogram(include_errored=include_errored)
        histogram_str = ''
        if histogram:
            histogram_str = stats.histogram_str(histogram)
        report_str += f'''
Histogram: {histogram_str or '-'}'''

    return report_str


def _color(cond: bool):
    if cond:
        return Fore.GREEN
    return Fore.RED
