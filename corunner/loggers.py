from colorama import Fore, Style

from .report import Execution


def extensive(e: Execution):
    if e.error:
        print(
            f'{Fore.RED}{"☓"} {e.id:<20} {type(e.error).__name__}: {e.error}{Style.RESET_ALL}',
            flush=True)
    else:
        print(f'{"√"} {e.id:<20} {round(e.latency)} ms',
              flush=True)


def simple(e: Execution):
    char = Fore.RED + 'F' + Style.RESET_ALL if e.error else '.'
    print(char, end='', flush=True)


def silent():
    pass
