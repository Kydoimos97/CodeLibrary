import pandas as pd


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

