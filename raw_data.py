"""
load data sets from specfic tabs in an excel file and turn them into pandas DataFrames
"""
from collections import namedtuple
import argparse

import pandas

from helpers import Constants, get_week_ends

DATA_SETS_NAMES = Constants.parmeters
SOILS = Constants.groups
LEVELS = Constants.level_labels
TREATMENTS = Constants.treatment_labels


ParsedArgs = namedtuple('ParsedArgs', ['sets', 'numbers', 'independent_sets', 'which'])
def get_setup_arguments() -> ParsedArgs:

    """Return arguments specifying which data sets will be imported from input file."""

    parser = argparse.ArgumentParser()
    parser.add_argument('--sets',
                        help='names of specific data sets to read from excel input file', nargs='+')
    parser.add_argument('--numbers',
                        help='numbers to be assignd to data sets', nargs='+', type=int)
    parser.add_argument('--independent_sets',
                        help='independent parameters to pass to correlations', nargs='+')
    parser.add_argument('--which',
                        help='choose between normalized means or difference of means',
                        default='norm', choices=['norm', 'diff'])

    parsed_args = parser.parse_args()

    sets = parsed_args.sets
    numbers = parsed_args.numbers
    independent = parsed_args.independent_sets
    which = parsed_args.which

    all_data_sets = DATA_SETS_NAMES
    all_numbers = range(1, len(all_data_sets)+1)

    if sets or numbers or (independent and which):
        return parsed_args
    else:
        return ParsedArgs(sets=all_data_sets, numbers=all_numbers,
                          independent_sets=independent, which=which)


def get_raw_data(data_set_name):

    """
    imports a single data set into a DataFrame
    """

    # data file to read data set from
    input_file = "all_tests.xlsx"

    # data set into DataFrame
    raw_data = pandas.read_excel(input_file,
                                 index_col=0,header=[0, 1, 2],
                                 sheet_name=data_set_name,
                                 na_values=["-", " "])
    raw_data.rename_axis('days', inplace=True) # label for index
    raw_data.columns.rename(LEVELS,
                            level=None, inplace=True)  # level labels
    raw_data.columns.set_levels(TREATMENTS,
                                level='treatment', inplace=True) # treatment level categories
    raw_data.columns.set_levels(SOILS, level='soil',
                                            inplace=True) # soil level categories
    raw_data = raw_data.swaplevel('soil',
                                  'treatment', axis=1)

    is_TOC = True if data_set_name == 'TOC' else False
    is_RESP = True if data_set_name == 'RESP' else False
    raw_data = (
        raw_data * 24 if is_RESP else
        raw_data.drop(14) if is_TOC else
        raw_data
    )

    return raw_data


def get_ergosterol_to_biomass():

    MBC_raw = get_raw_data('MBC')
    week_ends = get_week_ends(MBC_raw)
    MBC_raw_week_ends = MBC_raw.loc[week_ends]
    ERG_raw = get_raw_data('ERG')
    ERG_to_MBC = ERG_raw / MBC_raw_week_ends # compute ERG_to_MBC ratio
    ERG_to_MBC = ERG_to_MBC.drop(0) # drop day 0 with irregular data

    return ERG_to_MBC


def get_raw_MBC_to_MBN():

    raw_MBC = get_raw_data('MBC')
    week_ends = get_week_ends(raw_MBC)
    raw_MBC_week_ends = raw_MBC.loc[week_ends]
    raw_MBN = get_raw_data('MBN')
    raw_MBC_to_MBN = raw_MBC_week_ends / raw_MBN

    return raw_MBC_to_MBN


def get_raw_TOC_TN():
    raw_TOC = get_raw_data('TOC')
    raw_TN = get_raw_data('TON')
    raw_TOC_TN = raw_TOC / raw_TN

    return raw_TOC_TN

def get_raw_basal_qCO2():
    raw_control_MBC = get_raw_data('MBC')['c']
    raw_control_RESP = get_raw_data('RESP', ['c'])



def get_multi_sets(keys) -> dict:

    """
    Import multipule data sets as DataFrames

    returns a dictionary of dataframes for every data-set(=test)
    """

    # data file to read data sets from
    input_file = "all_tests.xlsx"

    # which data sets to iterate through
    data_set_names = keys

    # dictionary of DataFrames to append data sets into
    dataframes = {}


    for data_set_name in data_set_names:

        # input data into DataFrame ahd append into dataframes
        raw_data = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                     sheet_name=data_set_name, na_values=["-", " "])

        raw_data.rename_axis('days', inplace=True)  # label for index
        raw_data.columns.rename(["soil", "treatment", "replicate"],
                                level=None, inplace=True)  # level labels
        raw_data.columns.set_levels(['c', 't'], level='treatment',
                                    inplace=True)  # treatment level categories
        raw_data.columns.set_levels(['ORG', 'MIN', 'UNC'],
                                    level='soil', inplace=True)  # soil level categories
        raw_data = raw_data.swaplevel('soil', 'treatment', axis=1)

        dataframes[data_set_name] = raw_data

    return dataframes