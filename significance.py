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

def significance_between_soils(raw_data, treatment):

    data = replace_None(raw_data)
    data = data.loc[:, treatment]
    data = data.dropna(how='all')
    days = data.index

    columns = days
    index_levels = [['MIN', 'MIN', 'ORG'], ['ORG', 'UNC', 'UNC']]
    index_names = ['soil_1', 'soil_2']
    index = MultiIndex.from_arrays(index_levels, names=index_names)
    significance = DataFrame(index=index, columns=columns)

    # dataframe with soils anotated for significance
    anotations_index_label = 'soil'
    anotations_columms_label = 'days into incubation'
    anotations_index = ['MIN', 'ORG', 'UNC']
    anotations = DataFrame(index=anotations_index,
                                        columns=columns)
    anotations.rename_axis(index=anotations_index_label,
                           columns=anotations_columms_label, inplace=True)

    pair_1 = ('MIN', 'ORG')
    pair_2 = ('MIN', 'UNC')
    pair_3 = ('ORG', 'UNC')

    def anotate_significance(day):
        MIN_ORG = significance.loc[pair_1, day]
        MIN_UNC = significance.loc[pair_2, day]
        ORG_UNC = significance.loc[pair_3, day]

        option_1 = MIN_ORG == False and MIN_UNC == False and ORG_UNC == False # no difference
        option_2 = MIN_ORG == True and MIN_UNC == True and ORG_UNC == True # all different
        option_3 = MIN_ORG == True and MIN_UNC == True and ORG_UNC == False
        option_4 = MIN_ORG == True and MIN_UNC == False and ORG_UNC == False
        option_5 = MIN_ORG == True and MIN_UNC == False and ORG_UNC == True
        option_6 = MIN_ORG == False and MIN_UNC == True and ORG_UNC == True
        option_7 = MIN_ORG == False and MIN_UNC == False and ORG_UNC == True
        option_8 = MIN_ORG == False and MIN_UNC == True and ORG_UNC == False

        a = 'A'
        b = 'B'
        c = 'C'
        ab = 'AB'

        MIN, ORG, UNC = (
                            (a, a, a) if option_1 else
                            (a, b, c) if option_2 else
                            (a, b, b) if option_3 else
                            (a, b, ab) if option_4 else
                            (a, b, a) if option_5 else
                            (a, a, b) if option_6 else
                            (ab, a, b) if option_7 else
                            (a, ab, b)
            )

        anotations = {'MIN': MIN, 'ORG': ORG, 'UNC': UNC}

        return anotations

    for day in days:
        stacked_data = data.stack()
        sliced_by_day = stacked_data.loc[day]
        daily_data = sliced_by_day.stack()
        daily_data = daily_data.droplevel('replicate')
        result = daily_data.values
        id = daily_data.index.values

        # multiple comparisons objects
        multiple_comparisons = MultiComparison(result, id)
        pairwise_holm = multiple_comparisons.allpairtest(ttest_ind, method='holm')
        # pdb.set_trace()

        # insert ttest results into dataframe
        significance_matrix = DataFrame(pairwise_holm[2])
        ttest_results = significance_matrix['reject'].values
        if day == 15:
            significance.iloc[0,6]
        else:
            significance.loc[:, day] = ttest_results
        print(significance)

        # significance notation table
        daily_anotations = anotate_significance(day)
        for soil in anotations_index:
            anotations.loc[soil, day] = daily_anotations[soil]


    return anotations

if __name__ == '__main__':
    raw_data = get_raw_data("MBC")
    significance = significance_between_soils(raw_data, 't')

