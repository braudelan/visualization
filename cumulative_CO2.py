# todo compute stde

import pdb
from collections import namedtuple
import numpy
from pandas import DataFrame, MultiIndex

from raw_data import get_raw_data
from stats import get_stats
from helpers import *

SOILS = Constants.groups

#--------------------------------------weekly cumulative CO2------------------------------
#raw data
raw_data = get_raw_data('RESP')

# limits of time intervals between samplings
SAMPLING_TIMEPOINTS = raw_data.index.values
timepoints_index = [i for i in range(8)]
interval_list = [[SAMPLING_TIMEPOINTS[i], SAMPLING_TIMEPOINTS[i + 1]] for i in timepoints_index]
intervals_arrayed = numpy.asarray(interval_list)
INTERVALS = intervals_arrayed.T  # array.shape-->(2, len(SAMPLING_TIMEPOINTS))
BEGININGS = INTERVALS[0]
ENDINGS = INTERVALS[1]
SAMPLING_INTERVALS = ENDINGS- BEGININGS


def get_mean_rates(treatment):
    '''
    get average rate between every two consecutive sampling points.

    :param treatment: str
    either 't'(MRE treated) or 'c' for control.
    designates which treatment to slice out.

    :return: class Stats
    mean respiration rates averaged between each two consecutive
    sampling points.
    '''

    # empty dataframes to store results
    weeks = [1, 1, 1, 2, 2, 2, 3, 3]
    levels = [
        weeks,
        BEGININGS,
        ENDINGS,
    ]
    names = [
        'week',
        't_initial',
        't_end'
    ]
    multi_index = MultiIndex.from_arrays(
                    arrays=levels, names=names)
    respiration_rates = DataFrame(
                index=multi_index, columns=SOILS)
    rates_stnd_errors = DataFrame(
                index=multi_index, columns=SOILS)

    # data
    RESP_stats = get_stats(raw_data, treatment)
    RESP_means = RESP_stats.means
    RESP_stde = RESP_stats.stde

    for soil in SOILS:
        soil_respiration = RESP_means[soil]
        soil_stde = RESP_stde[soil]

        mean_rates = []
        stnd_errors = []
        for interval in interval_list:

            t_initial = interval[0]
            t_end = interval[1]

            t_initial_means = soil_respiration.loc[t_initial]
            t_initial_stde = soil_stde.loc[t_initial]
            t_end_means = soil_respiration.loc[t_end]
            t_end_stde = soil_stde.loc[t_end]

            mean = (t_initial_means + t_end_means) / 2
            stde = (t_initial_stde**2 + t_end_stde**2)**0.5 / 2

            mean_rates.append(mean)
            stnd_errors.append(stde)

        respiration_rates[soil] = mean_rates
        rates_stnd_errors[soil] = stnd_errors

    return Stats(
        means=respiration_rates,
        stde=rates_stnd_errors
    )

def get_cumulative_respiration(treatment):

    mean_rates = get_mean_rates(treatment)
    means = mean_rates.means
    stde = mean_rates.stde

    # weekly CO2
    mean_amounts = means.mul(SAMPLING_INTERVALS, axis='rows')  # rate X time
    stde_amounts = stde.mul(SAMPLING_INTERVALS, axis='rows')  # multiply stnd error by the same constant(i.e. time)

    # compute cumulative CO2 for every sampling day
    cumulative_respiration = mean_amounts.apply(
        get_cumulative_sum,
        axis='index',
        raw=True,
    )
    cumulative_error = stde_amounts.apply(
        get_cumulative_error,
        axis='index',
        raw=True,
    )
    cumulative_respiration = cumulative_respiration.droplevel([0,1]).rename_axis('day')
    cumulative_error = cumulative_error.droplevel([0,1]).rename_axis('day')

    return  Stats(
        means=cumulative_respiration,
        stde=cumulative_error,
    )


def get_weekly_respiration(mean_rates):
    ''' get cumulative respiration for each week.'''

    cumulative = get_cumulative_respiration(mean_rates)
    cumulative_means = cumulative.means
    cumulative_stde = cumulative.stde

    cumulative_by_week = cumulative_means.groupby(level='week')
    weekly_CO2 = cumulative_by_week.sum()

    # stnd error by week
    cumulative_stde_squared = cumulative_stde ** 2
    grouped_by_week = (cumulative_stde_squared).groupby('week')
    sumed = grouped_by_week.sum()
    weekly_CO2_stde = sumed ** 0.5
    relative_CO2_stde = weekly_CO2_stde

    return MEANS(
        means=weekly_CO2,
        stde=relative_CO2_stde
    )

if __name__ == '__main__':
    mean_rates = get_mean_rates('t')
    weekly_cumulative = get_weekly_respiration(mean_rates)

#--------------------------------------weekly MBC growth------------------------------------------
# # MBC raw data
# MBC_raw_data: DataFrame = get_raw_data('MBC')
#
# # rearange data
# week_ends = get_week_ends(MBC_raw_data)
# MBC_raw_data = MBC_raw_data.loc[week_ends]
#
# MBC_stats = get_stats(MBC_raw_data, 'c')
# MBC_means = MBC_stats.means
# MBC_means = MBC_means.iloc[:-1] # drop last week end
# MBC_stde = MBC_stats.stde
# MBC_stde = MBC_stde.iloc[:-1] # drop last week end
#
# # week beginings
# MBC_starts = MBC_means.iloc[:-1]
# MBC_starts_stde = MBC_stde.iloc[:-1]
# starts_squared = MBC_starts_stde**2
#
# # week ends
# MBC_ends = MBC_means.iloc[1:]
# MBC_ends_stde = MBC_stde.iloc[1:]
# ends_squared = MBC_ends_stde**2
#
# # change index to a range index
# frames_to_change_index = [
#                             MBC_starts,
#                             MBC_starts_stde,
#                             MBC_ends,
#                             MBC_ends_stde
#                       ]
# new_index = [1, 2, 3] # weeks
#
# for dataframe in frames_to_change_index:
#     dataframe.set_axis(new_index, inplace=True)
#
# weekly_growth = MBC_ends - MBC_starts
# weekly_growth_stde = (MBC_starts_stde**2 + MBC_ends_stde**2)**0.5
# relative_growth_stde = weekly_growth_stde / weekly_growth
#
# # -------------------------------------weekly metabolic quotient-----------------------------------------
# # respiration data
# RESP_raw_data = get_raw_data('RESP')
# RESP_stats = get_stats(RESP_raw_data, 'c')
#
# mean_respiration_rates = get_mean_rates()
# weekly_CO2 = get_weekly_cumulative(mean_respiration_rates)
# weekly_CO2_means = weekly_CO2.means
# weekly_CO2_stde = weekly_CO2.stde
# weekly_quotient = weekly_CO2_means / weekly_growth
# weekly_quotient_stde = propagate_stde(weekly_quotient, weekly_CO2_stde,
#                                       relative_growth_stde)
#
# if __name__ == '__main__':
#     averaged = get_mean_rates()