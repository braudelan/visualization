import pandas
from matplotlib import pyplot

from raw_data     import get_keys, get_raw_data
from stats        import get_stats, plot_stats
from baseline     import get_baseline, plot_baseline
from control      import plot_control
from Ttest        import get_daily_Ttest, tabulate_daily_Ttest
from growth       import get_weekly_growth, tabulate_growth


# set pyplot parameters
pyplot.rc('savefig', bbox='tight', pad_inches=1.5)

INPUT_FILE = "all_tests.xlsx"

# arguments to specify which data sets to load from INPUT_FILE
keys_output = get_keys()
if type(keys_output) != tuple:
    KEYS    = get_keys().specific
    NUMBERS = get_keys().numbers
else:
    KEYS    = get_keys()[0]
    NUMBERS = get_keys()[1]


baseline_dict = {}
for key, number in zip(KEYS, NUMBERS):

# input data into DataFrame
    raw_data = get_raw_data(key)

# get general statistics
    means, normalized, means_stde, difference = get_stats(raw_data)

# plot means and normalized means(effect)
    general_stats_fig = plot_stats(means, normalized, means_stde, number, key)
    general_stats_fig.savefig("./figures/%s_figuers.png" % key, )
    pyplot.cla()

# # plot control
#     control_means_fig = plot_control(means, means_stde, key, number)
#     control_means_fig.savefig('./control_figures/%s.png' % key)
#     pyplot.cla()

# # plot ttest table
#     daily_ttest = get_daily_Ttest(raw_data)
#     ttest_table = tabulate_daily_Ttest(daily_ttest, key)
#     ttest_table.savefig("./figures/%s_Ttest.png" % key, bbox_inches='tight')
#     pyplot.cla()

# # plot weekly growth table
#     if test != 'RESP':
#         weekly_growth = get_weekly_growth(means)
#         growth_table = tabulate_growth(weekly_growth, number, test)
#         growth_table.savefig("./figures/%s_growth.png" % test, bbox_inches='tight')
#         pyplot.clf()


# # baseline dataframe
# baseline = get_baseline(KEYS)
# plot_baseline(baseline)