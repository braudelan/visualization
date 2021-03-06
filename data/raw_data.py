"""
load data sets from specfic tabs in an excel file and turn them into pandas DataFrames
"""
from collections import OrderedDict

import pandas
from pandas import DataFrame

import data.stats as stats
import constants
from data.helpers import get_week_ends

# where data is uploaded from
INPUT_FILE = constants.main_input_file

# some constant parameters
DATA_SETS_NAMES = constants.parameters
SOILS = constants.LONG_TERM_TREATMENTS
LEVELS = constants.level_names
TREATMENTS = constants.treatment_labels


# def get_setup_arguments():
#
#     """Return arguments specifying which data sets will be imported from input file."""
#
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--sets',
#                         help='names of specific data sets to read from excel input file', nargs='+')
#
#     parsed_args = parser.parse_args()
#     sets = parsed_args.sets
#     all_data_sets = DATA_SETS_NAMES
#
#     if sets:
#         return parsed_args.sets
#     else:
#         return all_data_sets


def get_raw_data(data_set_name):

    """
    imports a single data set into a DataFrame
    """


    # data set into DataFrame
    raw_data = pandas.read_excel(INPUT_FILE,
                                 index_col=0,header=[0, 1, 2],
                                 sheet_name=data_set_name,
                                 na_values=["-", " "])

    # name the index
    raw_data.rename_axis(
        'days', inplace=True)

    # name and reorder the columns index
    raw_data = raw_data.swaplevel(
                            0, 1, axis=1)
    raw_data.columns.rename(
        LEVELS, level=None, inplace=True)  # level names
    raw_data.columns.set_levels(
        TREATMENTS, level='treatment', inplace=True) # 'treatment' level labels
    raw_data.columns.set_levels(
        SOILS, level='soil', inplace=True) # 'soil' level labels

    # specific processing for TOC and RESP data sets
    is_TOC = True if \
        data_set_name == 'TOC' else False
    is_ERG = True if\
        data_set_name == 'Erg' else False
    raw_data = (
        # raw_data * 24 if is_RESP else
        raw_data.drop(14) if is_TOC else
        raw_data
    )

    return raw_data


def get_multi_sets(keys, treatment=None, wknds=False, normalize_by=None) -> dict:

    """
    Import multipule data sets as DataFrames

    returns a dictionary of data frames for every data-set(=test or analysis)
    """

    # data file to read data sets from
    input_file = "../input_data.xlsx"

    # which data sets to iterate through
    data_set_names = keys

    # append all data sets into a dictionary
    dataframes = OrderedDict()
    for data_set_name in data_set_names:

        raw_data = get_raw_data(data_set_name)

        if data_set_name == 'Erg':
            raw_data = get_ergosterol_to_biomass()

        if wknds and data_set_name == 'MBC':
            week_ends = [0, 7, 14, 21, 28]
            raw_data = raw_data.loc[week_ends]

        if normalize_by:
            raw_data = normalize_by(raw_data)

        elif treatment:
            raw_data = raw_data[treatment]
        dataframes[data_set_name] = raw_data

    return dataframes


# normalizations and quotients
def control_normalize(raw_data, control=None):
    '''
    divide each replicate with the average of corresponding control replicates.

    each treatment replicate is divided by the average of 4 (or less)
     corresponding control replicates and finally returned as a percantage
    combination.

    parameter:
    raw_data: DataFrame
    the data to be normalized.

    parameter:
    control: str
    the name of the data set from which control values will be taken
    and normalized by. if this parameter is not given control values will be
    taken from raw_data.
    '''
    # raw data of treated samples
    treatment_raw = raw_data.loc[:, 't']

    # control raw_data
    if control:
        control_raw = get_raw_data(control)['c']
    else:
        control_raw = raw_data['c']

    control_means = stats.get_stats(control_raw).means  # shape ->(10,3)

    # empty dataframe with the same shape and indexes as raw_t
    control_reindexed = DataFrame().reindex_like(treatment_raw)  # shape ->(10,12)

    # fill above shaped empty dataframe with the mean value for every set of replicates
    for row in treatment_raw.index:
        for column in treatment_raw.columns:
            soil = column[0]
            control_reindexed.loc[row, column] =\
                                control_means.loc[row, soil]

    normalized = treatment_raw - control_reindexed
    normalized

    return  normalized


