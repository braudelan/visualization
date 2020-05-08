# todo compute stde

from pandas import DataFrame, MultiIndex

from data.raw_data import get_raw_data
from data.stats import get_stats
from data.helpers import *

SOILS = Constants.LTTs

#raw data
RAW_DATA = get_raw_data('Resp')

# limits of time intervals between samplings
timepoints = RAW_DATA.index.values
n_intervals = len(timepoints) - 1
INTERVALS_LIST = [[timepoints[i], timepoints[i + 1]] for i in range(n_intervals)] # a list of intervals start and end (i.e [0, 2] for the interval between incubation start and 2 h)
intervals_arrayed = numpy.asarray(INTERVALS_LIST)
intervals = intervals_arrayed.T  # array.shape-->(2, len(SAMPLING_TIMEPOINTS))
BEGININGS = intervals[0]
ENDINGS = intervals[1]
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
    n_intervals_first = 5 # number of intervals in the 1st week
    n_intervals_second = 6 # same as above for 2nd week
    n_intervals_third = 5 # dito
    weeks = [1]*n_intervals_first + [2]*n_intervals_second + [3]*n_intervals_third
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
    RESP_stats = get_stats(RAW_DATA, treatment)
    RESP_means = RESP_stats.means
    RESP_stde = RESP_stats.stde

    for soil in SOILS:
        soil_respiration = RESP_means[soil]
        soil_stde = RESP_stde[soil]

        mean_rates = []
        stnd_errors = []
        for interval in INTERVALS_LIST:

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


def get_daily_respiration(treatment):

    rates = get_mean_rates(treatment)
    mean_rates = rates.means
    rates_stde = rates.stde

    # daily CO2
    daily_cumulative = mean_rates.mul(SAMPLING_INTERVALS,
                                             axis='rows')  # rate X time
    daily_error = rates_stde.mul(SAMPLING_INTERVALS,
                                             axis='rows')  # multiply stnd error by the same constant(i.e. time)

    return Stats(
        means=daily_cumulative,
        stde=daily_error
    )


def get_weekly_respiration(treatment):
    ''' get total respiration for each week.'''

    daily_cumulative = get_daily_respiration(treatment)
    daily_mean = daily_cumulative.means
    daily_error = daily_cumulative.stde

    grouped_by_week = daily_mean.groupby(level='week')
    weekly_respiration = grouped_by_week.sum()

    # stnd error by week
    daily_error_squared = daily_error ** 2
    grouped_by_week = (daily_error_squared).groupby('week')
    sumed = grouped_by_week.sum()
    weekly_respiration_error = sumed ** 0.5

    return Stats(
        means=weekly_respiration,
        stde=weekly_respiration_error
    )


def get_cumulative_respiration(treatment):

    daily_cumulative = get_daily_respiration(treatment)
    daily_mean = daily_cumulative.means
    daily_error = daily_cumulative.stde

    # compute cumulative CO2 for every sampling day
    cumulative_respiration = daily_mean.apply(
        get_cumulative_sum,
        axis='index',
        raw=True,
    )
    cumulative_error = daily_error.apply(
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


