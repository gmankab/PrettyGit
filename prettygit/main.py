#!/bin/python

'''
very simple and user friendly interface for git

license - gnu gpl 3
https://gnu.org/licenses/gpl-3.0.en.html
'''

from rich import traceback
from pynput import keyboard
from easyselect import Selection
import shutil as sh
import subprocess
import rich
import yaml
import sys
import os
from pathlib import Path
from dataclasses import dataclass

rich.pretty.install()
traceback.install(show_locals=True)

from prettygit.setup import version, yes_or_no

c = rich.console.Console()
print = c.print
print(f'[bold][deep_sky_blue1]prettygit v[white]{version}')
Key = keyboard.Key
proj_path = os.getcwd()
config_path = Path(f'{proj_path}/.git/prettygit.yml')
run_st = subprocess.getstatusoutput


@dataclass
class Data:
    branch = None
    remote = 'origin'
    commit_message = 'aboba'
    git_path = None
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
                'prettygit --help',
        },
        {
            'args': (
                '-b',
                '--branch'
            ),
            'info':
                'set branch for pushing',
            'examples':
                'prettygit --branch main',
        },
        {
            'args': (
                '-r',
                '--remote'
            ),
            'info':
                'set remote for pushing',
            'examples':
                'prettygit --remote origin',
        },
        {
            'args': (
                '-m',
                '--message',
                '--commit_message'
            ),
            'info':
                'set commit message',
            'examples':
                'prettygit --commit_message aboba',
        },
        {
            'args': (
                '-g',
                '--git_path'
            ),
            'info':
                'permanently set new path for git',
            'examples': [
                'prettygit --git_path /bin/git',
                'prettygit --git_path D:\\\\git\\\\git.exe',
            ],
        },
    ]


def create_config():
    if config_path.exists():
        Data.config = yml_read_file(
            config_path
        )
        Data.git_path = Data.config['git_path']
    else:
        Data.config['branches'] = [
            'main',
            'beta',
        ]
        Data.git_path = 'git'
        Data.config['git_path'] = Data.git_path

        yml_save(
            data = Data.config,
            file_path = config_path,
        )
        git_init()


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
    with open(
        file_path,
        'r',
    ) as file:
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
    with open(
        file_path,
        'w'
    ) as file:
        file.write(
            to_yml_str(
                data,
            )
        )


def git_init():
    print(f'try init git in [blue]{proj_path}[/blue]?')
    if yes_or_no.choose() == 'no':
        sys.exit()
    check_gitignore()
    run(f'{Data.git_path} init')
    config_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
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
    selection = None
    while True:
        if run(
            f'{Data.git_path} --version'
        ).split()[0] == 'git':
            return
        else:
            if not selection:
                selection = Selection(
                    items = [
                        'try again',
                        'input path',
                        'exit'
                    ],
                    styles = [
                        'green',
                        'blue',
                        'red',
                    ],
                )
            if Data.git_path == 'git':
                print('[red]can\'t find git on this computer')
            else:
                print(f'[red]can\'t find git on this path - "{Data.git_path}"')
            answer = selection.choose()
            match answer:
                case 'exit':
                    exit()
                case 'input path':
                    print('[blue]please input path for git:')
                    Data.git_path = input()
                    Data.config['git_path'] = Data.git_path
                    yml_save(
                        data = Data.config,
                        file_path = config_path,
                    )


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
        f"{proj_path}/.gitignore"
    )
    if not gitignore_path.exists():
        with open(gitignore_path, 'w') as gitignore:
            gitignore.write(
'''\
__pycache__
test.*
dist
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
            'cancel',
        ]
        branches = Selection(
            branches_list
        )
        branches.styles[-3:] = (
            'green',
            'red',
            'bright_black',
        )
        print('\n[green]select branch:')
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
            case 'cancel':
                exit()
            case _:
                return branch


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
[light_slate_blue]    args:  [white]\
{' [bright_black]|[/bright_black] '.join(option['args'])}
[light_slate_blue]    info:  [purple]\
{option['info']}
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
    rule()
    print(f'[bold green] PrettyGit [bold blue]v{version}')


def parse_args(
    options_list,
):
    def check_arg(
        name,
        arg,
    ):
        if index >= len(sys.argv):
            print(
                f'[bold red]excepted {name} after [bold blue]{arg}[/bold blue] argument but nothing got'
            )
            exit()

    index = 1

    for arg in sys.argv[1:]:
        index += 1

        match arg:
            case 'h' | '-h' | 'help' | '--help':
                get_help(
                    options_list = Data.options_list
                )
                exit()

            case '-b' | '--branch':
                check_arg('branch name', arg)
                Data.branch = sys.argv[index]
                print(f'set branch "{Data.branch}"')

            case '-r' | '--remote':
                check_arg('remote name', arg)
                Data.remote = sys.argv[index]
                print(f'set remote "{Data.remote}"')

            case '-m' | '--message' | '--commit_message':
                check_arg('commit_message', arg)
                Data.commit_message = sys.argv[index]
                print(f'set commit_message "{Data.commit_message}"')

            case '-g' | '--git_path':
                check_arg('git path', arg)
                Data.git_path = sys.argv[index]
                Data.config['git_path'] = Data.git_path
                yml_save(
                    data = Data.config,
                    file_path = config_path,
                )
                print(f'permanently set git path "{Data.git_path}"')

            case _:
                pass


def pypi():
    if not Path(
        f'{proj_path}/pyproject.toml'
    ).exists():
        return
    print('do you want to upload package to pypi?')
    if yes_or_no.choose() == 'no':
        return
    dist_path = Path(f'{proj_path}/dist')
    print(f'remove [deep_sky_blue1]{dist_path}[/deep_sky_blue1]?')
    if yes_or_no.choose() == 'no':
        return
    sh.rmtree(
        dist_path,
        ignore_errors=True,
    )
    os.system(f'{sys.executable} -m hatchling build')
    os.system(f'{sys.executable} -m twine upload dist/*')


def main():
    parse_args(Data.options_list)
    create_config()
    check_git()
    check_remote()
    check_gitignore()
    if not Data.branch:
        Data.branch = select_branch()
    os.system(f'{Data.git_path} add --all')
    os.system(f'{Data.git_path} commit -m "{Data.commit_message}"')
    run(f'{Data.git_path} branch -m {Data.branch}')
    os.system(f'{Data.git_path} push --set-upstream {Data.remote} {Data.branch}')
    pypi()


main()
