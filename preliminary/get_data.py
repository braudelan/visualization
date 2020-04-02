import pdb

import pandas
from pandas import DataFrame
from pandas import MultiIndex

from preliminary.constants import *
from data.helpers import *

LTTs = ['ORG', 'MIN']


def get_raw_data(data_name):

    # data set into DataFrame
    raw_data = pandas.read_excel(INPUT_FILE_PATH,
                                 index_col=[0, 1, 2],header=1,
                                 sheet_name=data_name)

    index_names =  ['LTT', 'STT', 'replicate']

    # name the index
    raw_data.rename_axis(index_names, inplace=True)
    raw_data.rename_axis('hours of incubation', axis='columns', inplace=True)

    # transpose
    raw_data = raw_data.T

    return raw_data



def get_stats(raw_data, STT: tuple):
    '''
    get statistics for each LTT.

    :param STT: tuple of strings
    which STT to compute statistics for.

    :return: stats
    Stats instance with means and stnd error.

    '''

    # slice Short Term Treatment

    raw_data = raw_data.loc[:, (slice(None), STT)].droplevel('STT', axis='columns')

    # get_statistics
    group_by_LTT = raw_data.groupby(level='LTT', axis=1)
    means = group_by_LTT.mean()
    stde = group_by_LTT.sem()

    return Stats(
        means=means,
        stde=stde,
    )

#------------------------------------------- cumulative respiration -----------------------------------

# get respiration raw data
RAW_DATA = get_raw_data('RESP')

# limits of time intervals between samplings
timepoints = RAW_DATA.index.values
n_intervals = len(timepoints) - 1
INTERVALS = [[timepoints[i], timepoints[i + 1]] for i in range(
    n_intervals)]  # a list of intervals start and end (i.e [0, 2] for the interval between incubation start and 2 h)
intervals_arrayed = numpy.asarray(INTERVALS)
interval_limits = intervals_arrayed.T  # array.shape-->(2, len(SAMPLING_TIMEPOINTS))
BEGININGS = interval_limits[0]
ENDINGS = interval_limits[1]
INTERVALS_TIME = ENDINGS - BEGININGS # intervals time in hours


def get_mean_rates(STT):
    '''
    get average rate between every two consecutive sampling points.

    :param raw_data: DataFrame

    :param STT: tuple of strings
    'control', 'starw', 'compost' or any combination of these.

    :return: class Stats
    mean respiration rates averaged between each two consecutive
    sampling points.
    '''

    # frame for mean rates
    levels = [
        # weeks,
        BEGININGS,
        ENDINGS,
    ]
    names = [
        # 'week',
        't_initial',
        't_end'
    ]
    multi_index = MultiIndex.from_arrays(
        arrays=levels, names=names)
    respiration_rates = DataFrame(
        index=multi_index, columns=LTTs)
    rates_stnd_errors = DataFrame(
        index=multi_index, columns=LTTs)

    # data
    RESP_stats = get_stats(RAW_DATA, STT)
    RESP_means = RESP_stats.means
    RESP_stde = RESP_stats.stde

    for soil in LTTs:
        soil_respiration = RESP_means[soil]
        soil_stde = RESP_stde[soil]

        mean_rates = []
        stnd_errors = []
        for interval in INTERVALS:
            t_initial = interval[0]
            t_end = interval[1]

            t_initial_means = soil_respiration.loc[t_initial]
            t_initial_stde = soil_stde.loc[t_initial]
            t_end_means = soil_respiration.loc[t_end]
            t_end_stde = soil_stde.loc[t_end]

            mean = (t_initial_means + t_end_means) / 2
            stde = (t_initial_stde ** 2 + t_end_stde ** 2) ** 0.5 / 2

            mean_rates.append(mean)
            stnd_errors.append(stde)

        respiration_rates[soil] = mean_rates
        rates_stnd_errors[soil] = stnd_errors

    return Stats(
        means=respiration_rates,
        stde=rates_stnd_errors
    )


def get_daily_respiration(STT):

    rates = get_mean_rates(STT)
    mean_rates = rates.means
    rates_stde = rates.stde

    # daily CO2
    daily_respiration = mean_rates.mul(INTERVALS_TIME / 24,
                                       axis='rows')  # rate X time (in days)
    daily_error = rates_stde.mul(INTERVALS_TIME / 24,
                                 axis='rows')  # multiply stnd error by the same constant(i.e. time)

    return Stats(
        means=daily_respiration,
        stde=daily_error
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
    cumulative_respiration = cumulative_respiration.droplevel(0).rename_axis('hours')
    cumulative_error = cumulative_error.droplevel(0).rename_axis('hours')

    return  Stats(
        means=cumulative_respiration,
        stde=cumulative_error,
    )
