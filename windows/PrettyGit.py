from urllib import request as r
from pathlib import Path
import subprocess
import shutil
import sys
import os

proj_name = 'PrettyGit'
proj_path = Path(__file__).parent.resolve()
run_st = subprocess.getstatusoutput
portable = 'portable' in sys.argv


if portable:
    if str(proj_path) not in sys.path:
        sys.path.append(
            str(proj_path)
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

    downloading_progress = 0
    def progress(
        block_num,
        block_size,
        total_size,
    ):
        global downloading_progress
        new_progress = round(
            block_num * block_size / total_size * 100
        )
        if new_progress != downloading_progress:
            downloading_progress = new_progress
            print(
                f'\r{new_progress}%',
                end = '',
            )

    pip = f'{sys.executable} -m pip'
    if portable:
        pip_cache_path = f'{proj_path}/pip_cache'
        upgrade_pip = run(f'{pip} install --upgrade pip --cache-dir {pip_cache_path}')
    else:
        upgrade_pip = run(f'{pip} install --upgrade pip')

    if 'No module named pip' in upgrade_pip:
        print('downloading pip')
        # pip is a shit which allow to install libs, so if we want to install libs we must have pip
        py_dir = Path(sys.executable).parent

        # fixing shit which doesn't allow to install pip in python embeddable on windows:
        for file in os.listdir(
            py_dir
        ):
            if file[-5:] == '._pth':
                with open(
                    f'{py_dir}/{file}', 'r+'
                ) as file:
                    if '#import site' in file.readlines()[-1]:
                        file.write('import site')

        # downloading pip
        get_pip = f'{proj_path}/get-pip.py'
        get_pip_tmp = f'{proj_path}/get-pip.tmp'
        r.urlretrieve(
            url = 'https://bootstrap.pypa.io/get-pip.py',
            filename = get_pip_tmp,
            reporthook = progress,
        )
        print()
        Path(get_pip_tmp).rename(get_pip)

        print('Preparing to install pip')
        if portable:
            os.system(
                f'{sys.executable} {get_pip} --no-warn-script-location --cache-dir {pip_cache_path}'
            )
        else:
            os.system(
                f'{sys.executable} {get_pip} --no-warn-script-location'
            )
        os.remove(get_pip)
        print('succesfully installed pip')
    else:
        print(upgrade_pip)

    os.system(f'{pip} config set global.no-warn-script-location true')

    if portable:
        os.system(f'{pip} install {proj_name} -t {proj_path} --cache-dir {pip_cache_path}')
        shutil.rmtree(
            pip_cache_path,
            ignore_errors=True
        )
    else:
        os.system(f'{pip} install {proj_name}')

    command = f'{sys.executable} {Path(__file__)}'
    if portable:
        command += ' portable'
    os.system(
        command
    )
