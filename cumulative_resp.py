import pdb
import numpy
from pandas import DataFrame

from raw_data import get_raw_data
from stats import get_stats
from helpers import Constants

SOILS = Constants.groups

def cumulative_co2():
    raw_data = get_raw_data('RESP')
    stats = get_stats(raw_data, 't')
    means = stats.means
    stde = stats.stde

    timepoints = means.index.values
    timepoints_index = [i for i in range(8)]
    intervals = [[timepoints[i], timepoints[i + 1]] for i in timepoints_index]

    respiration_rates = DataFrame(index = intervals , columns=SOILS)
    rates_stnd_errors = DataFrame(index = intervals , columns=SOILS)
    for soil in SOILS:
        data = means[soil]
        data_stde = stde[soil]

        rates = []
        stnd_errors = []
        i = 0
        for interval_limits in intervals:

            t_initial = interval_limits[0]
            t_end = interval_limits[1]

            t_initial_means = data.loc[t_initial]
            t_initial_stde = data_stde.loc[t_initial]
            t_end_means = data.loc[t_end]
            t_end_stde = data_stde.loc[t_end]

            average = (t_initial_means + t_end_means) / 2
            average_stde = (t_initial_stde**2 + t_end_stde**2)**0.5

            rates.append(average)
            stnd_errors.append(average_stde)
            i += 1
            pdb.set_trace()
        respiration_rates[soil] = rates
        rates_stnd_errors[soil] = stnd_errors

    return respiration_rates, rates_stnd_errors

if __name__ == '__main__':
    averaged = cumulative_co2()