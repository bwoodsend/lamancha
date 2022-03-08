from . import exceptions
from ._collection import Component, python, Distribution


def _PyInstaller_hook_dir():
    import os
    return [os.path.dirname(__file__)]
