from PFL.Support.logPrint import logPrint


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
