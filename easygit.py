#!/bin/python

from rich import traceback
from pynput import keyboard
import subprocess
from selection import Selection
import options
import rich
import time
import sys
import os
from pathlib import Path
from dataclasses import dataclass

rich.pretty.install()
traceback.install(show_locals=True)
console = rich.console.Console()
print = console.print
Key = keyboard.Key
proj_dir = os.getcwd()
config_path = Path(f'{proj_dir}/.git/easygit.yml')
run_st = subprocess.getstatusoutput
yes_or_no = Selection(
    [
        'yes',
        'no',
    ]
)


def git_init():
    check_git()
    check_remote()
    if not config_path.exists():
        run('git init')
        config_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        open(config_path, 'w').close()
        check_git()
        check_username()
        check_email()
        if run(
            'git config --global credential.helper'
        ) != 'store':
            run(
                'git config --global credential.helper store'
            )


def run(
    command: str
) -> str:
    return run_st(
        command
    )[-1]


def set_branch(
    *_,
    arg_pos,
    **__,
):
    Data.branch = sys.argv[arg_pos + 1]
    print(f'set branch "{Data.branch}"')


def set_remote(
    *_,
    arg_pos,
    **__,
):
    Data.remote = sys.argv[arg_pos + 1]
    print(f'set remote "{Data.remote}"')


def set_commit_message(
    *_,
    arg_pos,
    **__,
):
    Data.commit_message = sys.argv[arg_pos + 1]
    print(f'set commit_message "{Data.commit_message}"')


def check_username():
    if not run(
        'git config --global user.name'
    ):
        username = run('echo "$USER"')

        while True:
            print(
                f'use username "{username}" for git?'
            )

            if yes_or_no.choose() == 'yes':
                run(f'git config --global user.name {username}')
                print(f'[green]set git username [blue]"{username}"')
                break

            username = None
            while not username:
                print('[green]please input new username for git:')
                username = input()


def check_email():
    if not run(
        'git config --global user.email'
    ):
        text = '[green]please input new email for git:'
        while True:
            email = inp(text)
            print(
                f'use email "{email}" for git?'
            )
            if yes_or_no.choose() == 'yes':
                run(f'git config --global user.email {email}')
                print(f'[green]set git email [blue]"{email}"')
                break


def check_git():
    if run(
        'git -v'
    ).split()[0] != 'git':
        print('[red]git is not installed, please install it')
        exit()


def inp(
    text = None,
) -> str:
    output = None
    while not output:
        if text:
            print(text)
        output = input()
    return output


def add_remote(
    remote_name = None
):
    if not remote_name:
        remote_name = Data.remote
    text = (
'''
[bold green]\
Please create repo on one of this sites.
If your terminal supports links, use [blue1]ctrl+click[/blue1] to open link:
[/bold green]\
[deep_sky_blue1]
https://github.com
https://gitea.io
https://gogs.io
https://gitlab.com
https://codeberg.org
https://notabug.org
[bold green]
After creating repo input link here:\
'''
    )
    while True:
        url = inp(text)

        url = url.replace(
            'http://',
            'https://',
        )
        if 'https://' not in url:
            url = 'https://' + url

        print(
            f'use url "{url}" for git?'
        )

        if yes_or_no.choose() == 'yes':
            run(f'git remote add {remote_name} {url}')
            print('[green]your git remotes:')
            git_remotes = {}
            for remote in run(
                'git remote'
            ).split():
                git_remotes[remote] = run(
                    f'git remote get-url {remote}'
                )
            for key, val in git_remotes.items():
                print(f'{key}: {val}')
            break


def check_remote(
    remote_name = None
):
    if not remote_name:
        remote_name = Data.remote
    if run(
        f'git remote get-url {remote_name}'
    ).split()[0] == 'error:':
        add_remote(
            remote_name
        )


def check_gitignore():
    gitignore_path = Path(
        f"{proj_dir}/.gitignore"
    )
    if not gitignore_path.exists:
        with open(gitignore_path, 'w') as gitignore:
            gitignore.write(
'''\
__pycache__
test.*
'''
            )


@dataclass
class Data:
    branch = 'main'
    remote = 'origin'
    commit_message = 'aboba'
    options_list = [
        {
            'args': (
                '-h',
                '--help'
            ),
            'info':
                'show this message',
            'example':
                'easygit --help',
            'run':
                options.get_help,
            'skip_next': False
        },
        {
            'args': (
                '-b',
                '--branch'
            ),
            'info':
                'set branch for pushing',
            'example':
                'easygit --branch main',
            'run':
                set_branch,
            'skip_next': True
        },
        {
            'args': (
                '-r',
                '--remote'
            ),
            'info':
                'set remote for pushing',
            'example':
                'easygit --remote origin',
            'run':
                set_remote,
            'skip_next': True
        },
        {
            'args': (
                '-m',
                '--commit_message'
            ),
            'info':
                'set commit message',
            'example':
                'easygit --commit_message aboba',
            'run':
                set_commit_message,
            'skip_next': True
        },
    ]


def main():    
    options.parse(Data.options_list)
    git_init()
    os.system('git add --all')
    os.system(f'git commit -m "{Data.commit_message}"')



main()
