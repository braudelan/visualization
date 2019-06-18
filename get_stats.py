# todo get baseline values by calculating an average over control.
#   use dataframe.drop([]) to get only week ends and dataframde.mean() for averages

from collections import namedtuple
from get_raw_data import get_multi_sets
from helpers import get_week_ends, SOILS


# SOILS = ['ORG', 'MIN', 'UNC']

BasicStats = namedtuple('BasicStats', ['means', 'MRE', 'control', 'means_SE',
                                       'MRE_SE', 'control_SE', 'MRE_SD', 'control_SD', 'difference', 'normalized_diff'])
def get_stats(raw_data):

    # means
    groupby_soil_treatment = raw_data.groupby(level=['treatment', 'soil'],axis=1)  # group 4 replicates from every soil-treatment pair
    means = groupby_soil_treatment.mean()  # means of 4 replicates
    means_SD = groupby_soil_treatment.std() # std deviation
    means_SE = groupby_soil_treatment.sem()  # std error

    # means of control\MRE-treatment
    MRE = means.xs('t', level=0, axis=1)
    MRE_SD = means_SD.xs('t', level=0, axis=1)
    MRE_SE = means_SE.xs('t', level=0, axis=1)
    MRE.treatment_label = 't'
    control = means.xs('c', level=0, axis=1)
    control_SE = means_SE.xs('c', level=0, axis=1)
    control_SD = means_SD.xs('c', level=0, axis=1)
    control.treatment_label = 'c'

    #treatment effect
    difference = MRE - control   # treatment - control
    normalized_diff = difference / control * 100  # difference normalized to control (percent)

    return BasicStats(means=means, MRE=MRE, control=control, means_SE=means_SE, MRE_SE=MRE_SE,
                                       control_SE=control_SE, MRE_SD=MRE_SD, control_SD=control_SD,
                                            difference=difference, normalized_diff=normalized_diff)


def get_baseline(raw_data):
    """get the mean and std error of control samples of each soil, excluding week days. """

    raw_data_control = raw_data.loc[get_week_ends(raw_data), ('c', SOILS)]  # week ends control samples from raw data
    raw_data_control.columns = raw_data_control.columns.droplevel('treatment')
    control_stacked = raw_data_control.stack(level='replicate')

    means = control_stacked.mean().reindex(SOILS)
    means_SD = control_stacked.std()
    means_SE = control_stacked.sem()

    return means, means_SD, means_SE


def get_carbon_stats():

    sets_names = ['MBC', 'MBN', 'RESP', 'DOC', 'HWS','TOC']
    dataframes = get_multi_sets(sets_names)
    stats_frames = {}
    for set in sets_names:
        raw = dataframes[set]
        stats = get_stats(raw)
        means = stats.means
        means_SE = stats.means_SE
        set_stats = {'means': means, 'means_SE': means_SE}
        stats_frames[set] = set_stats

    MBC = stats_frames['MBC']['means']
    MBN = stats_frames['MBN']['means']
    RESP = stats_frames['RESP']['means']
    DOC = stats_frames['DOC']['means']
    HWES = stats_frames['HWS']['means']
    HWES_C = HWES / 4  # 40% C in glucose
    C_to_N_ratio = MBC / MBN
    C_to_N_ratio = C_to_N_ratio.loc[get_week_ends(C_to_N_ratio)]
    # soil_available_C = MBC + HWES_C + DOC
    # available_C_control = available_C.xs(key='c', level=0, axis=1)
    # available_C_MRE = available_C.xs(key='t', level=0, axis=1)
    # available_C_difference = available_C_MRE- available_C_control # todo plot available_c and available_C_difference

    return C_to_N_ratio


