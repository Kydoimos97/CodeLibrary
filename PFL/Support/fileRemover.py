import glob
import os

from PFL.Support.errorHandler import errorHandler


def fileRemover(remove_path):
    """
    The fileRemover function is used to remove all files in a given directory.
        It takes one argument, the path of the directory to be emptied.
        The function uses glob and os modules to iterate through each file in the
        specified directory and delete them using os.remove(). If an exception occurs,
        it will logPrint out that there was an error deleting a specific file.

    Args:
        remove_path: Specify the path of the directory that you want to remove files from

    Returns:
        Nothing

    Doc Author:
        Willem van der Schans
"""
    dir_files = glob.glob(os.path.join(remove_path, "*"))
    for f in dir_files:
        try:
            os.remove(f)
        except Exception as e:
            errorHandler(11003)
            pass
