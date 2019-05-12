"""
Import data sets from specfic tabs in an excel file and turn them into pandas DataFrames
"""

import argparse

import pandas


def get_keys():

    """Return arguments specifying which data sets will be imported from input file."""

    parser = argparse.ArgumentParser()
    parser.add_argument('-specific', help='names of specific data sets to read from excel input file', nargs='+')
    parser.add_argument('-numbers', help='numbers to be assignd to data sets', nargs='+', type=int)
    parser.add_argument('-independent', help='independent parameters to pass to correlations', nargs='+')
    parser.add_argument('-which', help='choose between normalized means or difference of means',choices=['norm', 'diff'])

    parsed_args   = parser.parse_args()

    specfic       = parser.parse_args().specific
    numbers       = parser.parse_args().numbers
    independent   = parser.parse_args().independent
    which_normalized  = parser.parse_args().which

    all_data_sets = ['MBC', 'MBN', 'DOC', 'ERG', 'HWE-S', 'RESP', 'AS', 'TOC']
    all_numbers   = range(1, len(all_data_sets)+1)

    if specfic or numbers or independent:
        return parsed_args
    else:
        return all_data_sets, all_numbers
    #
    # if specfic and independent :
    #     return specfic, independent
    # elif specfic and numbers:
    #     return specfic, numbers
    # elif specfic and not numbers :
    #     return  specfic, range(1,len(specfic)+1)
    # elif independent and not specfic and not numbers:
    #     return all_data_sets, independent
    # else:
    #     return all_data_sets, all_numbers


def get_raw_data(key):

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
    raw_data.columns.set_levels(["c", "t"], level='treatment', inplace=True)
    raw_data = raw_data.swaplevel('soil', 'treatment', axis=1)

    return raw_data



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
        raw_data.columns.set_levels(["c", "t"], level='treatment', inplace=True)

        dataframes[test] = raw_data

    return dataframes


