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

def significance_between_soils(data_set_name):

    raw_data: DataFrame = get_raw_data(data_set_name)
    normalized_raw = normalize_to_control(raw_data)
    normalized_raw = replace_nan(normalized_raw, 't')
    normalized_raw.set_index('days', inplace=True)

    days = normalized_raw.index

    index = Constants.groups
    columns = days
    significance = DataFrame(index=index, columns=columns)

    data = {}
    for day in days:
        daily_data = normalized_raw.loc[day]
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