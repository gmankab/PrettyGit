#!/bin/python

'''
very simple and user friendly interface for git

license - gnu gpl 3
https://gnu.org/licenses/gpl-3.0.en.html
'''

from rich import traceback
from pynput import keyboard
import subprocess
from prettygit.selection import Selection
import rich
import time
import yaml
import sys
import os
from pathlib import Path
from dataclasses import dataclass

rich.pretty.install()
traceback.install(show_locals=True)

from prettygit.setup import version

c = rich.console.Console()
print = c.print
Key = keyboard.Key
proj_dir = os.getcwd()
config_path = Path(f'{proj_dir}/.git/easygit.yml')
run_st = subprocess.getstatusoutput
yes_or_no = Selection(
    items = [
        'yes',
        'no',
    ],
    styles = [
        'green',
        'red'
    ]
)


def yml_read_str(
    data: str,
) -> any:
    return yaml.load(
        data,
        Loader = yaml.CLoader,
    )


def yml_read_file(
    file_path: str | Path
):
    with open(file_path, 'r') as file:
        return yml_read_str(
            file
        )


def to_yml_str(
    data: any,
) -> str:
    return yaml.dump(
        data,
        Dumper = yaml.CDumper,
    )


def yml_save(
    data: any,
    file_path: str | Path,
) -> None:
    with open(file_path, 'w') as file:
        file.write(
            to_yml_str(
                data,
            )
        )


def git_init():
    check_git()
    check_remote()
    if config_path.exists():
        Data.config = yml_read_file(
            config_path
        )
    else:
        print(f'try init git in [blue]{proj_dir}[/blue]?')
        if yes_or_no.choose() == 'no':
            sys.exit()
        check_gitignore()
        run(f'{Data.git_path} init')
        config_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        Data.config = {
            'branches': [
                'main',
            ],
        }
        yml_save(
            data = Data.config,
            file_path = config_path,
        )
        check_git()
        check_username()
        check_email()
        if run(
            f'{Data.git_path} config --global credential.helper'
        ) != 'store':
            run(
                f'{Data.git_path} config --global credential.helper store'
            )


def run(
    command: str
) -> str:
    return run_st(
        command
    )[-1]


def set_git_path(
    *_,
    arg_pos,
    **__,
):
    Data.git_path = sys.argv[arg_pos + 1]
    print(f'set git path "{Data.git_path}"')


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
        f'{Data.git_path} config --global user.name'
    ):
        username = run('echo "$USER"')

        while True:
            print(
                f'use username "{username}" for git?'
            )

            if yes_or_no.choose() == 'yes':
                run(f'{Data.git_path} config --global user.name {username}')
                print(f'[green]set git username [blue]"{username}"')
                break

            username = None
            while not username:
                print('[green]input new username for git:')
                username = input()


def check_email():
    if not run(
        f'{Data.git_path} config --global user.email'
    ):
        text = '[green]input new email for git:'
        while True:
            email = inp(text)
            print(
                f'use email "{email}" for git?'
            )
            if yes_or_no.choose() == 'yes':
                run(f'{Data.git_path} config --global user.email {email}')
                print(f'[green]set git email [blue]"{email}"')
                break


def check_git():
    if run(
        f'{Data.git_path} --version'
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
            f'use url [deep_sky_blue1]{url}[/deep_sky_blue1] for git?'
        )

        if yes_or_no.choose() == 'yes':
            run(f'{Data.git_path} remote add {remote_name} {url}')
            print('[green]your git remotes:')
            git_remotes = {}
            for remote in run(
                f'{Data.git_path} remote'
            ).split():
                git_remotes[remote] = run(
                    f'{Data.git_path} remote get-url {remote}'
                )
            for key, val in git_remotes.items():
                print(f'{key}: [deep_sky_blue1]{val}')
            print()
            break


def check_remote(
    remote_name = None
):
    if not remote_name:
        remote_name = Data.remote
    if run(
        f'{Data.git_path} remote get-url {remote_name}'
    ).split()[0] == 'error:':
        add_remote(
            remote_name
        )


