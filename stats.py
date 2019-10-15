''' calculate and return different statistics from raw data.'''
import pdb

from collections import namedtuple
import pandas
from pandas import DataFrame
from raw_data import get_multi_sets
from helpers import get_week_ends, Constants

SOILS = Constants.groups
STATS_NAMES = [
    'means',
    'stde',
    'stdv',
]

Stats = namedtuple('Stats', STATS_NAMES)

def get_stats(raw_data: DataFrame, treatment: str) -> namedtuple:
    '''
    calculate basic statistics for a given data sets.

    :returns
    namedtuple: the different statistics calculated

    '''

    # means
    groupby_soil_treatment = raw_data.groupby(level=['treatment', 'soil'], axis=1)

    means = groupby_soil_treatment.mean()  # means of 4 replicates
    stdv = groupby_soil_treatment.std() # std deviation
    sdte = groupby_soil_treatment.sem()  # std error
    # drop control\MRE
    means = means.xs(treatment, level=0, axis=1)
    stdv = stdv.xs(treatment, level=0, axis=1)
    stde = sdte.xs(treatment, level=0, axis=1)

    means.treatment_label = treatment
    # control = means.xs('c', level=0, axis=1)
    # control_SE = means_SE.xs('c', level=0, axis=1)
    # control_SD = means_SD.xs('c', level=0, axis=1)
    # control.treatment_label = 'c'

    # treatment effect
    # difference = MRE - control   # treatment - control
    # normalized_diff = difference / control * 100  # difference normalized to control (percent)

    return Stats(
        means=means,
        stde=stde,
        stdv=stdv,
        # difference=difference,
        # normalized_diff=normalized_diff
    )

def normalize_to_control(raw_data):
    '''subtracts the average of 4(or less) control replicates from each treatment replicate.'''

    raw_t = raw_data.loc[:, ('t', SOILS)] # MRE treatment
    raw_c = raw_data.loc[:, ('c', SOILS)] # control

    control_means = get_stats(raw_c, 'c').means # shape ->(10,3)

    # empty dataframe with the same shape and indexes as raw_t
    control_means_shaped = pandas.DataFrame().reindex_like(raw_t)

    for row in control_means_shaped.index:
        for column in control_means_shaped.columns:
            soil = column[1]
            control_means_shaped.loc[row, column] = control_means.loc[row, soil]

    normalized = raw_t / control_means_shaped * 100
    normalized = get_stats(normalized, 't')
    normalized_means = normalized.means
    normalized_stde = normalized.stde

    return Stats(
        means=normalized_means,
        stde=normalized_stde,
        stdv=None
    )

def normalize_to_baseline(raw_data):
    '''represent the means of each soil as a percentage of corresponding baseline value '''

    # get baseline stats
    baseline_stats = get_baseline(raw_data)
    baseline_means = baseline_stats.means
    baseline_stde = baseline_stats.stde

    # get treatment stats
    treatment_stats = get_stats(raw_data, 't')
    treatment_means: DataFrame = treatment_stats.means
    treatment_stde = treatment_stats.stde

    # setup empty dataframes for normalized stats
    index = treatment_means.index
    columns = treatment_means.columns
    normalized = DataFrame(index=index, columns=columns)
    normalized_stde = DataFrame(index=index, columns=columns)

    for soil in SOILS:

        treatment_data = treatment_means[soil]
        treatment_error = treatment_stde[soil]
        treatment_relative_error = treatment_error / treatment_data #relative stnd error

        baseline = baseline_means[soil]
        baseline_error = baseline_stde[soil]
        baseline_relative_error = baseline_error / baseline

        divided_by_baseline = treatment_data / baseline #data normalized to baseline
        normalized_relative_error = treatment_relative_error + baseline_relative_error
        normalized_error = normalized_relative_error * divided_by_baseline
        normalized[soil] = divided_by_baseline * 100
        normalized_stde[soil] = normalized_error * 100

    return Stats(
        means=normalized,
        stde=normalized_stde,
        stdv=None
    )


