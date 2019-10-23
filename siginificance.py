import pdb
from pandas import DataFrame
from statsmodels.stats.multicomp import MultiComparison, pairwise_tukeyhsd
from scipy.stats import ttest_ind

from raw_data import get_setup_arguments, get_raw_data
from stats import get_stats, normalize_to_control, normalize_to_baseline
from helpers import Constants, replace_nan

OUTPUT_PATH = '/home/elan/Dropbox/research/figures/significance/'
setup_args = get_setup_arguments()

SOILS = Constants.groups

def significance_between_soils(raw_data):


    data = replace_nan(raw_data, 't')
    data.set_index('days', inplace=True)
    days = data.index
    index = Constants.groups
    columns = days
    significance = DataFrame(index=index, columns=columns)

    data = {}
    for day in days:
        daily_data = data.loc[day]
        daily_data = daily_data.droplevel(1)

        for soil in SOILS:
            soil_data = daily_data[soil].values
            data[soil] = soil_data

    pdb.set_trace()

        # # multiple comparisons objects
        # multiple_comparisons = MultiComparison(response_var, id)
        # pairwise_holm = multiple_comparisons.allpairtest(ttest_ind, method='holm')

if __name__ == '__main__':

    significance_between_soils('MBC')