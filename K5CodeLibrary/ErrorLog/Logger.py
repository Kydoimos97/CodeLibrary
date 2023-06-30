import datetime
import os
import sys
from pathlib import Path
from K5CodeLibrary.Support.pathChecker import pathChecker


class Logger:

    def __init__(self, folder):

        pathChecker(Path(os.path.expandvars(fr'%APPDATA%\{folder}')))
        pathChecker(Path(os.path.expandvars(fr'%APPDATA%\{folder}\Logs')))
        file_path = Path(os.path.expandvars(fr'%APPDATA%\{folder}\Logs')).joinpath(
        f"{datetime.datetime.today().strftime('%m%d%Y_%H%M%S')}.log")
        self.dir_path = Path(os.path.expandvars(fr'%APPDATA%\{folder}\Logs'))
        self.log_cleaner()
        self.console = sys.stdout
        self.file = open(file_path, 'w')

    def write(self, message):
        self.console.write(message)
        self.file.write(message)

    def flush(self):
        self.console.flush()
        self.file.flush()

    def sorted_ls(self):
        mtime = lambda f: os.stat(os.path.join(self.dir_path, f)).st_mtime
        return list(sorted(os.listdir(self.dir_path), key=mtime))

    def log_cleaner(self):
        del_list = self.sorted_ls()[0:(len(self.sorted_ls()) - 100)]
        for file in del_list:
            os.remove(self.dir_path.joinpath(file))
            print(f"{datetime.datetime.today().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]} | Log file {file} deleted")

