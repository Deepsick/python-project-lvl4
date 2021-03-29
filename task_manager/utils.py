import pathlib
from os import path
import json

FIXTURES_DIR = 'fixtures'


def get_path(file_name):
    dir_path = pathlib.Path(__file__).absolute().parent
    return path.join(dir_path, FIXTURES_DIR, file_name)


def read_file(path, mode="r"):
    with open(path, mode) as f:
        result = f.read()
    return result


def read_fixture(file_name, mode="r"):
    return json.loads(read_file(get_path(file_name), mode))
