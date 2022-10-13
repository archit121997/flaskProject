
import re
import os
import pandas as pd

from config import *





def find_match(val):
    return bool(re.fullmatch(r'^P[0-9][0-9][0-9][0-9]$', val))




def columnsWithNoneValues(file_path):

    fname = file_path
    df = pd.read_csv(fname)
    none_index = []
    for col_index, c in enumerate(df.columns):
        temp = df[df[c].isna()][c]
        for row_index in temp.index:
            none_index.append((col_index, row_index))

    return none_index



def parseCSV(file_path):
    fname = file_path

    exceptions = []

    try:
        df = pd.read_csv(fname)
    except FileNotFoundError as e:
        print("File not found.")
        exceptions.append(e.__class__.__name__ + ': ' + str(e))
    except pd.errors.EmptyDataError:
        print("No data")
    except pd.errors.ParserError:
        print("Parse error")
    except Exception:
        print("Some other exception")


    return exceptions



def startsWithP(file_path):
    fname = file_path
    df = pd.read_csv(fname)

    df['is_valid_child_prop'] = df.apply(lambda x: find_match(x['Child Property ID']), axis=1)

    return df



def dataTypeValidation(file_path):

    fname = file_path
    df = pd.read_csv(fname)

    exceptions =[]
    dtype_dict = dict(df.dtypes)

    for col,col_type in columnsToCheckForDatatypes.items():

        if dtype_dict[col] != col_type:
            exceptions.append('Dtype mismatch:  expected type  to be opbjectbut found' + str(dtype_dict[col]))


    return exceptions










