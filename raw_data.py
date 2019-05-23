"""
Import data sets from specfic tabs in an excel file and turn them into pandas DataFrames
"""
from collections import namedtuple
import argparse

import pandas

ParsedArgs = namedtuple('ParsedArgs', ['sets', 'numbers', 'independent_sets', 'which'])
def get_setup_arguments() -> ParsedArgs:

    """Return arguments specifying which data sets will be imported from input file."""

    parser = argparse.ArgumentParser()
    parser.add_argument('--sets', help='names of specific data sets to read from excel input file', nargs='+')
    parser.add_argument('--numbers', help='numbers to be assignd to data sets', nargs='+', type=int)
    parser.add_argument('--independent_sets', help='independent parameters to pass to correlations', nargs='+')
    parser.add_argument('--which', help='choose between normalized means or difference of means',
                        default='norm', choices=['norm', 'diff'])

    parsed_args = parser.parse_args()

    sets = parsed_args.sets
    numbers = parsed_args.numbers
    independent = parsed_args.independent_sets
    which = parsed_args.which

    all_data_sets = ['MBC', 'MBN', 'DOC', 'ERG', 'HWE-S', 'RESP', 'AS', 'TOC']
    all_numbers = range(1, len(all_data_sets)+1)

    if sets or numbers or (independent and which) :
        return parsed_args
    else:
        return ParsedArgs(sets=all_data_sets, numbers=all_numbers, independent_sets=independent, which=which)

def get_raw_data(key):

    """
    imports a single data set into a DataFrame
    """

    # data file to read data set from
    input_file = "all_tests.xlsx"

    # data set into DataFrame
    raw_data = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                 sheet_name=key, na_values=["-", " "]).rename_axis("days")

    raw_data.columns.rename(["soil", "treatment", "replicate"], level=None, inplace=True)
    raw_data.columns.set_levels(['c', 't'], level='treatment', inplace=True)
    raw_data.columns.set_levels(['ORG', 'MIN', 'UNC'], level='soil', inplace=True)
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
        raw_data.columns.set_levels(['c', 't'], level='treatment', inplace=True)
        raw_data = raw_data.swaplevel('soil', 'treatment', axis=1)

        dataframes[test] = raw_data

    return dataframes

