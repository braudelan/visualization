from matplotlib import pyplot             # todo solve: running visualize.py with all data sets raises an error

from raw_data import get_setup_arguments, get_raw_data, get_multi_sets
from stats import get_normalized, get_stats, get_carbon_stats
from plot import make_figure, plot_dynamics, plot_baseline, plot_control_composite
# from model_dynamics import plot_model
from helpers import get_week_ends
# from Ttest import get_daily_Ttest
# from growth import get_weekly_growth, tabulate_growth


# set pyplot parameters
pyplot.rc('savefig',  pad_inches=1.5)

# input & output locations
INPUT_FILE = "all_tests.xlsx"
OUTPUT_DIRECTORY = '/home/elan/Dropbox/research/figures'


# setup
setup_arguments = get_setup_arguments()

DATA_SETS_NAMES = setup_arguments.sets
NUMBERS = setup_arguments.numbers

# plot dynamics of each soil parameter as a seperate graph
for set_name, number in zip(DATA_SETS_NAMES, NUMBERS):

    # input data into DataFrame
    raw_data = get_raw_data(set_name)

    # get basic statistics
    stats = get_stats(raw_data, 't')
    normalized_stats = get_normalized(raw_data)

    # statistics to plot
    means = stats.means
    stde = stats.stde
    stdv = stats.stdv

    norm_means = normalized_stats.means
    norm_stde = normalized_stats.stde
    norm_stdv = normalized_stats.stdv

    # # plot dynamics
    # dynamics_figure = make_figure(raw_data, number, set_name)
    #
    # plot_dynamics(dynamics_figure, means, stde, set_name, axes_lineup=1)
    # plot_dynamics(dynamics_figure, norm_means, norm_stde, set_name, axes_lineup=2)
    #
    # dynamics_figure.savefig("%s/%s_normalized.png" % (OUTPUT_DIRECTORY, set_name))
    # pyplot.cla()

raw_data_sets = get_multi_sets(DATA_SETS_NAMES)

# plot baseline
soil_properties_figure = plot_baseline(raw_data_sets)
soil_properties_figure.savefig('%s/baseline.png' % OUTPUT_DIRECTORY, bbox_inches='tight')

# plot composite image of control dynamics
control_composite_figure = plot_control_composite(raw_data_sets)
control_composite_figure.savefig('%/control.png' % OUTPUT_DIRECTORY, bbox_inches='tight')

# # plot C to N ratio
# c_to_n = get_carbon_stats()
# carbon_figure = plot_c_to_n(c_to_n)
# carbon_figure.savefig('./%s/C_to_N.png' %OUTPUT_DIRECTORY)

# MRE = MRE.loc[get_week_ends(MRE)] if set_name == 'RESP' else MRE
# MRE_SE = MRE_SE.loc[get_week_ends(MRE_SE)] if set_name == 'RESP' else MRE_SE
# normalized = normalized.loc[get_week_ends(normalized)] if set_name == 'RESP' else normalized

# # plot control
#     control_means_fig = plot_control(means, means_SE, set_name, number)
#     control_means_fig.savefig('./%s/control_%s.png' %(OUTPUT_DIRECTORY,set_name))
#     pyplot.cla()

# # plot ttest table
#     daily_ttest = get_daily_Ttest(raw_data)
#     ttest_table = tabulate_daily_Ttest(daily_ttest, set_name)
#     ttest_table.savefig("./%s/%s_Ttest.png" %(OUTPUT_DIRECTORY,set_name), bbox_inches='tight')
#     pyplot.cla()

# # plot weekly growth table
#     if test != 'RESP':
#         weekly_growth = get_weekly_growth(means)
#         growth_table = tabulate_growth(weekly_growth, number, set_name)
#         growth_table.savefig("./%s/%s_growth.png" %(OUTPUT_DIRECTORY,set_name) bbox_inches='tight')
#         pyplot.clf()
