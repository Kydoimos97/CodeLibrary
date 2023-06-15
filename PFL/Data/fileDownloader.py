import os
import sys
import time

import requests

from PFL.Support.errorHandler import errorHandler
from PFL.Support.logPrint import logPrint


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

