"""
Import data sets from specfic tabs in an excel file and turn them into pandas DataFrames
"""

import argparse

import pandas


def get_args():

    """
    Parse tab names arguments to be used for getting data sets from excel file

    returns a list of data set keys
    returns a corresponding list of id numbers
    both argument lists are optional
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-specific_sets', help='names of specific data sets to read from excel input file', nargs='+')
    parser.add_argument('-specific_nums', help='numbers to be assignd to data sets', nargs='+', type=int)
    specific_sets = parser.parse_args().specific_sets
    specific_nums = parser.parse_args().specific_nums

    return specific_sets, specific_nums


def get_multi_sets(args):

    """
    Import multipule data sets into **DataFrame**s
    """

    # data file to read data sets from
    input_file = "all_tests.xlsx"

    # which data sets to iterate through
    TESTS = args

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




