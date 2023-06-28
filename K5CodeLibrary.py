import glob
import inspect
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests


def currentTime(format_str=None):
    """
The currentTime function returns the current time in a specified format.

Args:
    format_str: Format the date and time in a specific way

Returns:
    The current time as a string

Doc Author:
    Willem van der Schans
    """
    if format_str is not None:
        return datetime.now().strftime(format_str)
    else:
        return datetime.now()


def errorHandler(code):
    """
The errorHandler function is used to handle errors that occur during the execution of a program.
It takes in an error code and returns a string explaining what the error was, as well as raising an exception.
The function also logs all errors to the log file.

Args:
    code: Determine what error to raise

Returns:
    A string with the error message

Doc Author:
    Willem van der Schans
"""
    input_code = code
    status_code = code

    if isinstance(status_code, str):
        try:
            status_code = int(status_code)
        except:
            status_code = 20000

    # This only works on python version >= 3.10 but is more efficient | Can be replaced with elif statements
    match status_code:

        # RESTAPI Error Responses [100-1000]
        case 200:
            logPrint(f"Request Successfully Completed | status code: {status_code}")
        case 204:
            error_string = f"Request failed: No content returned | status code: {status_code}"
            logPrint(error_string, log_type="e")
            raise ValueError(error_string)
        case 400:
            error_string = f"Request failed: Bad Request | status code: {status_code}"
            logPrint(error_string, log_type="e")
            raise ValueError(error_string)
        case 403:
            error_string = f"Request failed: Forbidden response (Check Auth & useragent) | status code: {status_code}"
            logPrint(error_string, log_type="e")
            raise ValueError(error_string)
        case 404:
            error_string = f"Request failed: Resource Not Found | status code: {status_code}"
            logPrint(error_string, log_type="e")
            raise ConnectionError(error_string)
        case 405:
            error_string = f"Request failed: Method not allowed | status code: {status_code}"
            logPrint(error_string, log_type="e")
            raise ValueError(error_string)
        case 500:
            error_string = f"Request failed: Internal Server Error | status code: {status_code}"
            logPrint(error_string, log_type="e")
            raise ConnectionError(error_string)
        case 501:
            error_string = f"Request failed: Method not implemented | status code: {status_code}"
            logPrint(error_string, log_type="e")
            raise ValueError(error_string)
        case 502:
            error_string = f"Request failed: Bad Gateway | status code: {status_code}"
            logPrint(error_string, log_type="e")
            raise ConnectionError(error_string)

        # Non-official Rest Error Codes [1000-1100]
        case 1404:
            error_string = f"Request failed: ConnectionError (Check URL) | status code: {status_code}"
            logPrint(error_string, log_type="e")
            raise ValueError(error_string)

        # Internal Errors [10000 - 20000]

            # File related Errors [11000-12000]
        case 11003:
            error_string = f"An Error Occurred: File not found (Check Path) | status code: {status_code}"
            logPrint(error_string, log_type="e")
            raise FileNotFoundError(error_string)

        # Case Exception handling
        case 20000:
            error_string1 = f"An error occurred: Unknown | status code: {str(input_code)}"
            error_string2 = f"An error occurred:  Cannot handle error code | status code: {status_code}"
            logPrint(error_string1, log_type="e")
            logPrint(error_string2, log_type="e")
            raise SystemError(error_string1)
        case _:
            error_string = f"An error occurred: fatal error during handling error {str(input_code)} | status code: ERROR REROUTED"
            logPrint(error_string, log_type="e")
            raise SystemError(error_string)


