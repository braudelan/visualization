# todo compute stde

import pdb
import numpy
from pandas import DataFrame, MultiIndex

from raw_data import get_raw_data
from stats import get_stats
from helpers import Constants, get_week_ends, propagate_stde

SOILS = Constants.groups

#--------------------------------------weekly cumulative CO2------------------------------
# respiration data
RESP_raw_data = get_raw_data('RESP')
RESP_stats = get_stats(RESP_raw_data, 'c')
RESP_means = RESP_stats.means
RESP_stde = RESP_stats.stde

# get the time intervals between samplings
timepoints = RESP_means.index.values
timepoints_index = [i for i in range(8)]
intervals_limits = [[timepoints[i], timepoints[i + 1]] for i in timepoints_index]
limits_arrayed = numpy.asarray(intervals_limits)
limits = limits_arrayed.T

# empty dataframes to store results
starts = limits[0]
ends = limits[1]
weeks = [1, 1, 1, 2, 2, 2, 3, 3]
levels = [weeks, starts, ends]
names = ['week', 't_initial', 't_end']
multiindex = MultiIndex.from_arrays(arrays=levels, names=names)
respiration_rates = DataFrame(index=multiindex, columns=SOILS)
rates_stnd_errors = DataFrame(index=multiindex, columns=SOILS)

def mean_CO2_rates():

    for soil in SOILS:
        data = RESP_means[soil]
        data_stde = RESP_stde[soil]

        rates = []
        stnd_errors = []
        i = 0
        for limits in intervals_limits:

            t_initial = limits[0]
            t_end = limits[1]

            t_initial_means = data.loc[t_initial]
            t_initial_stde = data_stde.loc[t_initial]
            t_end_means = data.loc[t_end]
            t_end_stde = data_stde.loc[t_end]

            average = (t_initial_means + t_end_means) / 2
            average_stde = (t_initial_stde**2 + t_end_stde**2)**0.5

            rates.append(average)
            stnd_errors.append(average_stde)
            i += 1
            # pdb.set_trace()
        respiration_rates[soil] = rates
        rates_stnd_errors[soil] = stnd_errors

    return respiration_rates, rates_stnd_errors

# get weekly cumulative CO2 respired
intervals = ends - starts
mean_rates = mean_CO2_rates()[0]
rates_stde = mean_CO2_rates()[1]
cumulative_CO2 = mean_rates.mul(intervals,
                                axis='rows') # rate X time
cumulative_stde = rates_stde.mul(intervals,
                                 axis='rows') # multiply stnd error by the same constant(i.e. time)
cumulative_by_week = cumulative_CO2.groupby(level='week')

cumulative_stde_squared = cumulative_stde ** 2
squared_and_grouped = (cumulative_stde_squared).groupby('week')
grouped_and_sumed = squared_and_grouped.sum()

weekly_CO2 = cumulative_by_week.sum()
weekly_CO2_stde =grouped_and_sumed ** 0.5
relative_CO2_stde = weekly_CO2_stde / weekly_CO2

#--------------------------------------weekly MBC growth------------------------------------------
# MBC raw data
MBC_raw_data: DataFrame = get_raw_data('MBC')

# rearange data
week_ends = get_week_ends(MBC_raw_data)
MBC_raw_data = MBC_raw_data.loc[week_ends]

MBC_stats = get_stats(MBC_raw_data, 'c')
MBC_means = MBC_stats.means
MBC_means = MBC_means.iloc[:-1] # drop last week end
MBC_stde = MBC_stats.stde
MBC_stde = MBC_stde.iloc[:-1] # drop last week end

# week beginings
MBC_starts = MBC_means.iloc[:-1]
MBC_starts_stde = MBC_stde.iloc[:-1]
starts_squared = MBC_starts_stde**2

# week ends
MBC_ends = MBC_means.iloc[1:]
MBC_ends_stde = MBC_stde.iloc[1:]
ends_squared = MBC_ends_stde**2

# change index to a range index
frames_to_change_index = [
                            MBC_starts,
                            MBC_starts_stde,
                            MBC_ends,
                            MBC_ends_stde
                      ]
new_index = [1, 2, 3] # weeks

for dataframe in frames_to_change_index:
    dataframe.set_axis(new_index, inplace=True)

weekly_growth = MBC_ends - MBC_starts
weekly_growth_stde = (MBC_starts_stde**2 + MBC_ends_stde**2)**0.5
relative_growth_stde = weekly_growth_stde / weekly_growth

# -------------------------------------weekly metabolic quotient-----------------------------------------
weekly_qCO2 = weekly_CO2 / weekly_growth
weekly_qCO2_stde = propagate_stde(weekly_qCO2, relative_CO2_stde,
                                                relative_growth_stde)

if __name__ == '__main__':
    averaged = mean_CO2_rates()