def check_gitignore():
    gitignore_path = Path(
        f"{proj_dir}/.gitignore"
    )
    if not gitignore_path.exists():
        with open(gitignore_path, 'w') as gitignore:
            gitignore.write(
'''\
__pycache__
test.*
'''
            )


def delete_branch():
    while True:
        branches_list = Data.config[
            'branches'
        ] + [
            'cancel'
        ]
        branches = Selection(
            branches_list
        )
        branches.styles[-1] = 'green'
        print('[green]select branch to delete:')
        branch = branches.choose()
        if branch == 'cancel':
            return
        print(f'[green]do you really want to delete branch [red1]"{branch}"[/red1]?')
        if yes_or_no.choose() == 'yes':
            Data.config[
                'branches'
            ].remove(
                branch
            )
            yml_save(
                data = Data.config,
                file_path = config_path,
            )
            return


def select_branch():
    while True:
        branches_list = Data.config[
            'branches'
        ] + [
            'add new',
            'delete branch',
        ]
        branches = Selection(
            branches_list
        )
        branches.styles[-2:] = (
            'green',
            'red',
        )
        print('[green]select branch:')
        branch = branches.choose()
        match branch:
            case 'add new':
                branch_to_add = None
                while not branch_to_add:
                    print('[green]input new branch name:')
                    branch_to_add = input()
                Data.config['branches'].append(branch_to_add)
                yml_save(
                    data = Data.config,
                    file_path = config_path,
                )
            case 'delete branch':
                delete_branch()
            case _:
                return branch


@dataclass
class Data:
    branch = None
    remote = 'origin'
    commit_message = 'aboba'
    git_path = "git"
    config = {}
    options_list = [
        {
            'args': (
                '-h',
                '--help'
            ),
            'info':
                'show this message',
            'examples':
                'easygit --help',
        },
        {
            'args': (
                '-b',
                '--branch'
            ),
            'info':
                'set branch for pushing',
            'examples':
                'easygit --branch main',
        },
        {
            'args': (
                '-r',
                '--remote'
            ),
            'info':
                'set remote for pushing',
            'examples':
                'easygit --remote origin',
        },
        {
            'args': (
                '-m',
                '--commit_message'
            ),
            'info':
                'set commit message',
            'examples':
                'easygit --commit_message aboba',
        },
        {
            'args': (
                '-g',
                '--git_path'
            ),
            'info':
                'set path for git',
            'examples': [
                'easygit --git_path /bin/git',
                'easygit --git_path D:\\\\git\\\\git.exe',
            ],
        },
    ]


def get_help(
    *_,
    options_list,
    **__
):
    def rule():
        c.rule(
            '[bold blue]Help',
            style = 'green',
            characters = '━'
        )
    rule()
    table = rich.table.Table(
        show_header = False,
        show_edge = False,
        expand = True,
        border_style = 'blue',
    )
    table.add_column()

    for option in options_list:
        text = f'''\
[light_slate_blue]    args:  [white]{' [bright_black]|[/bright_black] '.join(option['args'])}
[light_slate_blue]    info:  [purple]{option['info']}
'''
        if isinstance(
            option['examples'],
            list
        ):
            text += '[light_slate_blue]examples:  [medium_purple2]'
            text += ("\n" + " " * 11).join(option['examples'])
        else:
            text += (
f'[light_slate_blue] example:  [medium_purple2]{option["examples"]}'
            )
        table.add_row(
            text,
            end_section = True,
        )
    print(table)
    print(f'[green] PrettyGit v{version}')
    rule()
    exit()


def parse_args(
    options_list,
):
    class BadArgumentError(Exception):
        pass

    index = 1
    for arg in sys.argv[1:]:
        index += 1

        match arg:
            case 'h' | '-h' | 'help' | '--help':
                get_help(
                    options_list = Data.options_list
                )
            case _:
                pass


def main():
    check_gitignore()
    parse_args(Data.options_list)
    git_init()
    os.system(f'{Data.git_path} add --all')
    os.system(f'{Data.git_path} commit -m "{Data.commit_message}"')
    if not Data.branch:
        Data.branch = select_branch()
    run(f'{Data.git_path} branch -m {Data.branch}')
    os.system(f'{Data.git_path} push --set-upstream {Data.remote} {Data.branch}')


main()
