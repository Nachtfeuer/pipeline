"""Module table."""
# pylint: disable=superfluous-parens


def calculate_columns(sequence):
    """
    Find all row names and the maximum column widths.

    Args:
        columns (dict): the keys are the column name and the value the max length.

    Returns:
        dict: column names (key) and widths (value).
    """
    columns = {}

    for row in sequence:
        for key in row.keys():
            if key not in columns:
                columns[key] = len(key)

            value_length = len(str(row[key]))
            if value_length > columns[key]:
                columns[key] = value_length

    return columns


def calculate_row_format(columns, keys=None):
    """
    Calculate row format.

    Args:
        columns (dict): the keys are the column name and the value the max length.
        keys (list): optional list of keys to order columns as well as to filter for them.

    Returns:
        str: format for table row
    """
    row_format = ''
    if keys is None:
        keys = columns.keys()
    else:
        keys = [key for key in keys if key in columns]

    for key in keys:
        if len(row_format) > 0:
            row_format += "|"
        row_format += "%%(%s)-%ds" % (key, columns[key])

    return '|' + row_format + '|'


def pprint(sequence, keys=None):
    """
    Print sequence as ascii table to stdout.

    Args:
        sequence (list or tuple): a sequence with a dictionary each entry.
        keys (list): optional list of keys to order columns as well as to filter for them.
    """
    if len(sequence) > 0:
        columns = calculate_columns(sequence)
        row_format = calculate_row_format(columns, keys)
        header = row_format % dict([(key, key.title()) for key in columns])
        separator = row_format % dict([(key, '-' * columns[key]) for key in columns])

        print(separator)
        print(header)
        print(separator)

        for row in sequence:
            print(row_format % row)

        print(separator)
