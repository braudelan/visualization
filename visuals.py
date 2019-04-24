import argparse

import pandas
from matplotlib import pyplot

from get_raw_data import get_single_set
from get_raw_data import get_keys
from get_stats    import get_stats
from baseline     import get_baseline
from plot_stats   import plot_stats
from plot_control import plot_control
from get_Ttest    import get_daily_Ttest
# from get_growth import get_weekly_growth
# from tabulate_growth import make_growth_table

KEYS, NUMBERS = get_keys()

input_file = "all_tests.xlsx"

baseline_dict = {}


for key, number in zip(KEYS, NUMBERS):

# input data into DataFrame
    raw_data = get_single_set(key)

# get general statistics
    means, effect, means_stde = get_stats(raw_data)

# plot means and normalized means(effect)
#     general_stats_fig = plot_stats(means, effect, means_stde, number, key)
#     general_stats_fig.savefig("./figures/%s_figuers.png" % key, bbox_inches='tight', pad_inches=2)
#     pyplot.cla()
#
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
title_text = r'baseline values of important parameters for each soil'

baseline_figure = pyplot.figure(5)

axes = baseline_figure.add_subplot(111)
axes.axis('off')
axes.axis('tight')
ttest_title = axes.set_title(title_text, pad=0.2, fontsize=20, position=(0, 1.1))

baseline_table = pyplot.table(cellText=baseline.values,
                           loc='center',
                           colLabels=baseline.columns,
                           rowLabels=baseline.index,
                           cellLoc='center',
                          # colWidths=[0.1 for x in baseline.columns],
                           # bbox = [0.0, -1.3, 1.0, 1.0]
                           )

for cell in baseline_table._cells:
    if cell[0] == 0 or cell[1] == -1:
        baseline_table._cells[cell].set_text_props(weight='bold')

baseline_table.scale(2, 3)

baseline_figure.savefig("./misc_figures/baseline_table.png", bbox_inches='tight')
pyplot.cla()