def file_downloader(url, file_name, destination_path, useragent=None, chunk_size_bytes=102400):

    # Setup
    """
The file_downloader function is a simple function that downloads files from the internet.
It takes in a url, file_name, destination_path and useragent as arguments. The url argument is the location of the
file to be downloaded on the internet. The file_name argument is what you want to name your downloaded file when it
is saved locally on your computer (this can be different than its original name). The destination path argument tells
the function where you want to save your downloaded file locally on your computer (if this directory does not exist it will create one for you). Finally, if desired, you can pass in

Args:
    url: Specify the url of the file to be downloaded
    file_name: Name the file that is downloaded
    destination_path: Specify where the file should be downloaded to
    useragent: Set the useragent header in the request
    chunk_size_bytes: Set the size of each chunk that is downloaded

Returns:
    The path of the downloaded file

Doc Author:
    Willem van der Schans
"""
    start_time = time.time()
    byte_counter = 0
    destination_path_string = os.path.join(destination_path, file_name)
    if useragent is None:
        useragent_header = {'User-Agent': '200 Request Agent Version 1.0'}
    else:
        useragent_header = {'User-Agent': f'{str(useragent)}'}

    # Core Download
    logPrint("Starting download")
    try:
        with requests.get(url, stream=True, headers=useragent_header) as response_stream:
            response_stream.raise_for_status()
            with open(destination_path_string, 'wb') as f:
                for chunk in response_stream.iter_content(chunk_size_bytes):
                    byte_counter += chunk_size_bytes / (1024 ** 2)
                    f.write(chunk)
                    sys.stdout.write("\r")
                    sys.stdout.write(f"Downloading | MB's: {round(byte_counter, 2)} MB |"
                                     f" Time: {round(time.time() - start_time, 2)} seconds |"
                                     f" Mbps: {round(byte_counter / (time.time() - start_time) * 8, 2)}")
                    sys.stdout.flush()
    # Error Handling
    except requests.exceptions.ConnectionError:
        errorHandler(1404)
    except Exception:
        errorHandler(response_stream.status_code)

    # Logging Download Information
    sys.stdout.write("\r")
    logPrint(f"Download Complete | Size: {round(byte_counter, 2)} MB,"
             f" Time: {round(time.time() - start_time, 2)} seconds,"
             f" Speed: {round(byte_counter / (time.time() - start_time) * 8, 2)} Mbps,"
             f" Location: {destination_path_string}")
    errorHandler(response_stream.status_code)

    # return path
    return destination_path_string


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


def logPrint(return_string, log_type="l", include_time=True, seperator=False):
    """
The logPrint function is a simple function that prints out the input string with some additional information.
The additional information includes:
    - The time of the print (if specified)
    - The file and line number where it was called from (always included)
    - A log type, which can be one of three options: LOG, WARNING or ERROR. This will change the color of the output text to match its type.

Args:
    return_string: Print the string that is passed to it
    log_type: Specify the type of log message
    include_time: Include the time in the log string
    seperator: Print a seperator line in the console

Returns:
    A string, which is the log_string

Doc Author:
    Willem van der Schans
"""
    caller_file = inspect.stack()
    caller_file = caller_file[len(caller_file) - 1]
    caller_file = f"{str(os.path.basename(caller_file.filename))}:{caller_file.lineno}"
    log_type_str = str(log_type).upper()
    invalid_flag = False
    time_inp = include_time
    seperator_inp = seperator

    if seperator_inp:
        time_inp = False

    if log_type_str in ["LOG", "WARNING", "ERROR", "L", "W", "E", "NONE"]:
        if "LOG" in log_type_str or "L" in log_type_str:
            log_type_str = "LOG:    "
        elif "WARNING" in log_type_str or "W" in log_type_str:
            log_type_str = "WARNING:"
        elif "ERROR" in log_type_str or "E" in log_type_str:
            log_type_str = "ERROR:  "
        elif log_type_str == "NONE":
            log_type_str = ""
        else:
            invalid_flag = True
    else:
        invalid_flag = True

    if log_type_str == "":
        log_string = f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} | {caller_file} | {return_string}"
    elif time_inp:
        log_string = f"{log_type_str} {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} | {caller_file} | {return_string}"
    elif seperator_inp:
        log_string = f"\n{'-' * 10}{return_string}{'-' * 10}"
    else:
        log_string = f"{log_type_str} {caller_file} | {return_string}"

    if invalid_flag:
        print(log_string)
        warning_string = f"WARNING: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} | logPrint.py:XX | Invalid input for log type"
        print(warning_string)
        return log_string, warning_string
    else:
        print(log_string)
        return log_string


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


def printFull(x):
    """
The printFull function is used to print the full contents of a pandas dataframe.
It does this by setting the display options for max rows, columns, width and float format to None.
This allows us to see all the rows and columns in our dataframe without truncation or ellipses (...).
The function then prints out our dataframe using these new settings before resetting them back to their defaults.

Args:
    x: Pass in the dataframe that you want to print

Returns:
    A print of the dataframe with no limits on rows or columns

Source:
    https://stackoverflow.com/a/51593236

Doc Author:
    Willem van der Schans
"""
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')


def progressPrint(text_string):
    """
The progressPrint function is a simple function that prints text to the console
without creating a new line. This allows for printing of progress information without
creating an unreadable mess of lines in the console.

Args:
    text_string: Print the text string to the console

Returns:
    Nothing

Doc Author:
    Willem van der Schans
"""
    sys.stdout.write("\r")
    sys.stdout.write(text_string)
    sys.stdout.flush()
