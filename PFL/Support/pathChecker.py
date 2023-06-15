import os
from pathlib import Path


def pathChecker(check_path):
    """
The pathChecker function checks to see if a path exists. If it does not, the function creates the path.

Args:
    check_path: Check if the path exists

Returns:
    Nothing

Doc Author:
    Willem van der Schans
    """
    if os.path.exists(check_path):
        pass
    else:
        os.mkdir(check_path)

    return Path(check_path)
