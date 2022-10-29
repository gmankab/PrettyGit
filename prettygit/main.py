#!/bin/python

'''
very simple and user friendly interface for git

license - gnu gpl 3
https://gnu.org/licenses/gpl-3.0.en.html
'''

from pathlib import Path
from easyselect import Sel
from rich import traceback
from betterdata import Data
from dataclasses import dataclass
from prettygit.setup import (
    version,
    yes_no,
    alw_yes_no,
)
import shutil as sh
import subprocess
import rich
import sys
import os


rich.pretty.install()
traceback.install(show_locals=True)


c = rich.console.Console()
print = c.print
print(
    f'[bold][deep_sky_blue1]prettygit [white]{version}'
)
proj_path = os.getcwd()
config_path = Path(
    f'{proj_path}/.git/prettygit.yml'
)
config = Data(
    file_path=config_path
)
temp_data = Data()
run_st = subprocess.getstatusoutput


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


def check_config():
    if not config['inited_git']:
        act = yes_no.choose(
            f'try init git in [blue]{proj_path}[/]?'
        )
        match act:
            case 'yes':
                pass
            case 'no' | 'exit':
                sys.exit()
    temp_data['git_init'] = True
    if not temp_data['commit_message']:
        temp_data['commit_message'] = 'aboba'
    if not config['remote']:
        config['remote'] = 'origin'
    if not config['branches']:
        config['branches'] = [
            'main',
            'beta',
        ]
    if not config['git_path']:
        config['git_path'] = 'git'


def git_init():
    if not temp_data['git_init']:
        return
    run(f'{config.git_path} init')
    check_gitignore()
    check_username()
    check_email()
    check_remote()
    check_gitignore()
    check_branch()
    if run(
        f'{config.git_path} config --global credential.helper'
    ) != 'store':
        run(
            f'{config.git_path} config --global credential.helper store'
        )
    config['inited_git'] = True


def run(
    command: str
) -> str:
    return run_st(
        command
    )[-1]


def check_username():
    username = run(
        f'{config.git_path} config --global user.name'
    )
    if not username:
        username = run('echo "$USER"')
        while True:
            act = yes_no.choose(
                f'use username "{username}" for git?'
            )
            match act:
                case 'yes':
                    run(
                        f'{config.git_path} config --global user.name {username}'
                    )
                    print(
                        f'[green]set git username [blue]"{username}"'
                    )
                    break
                case 'no':
                    username = inp(
                        '[green]input new username for git:'
                    )
                    continue
                case 'exit':
                    sys.exit()


def check_email():
    if not run(
        f'{config.git_path} config --global user.email'
    ):
        text = '[green]input new email for git:'
        while True:
            email = inp(text)
            act = yes_no.choose(
                f'use email "{email}" for git?'
            )
            match act:
                case 'yes':
                    run(f'{config.git_path} config --global user.email {email}')
                    print(f'[green]set git email [blue]"{email}"')
                    break
                case 'no':
                    continue
                case 'exit':
                    sys.exit()


def check_git():
    actions = None
    while True:
        git_ver = run(
            f'{config.git_path} --version'
        )
        if git_ver.split()[0] == 'git':
            return
        else:
            if not actions:
                actions = Sel(
                    items=[
                        'try again',
                        'input path',
                        'exit'
                    ],
                    styles=[
                        'green',
                        'blue',
                        'red',
                    ],
                )
            action = actions.choose(
                f'[red]can\'t find git on this path - "{config.git_path}"'
            )
            match action:
                case 'exit':
                    sys.exit()
                case 'input path':
                    config['git_path'] = inp(
                        '[blue]please input path for git:'
                    )
                case 'try again':
                    continue


def inp(
    text=None,
) -> str:
    output = None
    while not output:
        if text:
            print(text)
        output = input()
    return output


def check_remote():
    if run(
        f'{config.git_path} remote get-url {config["remote"]}'
    ).split()[0] != 'error:':
        return

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

        act = yes_no.choose(
            f'use url [deep_sky_blue1]{url}[/deep_sky_blue1] for git?'
        )
        match act:
            case 'yes':
                pass
            case 'no':
                continue
            case 'exit':
                sys.exit()

        run(f'{config.git_path} remote add {config.remote} {url}')
        print('[green]your git remotes:')
        git_remotes = {}
        for remote in run(
            f'{config.git_path} remote'
        ).split():
            git_remotes[remote] = run(
                f'{config.git_path} remote get-url {remote}'
            )
        for key, val in git_remotes.items():
            print(f'{key}: [deep_sky_blue1]{val}')
        print()
        break


def check_gitignore():
    gitignore_path = Path(
        f"{proj_path}/.gitignore"
    )
    if not gitignore_path.exists():
        gitignore_path.parent.mkdir(
            exist_ok = True,
            parents = True,
        )
        with open(
            gitignore_path,
            'w'
        ) as gitignore:
            gitignore.write(
                '''\
__pycache__
*config*
*.txt
*.yml
*.log
test*
dist
'''
            )


def delete_branch():
    while True:
        branches_list = config[
            'branches'
        ] + [
            'exit',
            'cancel',
        ]
        branches = Sel(
            branches_list
        )
        branches.styles[-2:] = [
            'bright_black',
            'green',
        ]
        branch = branches.choose(
            '[green]select branch to delete:'
        )

        match branch:
            case 'cancel':
                return
            case 'exit':
                sys.exit()
            case _:
                pass
        act = yes_no.choose(
            f'[red]do you really want to delete branch [blue]"{branch}"[/blue]?'
        )
        match act:
            case 'yes':
                pass
            case 'no':
                continue
            case 'exit':
                sys.exit()
        config[
            'branches'
        ].remove(
            branch
        )
        config.to_file()
        return


