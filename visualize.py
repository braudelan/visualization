from matplotlib import pyplot             # todo solve: running visualize.py with all data sets raises an error

from get_raw_data import get_setup_arguments, get_raw_data
from get_stats import get_stats
from plot import plot_all_means, plot_data
from baseline import get_baseline, plot_baseline
from control import plot_control
from Ttest import get_daily_Ttest, tabulate_daily_Ttest
from growth import get_weekly_growth, tabulate_growth


# set pyplot parameters
pyplot.rc('savefig', bbox='tight', pad_inches=1.5)

# input & output locations
INPUT_FILE = "all_tests.xlsx"
OUTPUT_DIRECTORY = output_dir = "incubation_figures"

# setup arguments
setup_arguments = get_setup_arguments()
SETS_NAMES = setup_arguments.sets
NUMBERS = setup_arguments.numbers

SOILS = ['ORG', 'MIN', 'UNC']
def get_week_ends(dataframe):
    every_7th = dataframe.index.isin([0, 7, 14, 21, 28])
    return every_7th

# main loop
for set_name, number in zip(SETS_NAMES, NUMBERS):

# input data into DataFrame
    raw_data = get_raw_data(set_name)

# get statistics
    BasicStats = get_stats(raw_data)

    means = BasicStats.means
    means_SE = BasicStats.means_SE
    MRE = BasicStats.MRE
    MRE = MRE.loc[get_week_ends(MRE)] if set_name == 'MBC' else MRE
    MRE_SE = BasicStats.MRE_SE
    MRE_SE = MRE_SE.loc[get_week_ends(MRE_SE)] if set_name == 'MBC' else MRE_SE
    control = BasicStats.control
    control_SE = BasicStats.control_SE
    difference = BasicStats.difference
    normalized = BasicStats.normalized_diff
    normalized = normalized.loc[get_week_ends(normalized)] if set_name == 'MBC' else normalized

# # plot means and normalized means(effect)
#     general_stats_fig = plot_all_means(means, normalized, means_SE, number, set_name)
#     general_stats_fig.savefig("./%s/%s_all_means_&_normalized.png" % (output_dir, set_name))
#     pyplot.cla()

# plot MRE and control seperatly
    treatment_figure = plot_data(MRE, MRE_SE, number, set_name, normalized=normalized)
    treatment_figure.savefig("./%s/%s_treatment.png" % (output_dir, set_name))
    pyplot.cla()

# # plot week ends means and normalized means of MBC and RESP
#     week_ends_fig = plot_week_ends(means, normalized, means_SE, number, set_name)
#     week_ends_fig.savefig("./%s/%s_week_ends.png" % (output_dir, set_name))
#     pyplot.cla()

# # plot control
#     control_means_fig = plot_control(means, means_SE, set_name, number)
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