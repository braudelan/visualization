import pdb
import numpy
from pandas import DataFrame, Series, MultiIndex
from statsmodels.stats.multicomp import MultiComparison, pairwise_tukeyhsd
from scipy.stats import ttest_ind

from raw_data import get_setup_arguments, get_raw_data, get_multi_sets
from stats import get_stats, subtract_control, subtract_baseline
from helpers import Constants, replace_None, get_week_ends

OUTPUT_PATH = '/home/elan/Dropbox/research/figures/significance/'
setup_args = get_setup_arguments()
DATA_SETS_NAMES = setup_args.sets

SOILS = Constants.groups
TREATMENTS = Constants.treatment_labels
COLUMNS_LEVELS = Constants.level_labels


def anotate_significance(booleans, day=None):

    # define pairs
    pair_1 = ('MIN', 'ORG')
    pair_2 = ('MIN', 'UNC')
    pair_3 = ('ORG', 'UNC')

    # assign reject/accept boolean value to each pair
    if day is not None:
        MIN_ORG = booleans.loc[pair_1, day]
        MIN_UNC = booleans.loc[pair_2, day]
        ORG_UNC = booleans.loc[pair_3, day]
    else:
        MIN_ORG = booleans.loc[pair_1]
        MIN_UNC = booleans.loc[pair_2]
        ORG_UNC = booleans.loc[pair_3]

    # define the options for significance between the soils
    option_1 = MIN_ORG == False and MIN_UNC == False and ORG_UNC == False  # no difference
    option_2 = MIN_ORG == True and MIN_UNC == True and ORG_UNC == True  # all different
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

    # assign appropriate letter to each soil
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
    anotations = Series(anotations)

    return anotations


def daily_significance_between_soils(raw_data, treatment=None):

    # handle missing data
    if treatment is not None:
      data = raw_data.loc[:, treatment]
    data = raw_data.dropna(how='all')
    data = replace_None(data)


    # dataframe to store booleans rejecting/accepting null hypothesis
    days = data.index
    index_levels = [['MIN', 'MIN', 'ORG'], ['ORG', 'UNC', 'UNC']]
    index_names = numpy.array(['soil_1', 'soil_2'])
    index = MultiIndex.from_arrays(index_levels,
                                   names=index_names)
    significance_booleans = DataFrame(index=index,
                                    columns=days)

    # dataframe to store letters anotating significance
    letters_index_label = 'soil'
    letters_columms_label = 'day of incubation'
    letters_index = ['MIN', 'ORG', 'UNC']
    letters = DataFrame(index=letters_index,
                                        columns=days)
    letters.rename_axis(index=letters_index_label,
                           columns=letters_columms_label, inplace=True)

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
        significance_matrix = DataFrame(pairwise_holm[2])

        # insert reject/accept booleans into dataframe
        reject_accept = significance_matrix['reject'].values
        significance_booleans.loc[:, day] = reject_accept

        # get anotation letters and insert them into letters dataframe
        significance_letters = anotate_significance(significance_booleans, day=day)
        for soil in letters_index:
            letters.loc[soil, day] = significance_letters[soil]

    return letters


def baseline_significance(data_sets_names) -> DataFrame:
    '''
    compute significance between baseline values.

    :parameter
    data_sets_names : list
        names of parameters for which baseline significance
        should be computed.

    :returns

    dataframe
        with letters designating significance
        between baseline values for each data set.
     '''

    def get_data_set_significance(raw_data) -> Series:
        week_ends_control = raw_data.loc[
            get_week_ends(raw_data), ('c', SOILS)]  # week ends control samples from raw data
        stacked = week_ends_control.stack(level=COLUMNS_LEVELS)
        index_reset = stacked.reset_index(level=('days', 'treatment', 'replicate'), drop=True)
        data = index_reset

        id = data.index.values
        values = data.values

        multiple_comparisons = MultiComparison(values, id)
        pairwise_holm = multiple_comparisons.allpairtest(ttest_ind, method='holm')
        significance_matrix = DataFrame(pairwise_holm[2])

        index_levels = [['MIN', 'MIN', 'ORG'], ['ORG', 'UNC', 'UNC']]
        index_names = numpy.array(['soil_1', 'soil_2'])
        index = MultiIndex.from_arrays(index_levels,
                                       names=index_names)
        significance_booleans = Series(index=index)

        # insert reject/accept booleans into dataframe
        reject_accept = significance_matrix['reject'].values
        significance_booleans.loc[:] = reject_accept
        letters = anotate_significance(significance_booleans)

        return letters

    data_sets = get_multi_sets(data_sets_names)

    index = SOILS
    columns = data_sets_names
    baseline_letters = DataFrame(index=index, columns=columns)
    for name, data in data_sets.items():
        significance = get_data_set_significance(data)
        baseline_letters[name] = significance

    return baseline_letters

if __name__ == '__main__':
    raw_data = get_raw_data("HWS")
    control_subtracted = subtract_control(raw_data)
    baseline_subtracted = subtract_baseline(raw_data)

    data_sets = {'control': control_subtracted, 'baseline': baseline_subtracted}
    for name, data_set in data_sets.items():

        significance_matrix = daily_significance_between_soils(data_set)

        print(f'{name}: {significance_matrix}')
