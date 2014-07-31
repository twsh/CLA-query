#!/usr/bin/env python3

import os


class ResponseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ExtensionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ColumnError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
# An exception to raise in case `get_column_by_name`
# is called on a worksheet it cannot deal with


def check_extensions(p, l):
    """ str, list of str -> string, bool
    Take a path and a list of strings.
    If the path has one of the list as an extension,
    return the path.
    If the path has another extension,
    raise an ExtensionError.
    If the path has no extension, check the list in order for files with that
    extension then return the path with the first one added.
    If a file isn't found, raise an ExtensionError.
    >> check_extensions('foo.txt', ['txt'])
    'foo.txt'
    >> check_extensions('foo.md', ['txt'])
    None
    >> check_extensions('foo', ['txt'])
    'foo.txt'
    """
    if os.path.splitext(p)[1][1:] in l:
        return p
    elif os.path.splitext(p)[1] != '':
        message = ("I know about these extensions: {}. "
                   "You have chosen an extension I don't know about: {}."
                   .format(', '.join(l), os.path.splitext(p)[1][1:]))
        raise ExtensionError(message)
    else:
        for i in range(len(l)):
            if os.path.isfile(p + '.' + l[i]):
                return p + '.' + l[i]
            else:
                message = ("I know about these extensions: {}. "
                           "I couldn't find a file with one of these "
                           "extensions."
                           .format(', '.join(l)))
                raise ExtensionError(message)


def get_column_by_name(worksheet, s):
    """ Worksheet, String -> int
    Take an openpyxl Worksheet and a string.
    Return the column number of the column with the string as its header.
    Raise an exception if there are not exactly one such columns.
    """
    matches = 0
    for i in range(1, len(worksheet.columns)+1):
        if (worksheet.cell(row=1, column=i).value is not None
                and worksheet.cell(row=1, column=i).value.strip().lower() ==
                s.lower()):
            matches += 1
            column = i
    if matches == 1:
        return column
    else:
        if matches < 1:
            message = "I couldn't find a column called '{}'.".format(s)
        elif matches > 1:
            message = ("I found too many columns ({}) "
                       "called '{}'.".format(matches, s))
        raise ColumnError(message)


def get_ISBNs(workbook, s):
    """ Workbook, String -> List of Strings
    Take an openpyxl workbook and a string, return a list of the values as
    strings of the cells in the column of which the string is the name.
    """
    worksheet = workbook.active
    try:
        ISBN_column = get_column_by_name(worksheet, s)
    except ColumnError:
        raise
    # If there's no suitable column pass up the exception
    else:
        return [str(worksheet.cell(row=i, column=ISBN_column).value).strip()
                for i in range(2, len(worksheet.rows)+1)
                if worksheet.cell(row=i, column=ISBN_column).value is not None]


def write_responses(workbook, d, s):
    """ Workbook, Dictionary, String -> Workbook
    Take an openpyxl workbook, a dictionary and a string.
    For each key in the dictionary which is a value of the cell in the column
    which has the string as its header, write its value in the final column of
    the spreadsheet in the corresponding row.
    Call the final column 'Responses', and match all formatting.
    """
    worksheet = workbook.active
    last_column = len(worksheet.columns)+1
    try:
        ISBN_column = get_column_by_name(worksheet, s)
    except ColumnError:
        raise
    else:
        for i in range(1, len(worksheet.rows)+1):
            if worksheet.cell(row=i, column=ISBN_column).value is not None\
                    and str(worksheet.cell(row=i, column=ISBN_column).value).strip() in d:
                worksheet.cell(row=i, column=last_column).value =\
                    d[str(worksheet.cell(row=i, column=ISBN_column).value).strip()]
                worksheet.cell(row=i, column=last_column).style =\
                    worksheet.cell(row=i, column=ISBN_column).style
        worksheet.cell(row=1, column=last_column).value = 'Response'
        worksheet.cell(row=1, column=last_column).style =\
            worksheet.cell(row=1, column=ISBN_column).style
        return workbook


def check_for_integers(workbook, s):
    """ Workbook, String -> bool
    Take an openpyxl workbook and a string.
    Return True iff the column of which the string is the header contains values
    which are integers.
    """
    worksheet = workbook.active
    try:
        ISBN_column = get_column_by_name(worksheet, s)
    except ColumnError:
        raise
    else:
        for i in range(1, len(worksheet.rows)+1):
            if isinstance(worksheet.cell(row=i, column=ISBN_column).value, int):
                return True
    return False
