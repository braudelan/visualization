"""
Import data sets from specfic tabs in an excel file and turn them into pandas DataFrames
"""

import argparse

import pandas


def get_keys():

    """
    get arguments specifying which data sets will be imported from excel file.

    if arguments are passed in command line,
    returns a list of specific data set keys.
    also returns a corresponding list of id numbers.
    both lists are optional arguments.
    if no arguments are passed, a list of all data sets keys will be returned.
    also a range the length of all data sets will be returned
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-data_sets', help='names of specific data sets to read from excel input file', nargs='+')
    parser.add_argument('-nums', help='numbers to be assignd to data sets', nargs='+', type=int)

    spec_data_sets = parser.parse_args().data_sets
    numbers        = parser.parse_args().nums
    all_data_sets  = ['MBC', 'MBN', 'DOC', 'ERG', 'HWE-S', 'RESP', 'AS', 'TOC']
    all_numbers    = range(1, len(all_data_sets)+1)

    if spec_data_sets and numbers:
        return spec_data_sets, numbers
    elif spec_data_sets and not numbers:
        return  spec_data_sets, range(1,len(spec_data_sets)+1)
    else:
        return all_data_sets, all_numbers


def get_multi_sets(keys):

    """
    Import multipule data sets as DataFrames

    returns a dictionary of dataframes for every data-set(=test)
    """

    # data file to read data sets from
    input_file = "all_tests.xlsx"

    # which data sets to iterate through
    TESTS = keys

    # dictionary of DataFrames to append data sets into
    dataframes = {}

    for test in TESTS:

        # input data into DataFrame ahd append into dataframes
        raw_data = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                         sheet_name=test,
                                         na_values=["-", " "]).rename_axis("days")
        raw_data.columns.rename(["soil", "treatment", "replicate"],
                                level=None, inplace=True)
        raw_data.columns.set_levels(["c", "t"], level=1, inplace=True)

        dataframes[test] = raw_data

    return dataframes



def get_single_set(key):

    """
    imports a single data set into a DataFrame
    """

    # data file to read data set from
    input_file = "all_tests.xlsx"

    # data set into DataFrame
    raw_data = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                 sheet_name=key,
                                 na_values=["-", " "]).rename_axis("days")
    raw_data.columns.rename(["soil", "treatment", "replicate"],
                            level=None, inplace=True)
    raw_data.columns.set_levels(["c", "t"], level=1, inplace=True)

    return raw_data




