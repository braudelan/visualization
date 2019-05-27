from matplotlib import pyplot

from raw_data import get_setup_arguments, get_raw_data
from get_stats import get_stats
from plot_stats import plot_stats, plot_week_ends, plot_seperatlly
from baseline import get_baseline, plot_baseline
from control import plot_control
from Ttest import get_daily_Ttest, tabulate_daily_Ttest
from growth import get_weekly_growth, tabulate_growth


# set pyplot parameters
pyplot.rc('savefig', bbox='tight', pad_inches=1.5)

# local variables
INPUT_FILE = "all_tests.xlsx"
OUTPUT_DIRECTORY = output_dir = "incubation_figures"

# arguments to specify which data sets to load from INPUT_FILE
setup_arguments = get_setup_arguments()

SETS_NAMES = setup_arguments.sets
NUMBERS = setup_arguments.numbers

SOILS = ['ORG', 'MIN', 'UNC']
baseline_dict = {}
for set_name, number in zip(SETS_NAMES, NUMBERS):

# input data into DataFrame
    raw_data = get_raw_data(set_name)

# get general statistics
    BasicStats = get_stats(raw_data)

    means = BasicStats.means.loc[:,('t', SOILS)]
    means_stde = BasicStats.means_stde.loc[:, ('t', SOILS)]
    difference = BasicStats.difference
    normalized = BasicStats.normalized_diff

# plot means and normalized means(effect)
    general_stats_fig = plot_stats(means, normalized, means_stde, number, set_name)
    general_stats_fig.savefig("./%s/%s_all_means_&_normalized.png" % (output_dir, set_name))
    pyplot.cla()

# plot MRE and control seperatly
    treatment_figure = plot_stats(means, normalized, means_stde, number, set_name)
    treatment_figure.savefig("./%s/%s_treatment.png" % (output_dir, set_name))
    pyplot.cla()

# # plot week ends means and normalized means of MBC and RESP
#     week_ends_fig = plot_week_ends(means, normalized, means_stde, number, set_name)
#     week_ends_fig.savefig("./%s/%s_week_ends.png" % (output_dir, set_name))
#     pyplot.cla()

# # plot control
#     control_means_fig = plot_control(means, means_stde, set_name, number)
#     control_means_fig.savefig('./%s/control_%s.png' %(output_dir,set_name))
#     pyplot.cla()

# # plot ttest table
#     daily_ttest = get_daily_Ttest(raw_data)
#     ttest_table = tabulate_daily_Ttest(daily_ttest, set_name)
#     ttest_table.savefig("./%s/%s_Ttest.png" %(output_dir,set_name), bbox_inches='tight')
#     pyplot.cla()

# # plot weekly growth table
#     if test != 'RESP':
#         weekly_growth = get_weekly_growth(means)
#         growth_table = tabulate_growth(weekly_growth, number, set_name)
#         growth_table.savefig("./%s/%s_growth.png" %(output_dir,set_name) bbox_inches='tight')
#         pyplot.clf()


# # baseline dataframe
# baseline = get_baseline(nameS)
# plot_baseline(baseline)