def normalize_to_initial(raw_data):
    '''represent the means of each soil as a percentage of corresponding initial value '''

    # get initial values
    stats = get_stats(raw_data, 'c')
    means = stats.means
    stde = stats.stde
    initial_values = means.loc[0] #means of day 0
    initial_values_stde = stde.loc[0]

    # get treatment stats
    treatment_stats = get_stats(raw_data, 't')
    treatment_means: DataFrame = treatment_stats.means
    treatment_stde = treatment_stats.stde

    # setup empty dataframes for normalized stats
    index = treatment_means.index
    columns = treatment_means.columns
    normalized = DataFrame(index=index, columns=columns)
    normalized_stde = DataFrame(index=index, columns=columns)

    for soil in SOILS:

        treatment_data = treatment_means[soil]
        treatment_error = treatment_stde[soil]
        treatment_relative_error = treatment_error / treatment_data #relative stnd error

        initial = initial_values[soil]
        initial_error = initial_values_stde[soil]
        initial_relative_error = initial_error / initial

        divided_by_initial = treatment_data / initial #data normalized to initial
        normalized_relative_error = treatment_relative_error + initial_relative_error
        normalized_error = normalized_relative_error * divided_by_initial
        normalized[soil] = divided_by_initial * 100
        normalized_stde[soil] = normalized_error * 100

    return Stats(
        means=normalized,
        stde=normalized_stde,
        stdv=None
    )


def get_baseline(raw_data):
    """
    for each soil, get the mean value of control samples across the entire time line.

    week day samplings between MRE applications are excluded from calculations
     to avoid local fluctuations as a result of water additions.
    """

    week_ends_control = raw_data.loc[get_week_ends(raw_data), ('c', SOILS)]  # week ends control samples from raw data
    week_ends_control.columns = week_ends_control.columns.droplevel('treatment')
    control_stacked = week_ends_control.stack(level='replicate')

    means = control_stacked.mean().reindex(SOILS)
    stdv = control_stacked.std()
    stde = control_stacked.sem()

    return Stats(
        means=means,
        stde=stde,
        stdv=stdv,
    )


def get_carbon_stats():
    '''calculate '''

    # which data sets to get
    sets_names = ['MBC', 'MBN', 'RESP', 'DOC', 'HWS', 'TOC']
    # get the raw data
    dataframes = get_multi_sets(sets_names)

    # get baseline value for TOC
    raw_TOC = dataframes['TOC']
    raw_TOC_control = raw_TOC.loc[:, 'c']
    exclude_day14 = raw_TOC_control.drop(index=14)
    stacked = exclude_day14.stack()
    TOC_means = stacked.mean() * 1000
    TOC_stde = stacked.sem() * 1000
    TOC_relative_stde = TOC_stde / TOC_means

    normalized_to_TOC = {}
    for set in sets_names:
        raw = dataframes[set]
        treatment_stats = get_stats(raw, 't')
        control_stats = get_stats(raw, 'c')
        normalized_to_control = normalize_to_control(raw)

        stats = {'treatment': treatment_stats,
                 'control': control_stats,
                 'normalized': normalized_to_control}
        pdb.set_trace()
        for category in stats.keys():
            category_stats = stats[category]
            means = category_stats.means
            stde = category_stats.stde
            relative_stde = stde / means

            divided_by_TOC = means / TOC_means
            percent_of_TOC = divided_by_TOC * 100
            relative_stde_of_quotient = ( TOC_relative_stde**2 + relative_stde**2)**0.5 * 100 # multiplied by 100 for percentage

            normalized_to_TOC[set][category]['means'] = percent_of_TOC
            normalized_to_TOC[set][category]['stde'] = relative_stde_of_quotient

    return normalized_to_TOC
    # # a dict with stats for treatment\control\normalized
    # MBC = statistics['MBC']
    # DOC = statistics['DOC']
    # HWS = statistics['HWS']
    #
    # # get baseline value for TOC
    # raw_TOC = dataframes['TOC']
    # raw_TOC_control = raw_TOC.loc[:,'c']
    # exclude_day14 = raw_TOC_control.drop(index=14)
    # stacked = exclude_day14.stack()
    # TOC_means = stacked.mean()
    # TOC_stde = stacked.sem()
    #
    # for set in sets_names:
    #
    # MBC_treatment = MBC['treatment']
    # MBC_treatment_means = MBC_treatment.means
    # MBC_treatment_stde = MBC_treatment.stde
    #
    # MBC_normalized = MBC['normalized']
    # MBC_normalized_means = MBC_normalized.means
    # MBC_normalized_stde = MBC_normalized.stde
    #
    # DOC_treatment = DOC['treatment']
    # DOC_treatment_means = DOC_treatment.means
    # DOC_treatment_stde = DOC_treatment.stde
    #
    # HWS_treatment = HWS['treatment']
    # HWS_treatment_means = HWS_treatment.means
    # HWS_treatment_stde = HWS_treatment.stde
    #
    # # divide by TOC
    # divided = {}
    # for
    # return statistics
