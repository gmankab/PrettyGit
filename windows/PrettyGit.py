from urllib import request as r
from pathlib import Path
import subprocess
import shutil
import sys
import os



project_name = 'PrettyGit'
project_path = Path(__file__).parent.resolve()
portable = 'portable' in sys.argv
run_st = subprocess.getstatusoutput

if portable:
    sys.path.append(
        project_path
    )

try:
    import prettygit
    sys.exit()
except ImportError:
    def run(
        command: str
    ) -> str:
        return run_st(
            command
        )[-1]


    pip = f'{sys.executable} -m pip'
    upgrade_pip = run(f'{pip} install --upgrade pip')

    if 'No module named pip' in upgrade_pip:
        print('installing pip...')
        # pip is a shit which allow to install libs, so if we want to install libs we must have pip
        py_dir = Path(sys.executable).parent

        # fixing shit which doesn't allow to install pip in python embeddable in windows:
        for file in os.listdir(
            py_dir
        ):
            if file[-5:] == '._pth':
                with open(
                    f'{py_dir}/{file}', 'r+'
                ) as file:
                    if '#import site' in file.readlines()[-1]:
                        file.write('import site')

        # installing pip:
        get_pip = f'{project_path}/get-pip.py'

        r.urlretrieve(
            url = 'https://bootstrap.pypa.io/get-pip.py',
            filename = get_pip,
        )
        os.system(f'{sys.executable} {get_pip} --no-warn-script-location')
        os.remove(get_pip)
        os.remove(project_path)
    else:
        print(upgrade_pip)

    os.system(f'{pip} config set global.no-warn-script-location true')

    if portable:
        pip_cache = f'{project_path}/pip_cache'
        pip_cache_path = f'{project_path}/pip_cache'
        os.system(f'{pip} install {project_name} -t {project_path} --cache-dir {pip_cache}')
        shutil.rmtree(pip_cache)
    else:
        os.system(f'{pip} install {project_name}')

    os.system(
        " ".join(
            [
                sys.executable
            ] + sys.argv[1:]
        )
    )
