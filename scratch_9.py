from pandas import DataFrame
from statsmodels.stats.multicomp import pairwise_tukeyhsd

from raw_data import get_setup_arguments, get_raw_data
from stats import get_stats, normalize_raw_data
from growth import get_weekly_growth, tabulate_growth
from helpers import Constants, replace_nan

OUTPUT_FOLDER =Constants.output_folder

setup_args = get_setup_arguments()

data_sets_names = setup_args.sets[0]
#
# for number, name in enumerate(data_sets_names):
#
#     raw = get_raw_data(name)
#     stats = get_stats(raw, 't')
#     normelized_stats = get_normalized(raw)
#     normalized_means = normelized_stats.means
#     normalized_stde = normelized_stats.stde
#     weekly_growth_norm = get_weekly_growth(normalized_means, normalized_stde)
#
#     growth_table = tabulate_growth(weekly_growth_norm, name, number)
#     growth_table.savefig('%s/%s_weekly_growth.png' %(OUTPUT_FOLDER, name))

raw: DataFrame = get_raw_data(data_sets_names)
norm_raw = normalize_raw_data(raw)
norm_raw = replace_nan(norm_raw, 't')
norm_raw.set_index('days', inplace=True)
#
# stats = get_stats(raw, 't')
# norm_stats = get_stats(norm_raw, 't')
#
# means = stats.means
# stde = stats.stde
#
# norm_means = norm_stats.means
# norm_stde = norm_stats.stde

days = norm_raw.index

for day in days:

    data = norm_raw.loc[day]
    data = data.droplevel(1)

    id = data.index
    response_var = data.values

    multi_comparisons = pairwise_tukeyhsd(response_var, id)

    print(str(day), str(multi_comparisons._results_table))

