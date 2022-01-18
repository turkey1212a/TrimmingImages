from datetime import datetime
import numpy as np
import os
from pathlib import Path
import logging

def madir_if_absent(path):
    if not os.path.exists(path):
        os.makedirs(path)


def filename_without_extention(path):
    return Path(path).stem


def filename_with_extention(path):
    return Path(path).name


def file_extention(path):
    return Path(path).suffix


def parent_dir(path):
    return Path(path).parent


def timestamp_time(time, mode='numerics'):
    if mode == 'numerics':
        ret = f'{time.year:04}{time.month:02}{time.day:02}_{time.hour:02}{time.minute:02}{time.second:02}'
    elif mode == 'time_string':
        ret = f'{time.year:04}/{time.month:02}/{time.day:02}/{time.hour:02}:{time.minute:02}:{time.second:02}'
    return ret


def timestamp_now(mode='numerics'):
    return timestamp_time(datetime.now(), mode)


def log_write(msg: str, flg: bool):
    if bool:
        logging.debug(msg)
