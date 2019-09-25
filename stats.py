''' calculate and return different statistics from raw data.'''

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

BasicStats = namedtuple('BasicStats', STATS_NAMES)
BaselineStats = namedtuple('BaselineStats', STATS_NAMES)

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

    return BasicStats(
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

    normalized = raw_t - control_means_shaped

    return normalized

def normalize_to_baseline(raw_data):
    '''represent the means of each soil as a percentage of corresponding baseline value '''

    # get baseline
    baseline_stats = get_baseline(raw_data)
    baseline_means = baseline_stats.means
    baseline_stdv = baseline_stats.stdv

    # get treatment means
    treatment_stats = get_stats(raw_data, 't')
    treatment_means: DataFrame = treatment_stats.means
    treatment_stdv = treatment_stats.stdv

    index = treatment_means.index
    columns = treatment_means.columns
    normalized = DataFrame(index=index, columns=columns)

    for soil in SOILS:
        treatment_data = treatment_means[soil]
        baseline = baseline_means[soil]
        percent_of_baseline = treatment_data / baseline * 100

        normalized[soil] = percent_of_baseline

    return normalized









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

    return BasicStats(
        means=means,
        stde=stde,
        stdv=stdv,
    )


def get_carbon_stats():
    '''calculate '''
    sets_names = ['MBC', 'MBN', 'RESP', 'DOC', 'HWS', 'TOC']
    dataframes = get_multi_sets(sets_names)
    statistics = {}
    for set in sets_names:
        raw = dataframes[set]
        stats = get_stats(raw)
        means = stats.means
        stde = stats.stde
        data_set_stats = {'means': means, 'means_stde': stde}
        statistics[set] = data_set_stats

    MBC = statistics['MBC']['means']
    MBN = statistics['MBN']['means']
    HWES = statistics['HWS']['means']
    RESP = statistics['RESP']['means']
    DOC = statistics['DOC']['means']
    HWES_C = HWES / 4  # 40% C in glucose
    C_to_N_ratio = MBC / MBN
    C_to_N_ratio = C_to_N_ratio.loc[get_week_ends(C_to_N_ratio)]
    # soil_available_C = MBC + HWES_C + DOC
    # available_C_control = available_C.xs(key='c', level=0, axis=1)
    # available_C_MRE = available_C.xs(key='t', level=0, axis=1)
    # available_C_difference = available_C_MRE- available_C_control # todo plot available_c and available_C_difference

    return C_to_N_ratio
