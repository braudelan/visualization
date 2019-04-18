import argparse

import pandas
from matplotlib import pyplot

from stats import get_stats
from plot_stats import plot_stats
from plot_control import plot_control
from daily_ttest import get_daily_ttest
from daily_ttest_table import plot_ttest_table
from which_round import get_round
from growth import get_weekly_growth
from growth_table import make_growth_table

parser = argparse.ArgumentParser()
parser.add_argument('-s_tests', help='specfic tests to run the script with', nargs='+')
parser.add_argument('-s_numbers', help='specify figure numbers for s_tests', nargs='+', type=int)
args = parser.parse_args()

input_file = "all_tests.xlsx"

TESTS = ['MBC','MBN', 'DOC', 'ERG', 'HWE-S', 'RESP', 'AS', 'TOC']
NUMBERS = range(1, len(TESTS)+1)

if args.s_tests:
    TESTS = args.s_tests

if args.s_numbers:
    NUMBERS = args.s_numbers

baseline_dict = {}

for test, number in zip(TESTS, NUMBERS):

# input data into DataFrame
    raw_data = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                     sheet_name=test,
                                     na_values=["-", " "]).rename_axis("days")
    raw_data.columns.rename(["soil", "treatment", "replicate"],
                            level=None, inplace=True)
    raw_data.columns.set_levels(["c", "t"], level=1, inplace=True)

#get general statistics
    means, means_stde, effect = get_stats(raw_data)

#get baseline values and append to baseline_dict
    control_means       = means.xs('c', level=1, axis=1)
    baseline            = control_means.loc[0].round(get_round(means))
    baseline_to_dict    = baseline.squeeze().to_dict()
    baseline_dict[test] = baseline_to_dict

# plot graphs of basic statistics
    basic_stats_fig = plot_stats(means, effect, means_stde, number, test)
    basic_stats_fig.savefig("./one_shot_figures/%s_figuers.png" % test, bbox_inches='tight', pad_inches=2)
    pyplot.cla()

# plot control graph
    control_means_fig = plot_control(control_means, test, number)
    control_means_fig.savefig('./control_figures/%s.png' %test) #, bbox_inches='tight')
    pyplot.cla()

# plot ttest table
    daily_ttest = get_daily_ttest(raw_data)
    ttest_table = plot_ttest_table(daily_ttest, test)
    ttest_table.savefig("./one_shot_figures/%s_Ttest.png" %test, bbox_inches='tight')
    pyplot.cla()


    # if len(means.index) > 3:
    #     weekly_growth = get_weekly_growth(means)
    #     growth_table = make_growth_table(weekly_growth, number, test)
    #     growth_table.savefig("./one_shot_figures/%s_growth.png" % test, bbox_inches='tight')
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

figure.savefig("./figures/baseline_table.png", bbox_inches='tight')
pyplot.cla()