from pathlib import Path
import platform
import selection
import shutil as sh

project_path = Path(__file__).parent.resolve()
icon_ico_source = f'{project_path}/icon.ico'


def main():
    print(platform.system())
    if 'linux' in platform.system().lower():
        linux()
    elif 'windows' in platform.system().lower():
        windows()


def linux():
    home = Path.home()
    share = f'{home}/.local/share'

    dotdesktop_path = Path(f'{home}/.local/share/applications/PrettyGit.desktop')
    if not dotdesktop_path.exists():
        dotdesktop_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        sh.copy(
            f'{project_path}/PrettyGit.desktop',
            f'{home}/.local/share/applications/PrettyGit.desktop',
        )

    icon_path = Path(f'{share}/icons/PrettyGit.svg')
    if not icon_path.exists():
        icon_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        sh.copy(
            f'{project_path}/icon.svg',
            f'{share}/icons/PrettyGit.svg',
        )


def windows():
    print('got windows')


main()
