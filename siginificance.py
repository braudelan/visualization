import pdb
from pandas import DataFrame, MultiIndex
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
    # multiindexs
    columns_level_0 = days
    columns_level_1 = ['pval', 'pval_corr', 'reject']
    columns_index_levels = [columns_level_0, columns_level_1]
    columns_index_names = ['days', 'ttest_stats']
    columns_multiindex = MultiIndex.from_product(columns_index_levels,
                                                        names=columns_index_names)
    index_levels = [['MIN', 'MIN', 'ORG'], ['ORG', 'UNC', 'UNC']]
    index_names = ['soil_1', 'soil_2']
    multiindex = MultiIndex.from_arrays(index_levels, names=index_names)
    significance = DataFrame(index=multiindex, columns=columns_multiindex)

    pair_1 = significance.index[0]
    pair_2 = significance.index[1]
    pair_3 = significance.index[2]

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

            # insert ttest results into dataframe
            significance_matrix = DataFrame(pairwise_holm[2])
            ttest_stats = significance_matrix.loc[:, 'pval':].values
            significance.loc[:, (day, columns_level_1)] = ttest_stats

            # significance notation table
            # pair_1_result = significance.loc[pair_1, (0, 'reject')]


    return significance

if __name__ == '__main__':
    raw_data = get_raw_data("MBC")
    significance = significance_between_soils(raw_data)