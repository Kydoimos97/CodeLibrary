import ast

from K5CodeLibrary.Support.logPrint import logPrint


def dataframeToDictLiteral(dataframe, data_column, id_column=None):
    """
The dataframeToDictLiteral function takes a dataframe and converts it to a dictionary.
The function requires two arguments: the dataframe, and the column name of the column containing
the values that will be used as values in the output dictionary. The optional third argument is
the name of a column that contains unique identifiers for each row; if this argument is not provided,
then each row's index will be used as its identifier.

Args:
    dataframe: Specify the dataframe to be converted
    data_column: Specify which column in the dataframe contains the data to be converted
    id_column: Specify the column that is used as a key in the dictionary

Returns:
    A dictionary of the form {id: data}, where id is either an integer or a string, and data is a list

Doc Author:
    Willem van der Schans
"""
    df = dataframe.reset_index(drop=True)
    if id_column is not None:
        output_dict = {}
        for row in range(len(df)):
            try:
                output_dict[str(df[id_column][row])] = df[data_column][row]
            except Exception as e:
                logPrint(f"Conversion failed of row {row} with exception {e}, continuing...")
                continue
    else:
        output_dict = {}
        for row in range(len(df)):
            try:
                output_dict[row] = ast.literal_eval(df[data_column][row])
            except Exception as e:
                logPrint(f"Conversion failed of row {row} with exception {e}, continuing...")
                continue

    return output_dict
