import pdb
from pandas import DataFrame
from statsmodels.stats.multicomp import MultiComparison, pairwise_tukeyhsd
from scipy.stats import ttest_ind

from raw_data import get_setup_arguments, get_raw_data
from stats import get_stats, normalize_raw_data
from growth import get_weekly_growth, tabulate_growth
from helpers import Constants, replace_nan

OUTPUT_PATH = '/home/elan/Dropbox/research/figures/significance/'
setup_args = get_setup_arguments()

data_sets_names = setup_args.sets

for name in data_sets_names:

    raw: DataFrame = get_raw_data(name)
    norm_raw = normalize_raw_data(raw)
    norm_raw = replace_nan(norm_raw, 't')
    norm_raw.set_index('days', inplace=True)

    days = norm_raw.index

    for day in days:

        # organize the data
        data = norm_raw.loc[day]
        data = data.droplevel(1)
        id = data.index
        response_var = data.values

        # multiple comparisons objects
        multiple_comparisons = MultiComparison(response_var, id)
        pairwise_holm = multiple_comparisons.allpairtest(ttest_ind, method='holm')
        pairwise_tukey = pairwise_tukeyhsd(response_var, id)

        # multiple comparisons results
        tukey_result = str(pairwise_tukey._results_table)
        holm_result = str(pairwise_holm[0])

        # open the file
        file_path = OUTPUT_PATH + name + '_significance.txt'
        mode_string = 'w+' if day == 0 else 'a'
        open_file = open(file_path, mode_string)

        # write results into file
        tukey_table_width = tukey_result.find('\n')
        day_title = '\n\nday ' + str(day) + ':\n\n'
        open_file.write(day_title + tukey_result)


        # print(str(day), str(multi_comparisons._results_table))

