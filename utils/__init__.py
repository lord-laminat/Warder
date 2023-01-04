import yadisk
import os
import datetime
import time

def mkdir(disk: yadisk.YaDisk, full_path: str) -> None:
    path = 'disk:'
    for obj in full_path.split('/'):
        if obj == 'disk:': continue

        path += f'/{obj}'
        try:
            disk.mkdir(path)
        except yadisk.exceptions.PathExistsError:
            ...

def reposSetup(disk: yadisk.YaDisk) -> None:
    mkdir(disk, f'disk:/warden/{os.getlogin()}/screenshots/{str(datetime.datetime.now()).split()[0]}/')