import sys


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