def check_branch() -> None:
    if temp_data['branch']:
        return
    while True:
        branches_list = config[
            'branches'
        ] + [
            'add new',
            'delete branch',
            'exit',
        ]
        branches = Sel(
            branches_list
        )
        branches.styles[-3:] = (
            'green',
            'red',
            'bright_black',
        )
        branch = branches.choose(
            '[green]select branch for pushing:'
        )
        match branch:
            case 'add new':
                branch_to_add = inp(
                    '[green]input new branch name:'
                )
                config['branches'].append(
                    branch_to_add
                )
                config.to_file()
            case 'delete branch':
                delete_branch()
            case 'exit':
                sys.exit()
            case _:
                temp_data['branch'] = branch
                return


def get_help(
    *_,
    local_options_list,
    **__
):
    def rule():
        c.rule(
            '[bold blue]Help',
            style='green',
            characters='━'
        )
    rule()
    table = rich.table.Table(
        show_header=False,
        show_edge=False,
        expand=True,
        border_style=None,
    )
    table.add_column()

    for option in local_options_list:
        text = f'''\
[light_slate_blue]    args:  [bold deep_sky_blue1]\
{' [bright_black]|[/bright_black] '.join(option['args'])}
[/bold deep_sky_blue1][light_slate_blue]    info:  [medium_purple2]\
{option['info']}
'''
        if isinstance(
            option['examples'],
            list
        ):
            text += '[light_slate_blue]examples:  [purple]'
            text += ("\n" + " " * 11).join(option['examples'])
        else:
            text += (
                f'[light_slate_blue] example:  [purple]{option["examples"]}'
            )
        table.add_row(
            text,
            end_section=True,
        )
    print(table)
    rule()


def parse_args(
    local_options_list
):
    def get_arg(
        name,
    ) -> str:
        nonlocal arg_index
        nonlocal arg
        if arg_index >= len(sys.argv):
            print(
                f'[bold red]excepted {name} after [bold blue]{arg}[/bold blue] argument but nothing got'
            )
            sys.exit()
        return sys.argv[arg_index]

    arg_index = 1
    skip_next = False

    for arg in sys.argv[1:]:
        arg_index += 1
        if skip_next:
            skip_next = False
            continue

        match arg:
            case 'h' | '-h' | 'help' | '--help':
                get_help(local_options_list=local_options_list)
                sys.exit()
            case '-b' | '--branch':
                temp_data['branch'] = get_arg('branch name')
                skip_next = True
                if temp_data['branch'] not in config['branches']:
                    config['branches'].append(temp_data['branch'])
                print(f'[green]set branch [blue]"{temp_data.branch}"')
            case '-r' | '--remote':
                skip_next = True
                config['remote'] = get_arg('remote name')
                print(f'[green]permanently set remote [blue]"{config.remote}"')
            case '-m' | '--message' | '--commit_message':
                skip_next = True
                temp_data.commit_message = get_arg('commit_message')
                print(
                    f'[green]set commit_message [blue]"{temp_data.commit_message}"')
            case '-g' | '--git_path':
                skip_next = True
                config['git_path'] = get_arg('git path')
                print(
                    f'[green]permanently set git path [blue]"{config.git_path}"')
            case _:
                print(f'[bold red]wrong argument [blue]{arg}')
                sys.exit()


def pypi():
    if not Path(
        f'{proj_path}/pyproject.toml'
    ).exists():
        return
    act = yes_no.choose(
        '\n[green]do you want to upload package to pypi?'
    )
    match act:
        case 'yes':
            pass
        case 'no':
            return
        case 'exit':
            sys.exit()

    pypirc_path = Path(
        f'{Path.home()}/.pypirc'
    )
    if not pypirc_path.exists():
        while True:
            token = inp('input your pypi token:')
            if token[:5] == 'pypi-':
                pypirc_path.parent.mkdir(
                    exist_ok = True,
                    parents = True,
                )
                with open(
                    pypirc_path,
                    'w'
                ) as pypirc:
                    pypirc.write(
                        f'''\
[pypi]
  username = __token__
  password = {token}
'''
                    )
                break
            else:
                act = yes_no.choose(
                    '[bold red]token must start with [blue]pypi-\n'
                    '[green]input again?'
                )
                match act:
                    case 'yes':
                        continue
                    case 'no' | 'exit':
                        sys.exit()

    dist_path = Path(f'{proj_path}/dist')
    if dist_path.exists():
        if not config['always_delete']:
            act = alw_yes_no.choose(
                f'[red]remove [deep_sky_blue1]{dist_path}[/deep_sky_blue1] ?'
            )
            match act:
                case 'yes':
                    pass
                case 'always yes':
                    config['always_delete'] = True
                case 'no':
                    return
                case 'exit':
                    sys.exit()
        sh.rmtree(
            dist_path,
            ignore_errors=True,
        )
    os.system(f'{sys.executable} -m hatchling build')
    os.system(f'{sys.executable} -m twine upload dist/*')


def main():
    parse_args(options_list)
    check_config()
    check_git()
    git_init()
    print(f'selected branch {temp_data.branch}')
    os.system(f'{config.git_path} add --all')
    os.system(f'{config.git_path} commit -m "{temp_data.commit_message}"')
    run(f'{config.git_path} branch -m {temp_data.branch}')
    os.system(
        f'{config.git_path} push --set-upstream {config.remote} {temp_data.branch}'
    )
    pypi()


main()