def normalize_to_initial(raw_data, treatment='t', initial=None):

    # raw data from treated samples
    treatment_raw = raw_data[treatment] if treatment else raw_data

    # get the mean of the first sampling of the control treatment
    if initial:
        control_raw = get_raw_data(initial)['c']
    else:
        control_raw = raw_data['c']

    control_means = stats.get_stats(control_raw).means  # shape ->(10,3)
    day_zero = control_means.loc[0]

    # empty dataframe with the same shape and indexes as raw_t
    control_reindexed = DataFrame().reindex_like(treatment_raw)  # shape ->(10,12)

    # fill above shaped empty dataframe with the mean value for every set of replicates
    for row in treatment_raw.index:
        for column in treatment_raw.columns:
            soil = column[0] # because there is a 'replicate' level, otherwise soil=column
            control_reindexed.loc[row, column] = day_zero[soil]

    normalized = treatment_raw - control_reindexed

    return normalized


def get_ergosterol_to_biomass():

    MBC_raw = get_raw_data('MBC')
    week_ends = get_week_ends(MBC_raw)
    MBC_raw_week_ends = MBC_raw.loc[week_ends]
    ERG_raw = get_raw_data('Erg')

    ERG_to_MBC = ERG_raw / MBC_raw_week_ends # compute ERG_to_MBC ratio
    ERG_to_MBC.loc[0, ('c', 'UNC', 1)] = None # irregular data (replicate#1 in MRE_treated UNC at day 0)
    ERG_to_MBC.loc[0, ('t', 'UNC', 1)] = None  # irregular data (replicate#1 in MRE_treated UNC at day 0)

    return ERG_to_MBC


def get_raw_MBC_to_MBN():

    raw_MBC = get_raw_data('MBC')
    week_ends = get_week_ends(raw_MBC)
    raw_MBC_week_ends = raw_MBC.loc[week_ends]
    raw_MBN = get_raw_data('MBN')
    raw_MBC_to_MBN = raw_MBC_week_ends / raw_MBN

    return raw_MBC_to_MBN


def get_raw_TOC_TON():
    raw_TOC = get_raw_data('TOC')
    raw_TON = get_raw_data('TON')
    raw_TOC_TON = raw_TOC / raw_TON

    return raw_TOC_TON


def toc_normalize(raw_data):

    # get baseline TOC in mg/kg
    toc_raw = get_raw_data('TOC')
    toc_baseline_stats = stats.get_baseline_stats(toc_raw)
    toc_baseline = toc_baseline_stats.means * 10000 # 10^4 mg in 1% of kg
    toc_stde = toc_baseline_stats.stde * 10000


def get_HWS_to_MBC(inverted=False):

    raw_MBC = get_raw_data('MBC')
    week_ends = get_week_ends(raw_MBC)
    raw_MBC_week_ends = raw_MBC.loc[week_ends]
    raw_HWS = get_raw_data('HWES')

    HWS_to_MBC = raw_HWS / raw_MBC_week_ends * 100
    MBC_to_HWS = raw_MBC_week_ends / raw_HWS * 100

    raw_HWS_to_MBC = HWS_to_MBC if not inverted else MBC_to_HWS

    return raw_HWS_to_MBC


def baseline_normalize(raw_data, treatment='t', baseline=None):

    # get baseline stats
    if baseline:
        raw_baseline = get_raw_data(baseline) * 10000 if \
                        baseline == 'TOC' else get_raw_data(baseline)
        baseline_stats = stats.get_baseline_stats(raw_baseline)
    else:
        baseline_stats = stats.get_baseline_stats(raw_data)
    baseline_means = baseline_stats.means

    # raw treatment data
    raw_data = raw_data.loc[:, treatment]

    # reshape baseline means to the same dimensions as raw_data
    baseline_reshaped = DataFrame().reindex_like(raw_data)
    for soil in SOILS:
        baseline_reshaped[soil] = baseline_means[soil]

    if baseline:
        normalized = raw_data / baseline_reshaped * 100
    else:
        normalized = (raw_data - baseline_reshaped) / baseline_reshaped * 100
    return normalized

