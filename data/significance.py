from pandas import DataFrame, Series
from statsmodels.stats.multicomp import MultiComparison
from scipy.stats import ttest_ind

from data.helpers import replace_nan_with_mean
import constants

# DATA_SETS_NAMES = get_setup_arguments()
# OUTPUT_PATH = '/home/elan/Dropbox/research/figures/significance/'
# TABLE_FORMATING_SCRIPT = constants.table_css

SOILS = constants.LONG_TERM_TREATMENTS
TREATMENTS = constants.treatment_labels
COLUMNS_LEVELS = constants.level_names


def get_significance_booleans(data):
    '''
    preform multiple comparisons (t-tests).

    paramters
    ---------
    data: Series
        must have a single level index containing the group labels (id).
        values are the results to be compared

    returns
    ------
    booleans: Series
         boolean values indicating significance between the groups.
    '''

    id = data.index.values
    value = data.values

    # multiple comparison
    multiple_comparisons = MultiComparison(value, id)  # instanciate multiple comparisons object
    pairwise_holm = multiple_comparisons.allpairtest(ttest_ind, method='holm')  # preform pairwise t-test
    significance_matrix = DataFrame(pairwise_holm[2])  # store results in dataframe
    groups_as_index = significance_matrix.set_index(['group1', 'group2'])
    significance_booleans = groups_as_index['reject']

    return significance_booleans


def annotate(booleans, day=None): #todo assign significance letters to match the order of mean values
    '''
     return a Series with letters indicating significance.

    :param booleans:
    DataFrame or Series with booleans indicating significance
    between group pairs.

    :param day:
    if booleans is a DataFrame then day will be the column by
    which it will be sliced.

    :return:
    a Series with groups(soils) as ndex.
    values are significance letters.
    '''

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

    # letters
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


def daily_significance_between_soils(
        raw_data, treatment=None)-> DataFrame:
    '''
    compute significance between LTTs for each sampling event (=day)..

    :param raw_data: DataFrame
    raw data with 'treatment' level dropped.

    :param treatment:
    if raw_data is not normalized, decides whether control
     or treated samples data will be used.

    :return:

    '''
    def find_missing_days(dataframe) -> list:
        '''
        return a list of days where there was missing data.

        any day where there was any Long Term Treatment
         for which there was no data at all on that specific day.
        '''
    
        days_missing_data = []
        days = dataframe.index
        for soil in SOILS:
            soil_mask = [day for day in days if
                                dataframe.loc[day, soil].isnull().all()]
            days_missing_data.extend(soil_mask)

        return days_missing_data

    def get_daily_data(data, day):
        """
        get the raw data of a given sampling day.

        :parameter data: DataFrame
        raw_data

        :returns daily_data: Series
        index values are Long Term Treatments (soils)
        """
        stacked_data = data.stack()
        sliced_by_day = stacked_data.loc[day]
        daily_data = sliced_by_day.stack()
        daily_data = daily_data.droplevel('replicate')

        return daily_data

    # handle missing data
    raw_data = raw_data.dropna(how='all')
    raw_data = raw_data.drop(find_missing_days(raw_data))
    raw_data = replace_nan_with_mean(raw_data)

    days = raw_data.index

    # dataframe to store significance by letters
    letters_index_label = 'soil'
    letters_columms_label = 'day of incubation'
    letters_index = ['MIN', 'ORG', 'UNC']
    letters = DataFrame(index=letters_index,
                        columns=days)
    letters.rename_axis(index=letters_index_label,
                        columns=letters_columms_label, inplace=True)

    for day in days:

        daily_data = get_daily_data(raw_data, day)
        booleans = get_significance_booleans(daily_data)

        # get anotation letters and insert them into letters dataframe
        significance_letters = annotate(booleans)
        letters[day] = significance_letters

    return letters

#
# def visualize_daily_significance(raw_data: DataFrame,
#         data_set_name: str, format_by, output_dir, label: str = None):
#
#     '''
#     create and save a table image with significance letters.
#
#     table columns are the sampling days.
#     the rows are the groups between which significance
#      is computed.
#
#     parameters
#     ----------
#     raw_data: DataFrame
#         the input data to compute significance for.
#
#     data_set_name: str
#         name of the parameter for which daily significance
#         is computed.
#
#
#     format_by: css file
#         css file by which the output table is formatted.
#
#     output_dir: path
#         where to place the output image.
#
#     label: str
#         meta data about the kind of data manipulation
#         preformed on the raw data.
#     '''
#
#     significance = daily_significance_between_soils(raw_data)
#     output_file = f'{output_dir}{data_set_name}_{label}'
#     DataFrame_to_image(significance, format_by, output_file)
#

