#!/bin/python

import rich
from rich import pretty
from rich.console import Console
from pynput import keyboard
import subprocess
import selection
import sys

pretty.install()
console = Console()
print = console.print
run = subprocess.getstatusoutput


def get_help(
    *_,
    options_list,
    **__
):
    console.rule(
        '[bold blue]Options',
        style = 'green',
        characters = '━'
    )
    table = rich.table.Table(
        show_header = False,
        show_edge = False,
        expand = True,
        border_style = 'blue',
    )
    table.add_column()

    for option in options_list:
        table.add_row(
f'''\
[light_slate_blue]   args:  [white]{'  '.join(option['args'])}
[light_slate_blue]   info:  [purple]{option['info']}
[light_slate_blue]example:  [medium_purple2]{option['example']}\
''',
            end_section = True
        )
    print(table)
    exit()


def parse(
    options_list,
    **kwargs
):
    class BadArgumentError(Exception):
        pass

    skip_next = False

    def check_arg(arg):
        for option in options_list:
            if arg in option['args']:
                option['run'](
                    arg_pos=index,
                    options_list=options_list,
                    **kwargs
                )
                nonlocal skip_next
                skip_next = option['skip_next']
                break

    for index, arg in enumerate(sys.argv):
        if index == 0:
            skip_next = False
            continue
        if skip_next:
            skip_next = False
            continue
        if len(arg) == 1:
            raise BadArgumentError(
                f'argument "{arg}" unexcepted'
            )
        elif arg[:2] == '--':
            check_arg(arg)
        elif arg[0] == '-':
            for char in arg:
                check_arg('-' + char)
        else:
            raise BadArgumentError(
                f'argument "{arg}" unexcepted'
            )
