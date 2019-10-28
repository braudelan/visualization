import pdb
import pandas
from pandas import DataFrame
from statsmodels.stats.multicomp import MultiComparison, pairwise_tukeyhsd
from scipy.stats import ttest_ind

from raw_data import get_setup_arguments, get_raw_data
from stats import get_stats, normalize_to_control, normalize_to_baseline
from helpers import Constants, replace_None

OUTPUT_PATH = '/home/elan/Dropbox/research/figures/significance/'
setup_args = get_setup_arguments()

SOILS = Constants.groups
TREATMENTS = Constants.treatment_labels

def significance_between_soils(raw_data):

    data = replace_None(raw_data)
    data = data.drop(8)
    days = data.index

    # create empty datarame to store results
    # index_levels = [['MIN', 'MIN', 'ORG'], ['ORG', 'UNC', 'UNC']]
    # multiindex = pandas.MultiIndex(index_levels,
    #                                 names=['group1', 'group2'])
    index = ['MIN-ORG', 'MIN-UNC', 'ORG-UNC']
    columns_levels = [days, ['pval', 'pval_corr', 'reject']]
    columns_multiindex = pandas.MultiIndex(levels=columns_levels, codes=[0,0]
                                    names=['days', 'ttest_stats'])
    significance = DataFrame(index=index, columns=columns_multiindex)

    index = Constants.groups
    columns = days

    # pdb.set_trace()

    treatments_dict = {}
    days_dict = {}
    for treatment in TREATMENTS:
        for day in days:
            treatment_data = data[treatment]
            stacked_data = treatment_data.stack()
            sliced_by_day = stacked_data.loc[day]
            daily_data = sliced_by_day.stack()
            daily_data = daily_data.droplevel('replicate')
            result = daily_data.values
            id = daily_data.index.values

            # multiple comparisons objects
            multiple_comparisons = MultiComparison(result, id)
            pairwise_holm = multiple_comparisons.allpairtest(ttest_ind, method='holm')
            significance_matrix = DataFrame(pairwise_holm[2])
            ttest_stats = significance_matrix.loc[:, 'pval':]
            daily_significance = significance.loc[:, day]
            daily_significance = ttest_stats.values

    return significance

if __name__ == '__main__':
    raw_data = get_raw_data("MBC")
    significance = significance_between_soils(raw_data)