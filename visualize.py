from matplotlib import pyplot             # todo solve: running visualize.py with all data sets raises an error

from raw_data import get_setup_arguments, get_raw_data, get_multi_sets
from stats import normalize_to_control, get_stats
from plot import make_figure, make_axes, plot_lines, draw_labels
from helpers import get_week_ends
# from model_dynamics import plot_model
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
RAW_DATA_SETS = get_multi_sets(DATA_SETS_NAMES)

# plot dynamics of each soil parameter as a seperate graph
for set_name, number in zip(DATA_SETS_NAMES, NUMBERS):

    # input data into DataFrame
    raw_data = get_raw_data(set_name)
    normalized_raw = normalize_to_control(raw_data)

    # get basic statistics
    treatment_stats = get_stats(raw_data, 't')
    control_stats = get_stats(raw_data, 'c')
    normalized_stats = get_stats(normalized_raw, 't')

    # statistics to plot
    treatment_means = treatment_stats.means
    treatment_stde = treatment_stats.stde
    control_means = control_stats.means
    control_stde = control_stats.stde
    norm_means = normalized_stats.means
    norm_stde = normalized_stats.stde

    # plot dynamics
    dynamics_figure = make_figure(raw_data, number, set_name)

    means_axes = make_axes(dynamics_figure, axes_position='single')
    # normalized_axes = make_axes(dynamics_figure, axes_position='bottom of 2')

    treatment_lines = plot_lines(means_axes, treatment_means,
                                             'treatment', treatment_stde)
    control_lines = plot_lines(means_axes, control_means,
                                             'control', control_stde)
    # normalized_lines = plot_lines(normalized_axes, norm_means,
    #                                          'normalized', norm_stde)

    # draw_labels(dynamics_figure, wknds_axes,
    #                         set_name, axes_position='top of 3')
    draw_labels(dynamics_figure, means_axes,
                            set_name, axes_position='single')
    # draw_labels(dynamics_figure, normalized_axes,
    #                         set_name, axes_position='bottom of 2')

    dynamics_figure.savefig("%s/%s_dynamics.png" % (OUTPUT_DIRECTORY, set_name))
    pyplot.cla()



# # plot baseline
# soil_properties_figure = plot_baseline(raw_data_sets)
# soil_properties_figure.savefig('%s/baseline.png' % OUTPUT_DIRECTORY, bbox_inches='tight')

# # plot composite image of control dynamics
# control_composite_figure = plot_control_composite(raw_data_sets)
# control_composite_figure.savefig('%s/control.png' % OUTPUT_DIRECTORY)

# # plot C to N ratio
# c_to_n = get_carbon_stats()
# carbon_figure = plot_c_to_n(c_to_n)
# carbon_figure.savefig('./%s/C_to_N.png' %OUTPUT_DIRECTORY)


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
