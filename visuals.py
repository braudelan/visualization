import argparse

import pandas
from matplotlib import pyplot

from get_raw_data import get_single_set
from get_raw_data import get_args
from get_stats import get_stats
from plot_stats import plot_stats
from plot_control import plot_control
from get_Ttest import get_daily_ttest
from tabulate_Ttest import tabulate_Ttest
from which_round import get_round
from get_growth import get_weekly_growth
from tabulate_growth import make_growth_table

specific_sets, specific_nums = get_args()

input_file = "all_tests.xlsx"

TESTS = ['MBC','MBN', 'DOC', 'ERG', 'HWE-S', 'RESP', 'AS', 'TOC']
NUMBERS = range(1, len(TESTS)+1)

if specific_sets:
    TESTS = specific_sets

if specific_nums:
    NUMBERS = specific_nums

baseline_dict = {}

for test, number in zip(TESTS, NUMBERS):

# input data into DataFrame
    raw_data = get_single_set(test)

#get general statistics
    means, effect, means_stde = get_stats(raw_data)

#get baseline values and append to baseline_dict
    control_means       = means.xs('c', level=1, axis=1)
    baseline            = control_means.loc[0].round(get_round(means))
    baseline_to_dict    = baseline.squeeze().to_dict()
    baseline_dict[test] = baseline_to_dict

# plot means and normalized means(effect)
    general_stats_fig = plot_stats(means, effect, means_stde, number, test)
    general_stats_fig.savefig("./figures/%s_figuers.png" % test, bbox_inches='tight', pad_inches=2)
    pyplot.cla()

# plot control graph
    control_means_fig = plot_control(control_means, test, number)
    control_means_fig.savefig('./control_figures/%s.png' %test) #, bbox_inches='tight')
    pyplot.cla()

# plot ttest table
    daily_ttest = get_daily_ttest(raw_data)
    ttest_table = tabulate_Ttest(daily_ttest, test)
    ttest_table.savefig("./figures/%s_Ttest.png" %test, bbox_inches='tight')
    pyplot.cla()


    # if len(means.index) > 3:
    #     weekly_growth = get_weekly_growth(means)
    #     growth_table = make_growth_table(weekly_growth, number, test)
    #     growth_table.savefig("./figures/%s_growth.png" % test, bbox_inches='tight')
    #     pyplot.clf()


# make baseline table of all tests
baseline_data  = pandas.DataFrame.from_dict(baseline_dict)

title_text = r'baseline values of important parameters for each soil'

figure = pyplot.figure(5)

axes = figure.add_subplot(111)
axes.axis('off')
axes.axis('tight')
ttest_title = axes.set_title(title_text, pad=0.2, fontsize=20, position=(0, 1.1))

baseline_columns = baseline_data.columns

baseline_table = pyplot.table(cellText=baseline_data.values,
                           loc='center',
                           colLabels=baseline_data.columns,
                           rowLabels=baseline_data.index,
                           cellLoc='center',
                          # colWidths=[0.1 for x in baseline_data.columns],
                           # bbox = [0.0, -1.3, 1.0, 1.0]
                           )

for cell in baseline_table._cells:
    if cell[0] == 0 or cell[1] == -1:
        baseline_table._cells[cell].set_text_props(weight='bold')

baseline_table.scale(2, 3)

figure.savefig("./misc_figures/baseline_table.png", bbox_inches='tight')
pyplot.cla()