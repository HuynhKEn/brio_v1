
import os
import sys

class UtilsRoot:
    def __init__(self):
        self._root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def get_root_path():
        return UtilsRoot()._root_path

