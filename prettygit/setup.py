from rich import traceback
from pathlib import Path
from easyselect import Sel
import shutil as sh
import platform
import rich
import sys
import os


version = '22.0.13'
proj_path = Path(__file__).parent.resolve()
icon_ico_source = f'{proj_path}/icon.ico'
c = rich.console.Console()
print = c.print
portable = 'portable' in sys.argv
yes_no = Sel(
    items=[
        'yes',
        'no',
        'exit',
    ],
    styles=[
        'green',
        'red',
        'bright_black',
    ]
)
alw_yes_no = Sel(
    items=[
        'yes',
        'always yes',
        'no',
        'exit',
    ],
    styles=[
        'green',
        'green',
        'red',
        'bright_black',
    ]
)


def main():
    if platform.system() == 'Linux':
        linux()
    elif platform.system() == 'Windows':
        windows()


def linux():
    home = Path.home()
    share = f'{home}/.local/share'

    dotdesktop_path = Path(
        f'{home}/.local/share/applications/PrettyGit.desktop')
    if dotdesktop_path.exists():
        return
    dotdesktop_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )
    with open(
        dotdesktop_path,
        'w',
    ) as dotdesktop:
        dotdesktop.write(
            '''\
[Desktop Entry]
Comment=very simple and user friendly interface for git
Type=Application
Icon=PrettyGit
Name=PrettyGit
Terminal=true
TerminalOptions=\\s--noclose
Hidden=false
Keywords=pretty;git
Exec=/bin/python -m prettygit
'''
        )

    icon_path = Path(f'{share}/icons/PrettyGit.svg')
    icon_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )
    sh.copy(
        f'{proj_path}/icon.svg',
        f'{share}/icons/PrettyGit.svg',
    )

    act = yes_no.choose(
        f'''
[green]\
Created file [deep_sky_blue1]{dotdesktop_path}

[green]\
This script can be runned with following command:
[deep_sky_blue1]\
python -m prettygit
[/deep_sky_blue1]\
Do you want do create shortcuts in \
[deep_sky_blue1]/bin[/deep_sky_blue1]?
Then you will be able to run this script with [deep_sky_blue1]prettygit[/deep_sky_blue1] and [deep_sky_blue1]pg[/deep_sky_blue1] commands
Creating this shortcuts requires sudo\
'''
    )
    match act:
        case 'yes':
            pass
        case 'no':
            return
        case 'exit':
            sys.exit()
    script = '''\
#!/bin/bash
python -m prettygit
'''
    os.system(
        f'''
echo "{script}" | sudo tee /bin/pg /bin/prettygit
sudo chmod +x /bin/prettygit
sudo chmod +x /bin/pg
'''
    )


def windows():
    shortcut = Path(
        f'{proj_path.parent.resolve()}/{proj_path.name}.lnk'
    )

    if shortcut.exists():
        return

    icon = Path(
        f'{Path(__file__).parent.resolve()}/icon.ico'
    )

    home = os.environ["USERPROFILE"]

    desktop = Path(
        f'{home}/desktop/{shortcut.name}'
    )

    start_menu = Path(
        f"{home}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/gmanka/{shortcut.name}"
    )

    start_menu.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shortcut_creator_path = f'{proj_path}/shortcut_creator.vbs'

    with open(
        shortcut_creator_path,
        'w'
    ) as shortcut_creator:
        shortcut_creator.write(
            f'''\
set WshShell = WScript.CreateObject("WScript.Shell")
set Shortcut = WshShell.CreateShortcut("{shortcut}")
Shortcut.TargetPath = "{sys.executable}"
Shortcut.Arguments = "{proj_path} {'portable' if portable else ""}"
Shortcut.IconLocation = "{icon}"
Shortcut.Save
'''
        )
    shortcut_creator.close()
    os.system(shortcut_creator_path)
    os.remove(shortcut_creator_path)
    sh.copyfile(shortcut, desktop,)
    sh.copyfile(shortcut, start_menu)
    text = f'''
[green]\
Created shortcuts on desktop and start panel

This script can be runned with following commands:
[deep_sky_blue1]\
{sys.executable} {proj_path}
{shortcut}
{desktop}
'''
    if not portable:
        text += f'{sys.executable} -m prettygit\n'
    print(
        text,
        highlight=False,
    )


main()
