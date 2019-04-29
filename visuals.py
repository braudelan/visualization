import pandas
from matplotlib import pyplot

from get_raw_data import get_keys
from get_raw_data import get_single_set
from get_stats    import get_stats
from baseline     import get_baseline, plot_baseline
from plot_stats   import plot_stats
from plot_control import plot_control
from get_Ttest    import get_daily_Ttest
from get_growth import get_weekly_growth
from tabulate_growth import make_growth_table

KEYS, NUMBERS = get_keys()

input_file = "all_tests.xlsx"

baseline_dict = {}


for key, number in zip(KEYS, NUMBERS):

# input data into DataFrame
    raw_data = get_single_set(key)

# get general statistics
    means, effect, means_stde = get_stats(raw_data)

# plot means and normalized means(effect)
    general_stats_fig = plot_stats(means, effect, means_stde, number, key)
    general_stats_fig.savefig("./figures/%s_figuers.png" % key, bbox_inches='tight', pad_inches=2)
    pyplot.cla()

# # plot control
#     control_means_fig = plot_control(control_means, key, number)
#     control_means_fig.savefig('./control_figures/%s.png' % key) #, bbox_inches='tight')
#     pyplot.cla()

# # plot ttest table
#     daily_ttest = get_daily_Ttest(raw_data)[1]
#     ttest_table = tabulate_Ttest(daily_ttest, key)
#     ttest_table.savefig("./figures/%s_Ttest.png" % key, bbox_inches='tight')
#     pyplot.cla()

# plot weekly growth table
#     if test != 'RESP':
#         weekly_growth = get_weekly_growth(means)
#         growth_table = make_growth_table(weekly_growth, number, test)
#         growth_table.savefig("./figures/%s_growth.png" % test, bbox_inches='tight')
#         pyplot.clf()


# get baseline dataframe
baseline = get_baseline(KEYS)

# plot baseline table of all tests
plot_baseline(baseline)