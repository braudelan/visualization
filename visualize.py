from matplotlib import pyplot             # todo solve: running visualize.py with all data sets raises an error
from matplotlib.pyplot import Figure, Axes
from raw_data import get_setup_arguments, get_raw_data, get_multi_sets
from stats import normalize_to_control, get_stats, normalize_to_baseline,\
    normalize_to_initial, normalize_to_TOC
from plot import make_figure, make_axes, plot_lines, draw_labels
from helpers import get_week_ends
# from model_dynamics import plot_model
# from Ttest import get_daily_Ttest
# from growth import get_weekly_growth, tabulate_growth


# set pyplot parameters
pyplot.rc('savefig',  pad_inches=1.5)

# input & output locations
INPUT_FILE = "all_tests.xlsx"
FIGURES_DIRECTORY_PATH = '/home/elan/Dropbox/research/figures'
SPECIFIED_DIRECTORY_PATH = '/TOC_normalized/'
OUTPUT_DIRECTORY_PATH = FIGURES_DIRECTORY_PATH + SPECIFIED_DIRECTORY_PATH
FILE_PREFIX = '_simple_means_and_baseline'

# setup
setup_arguments = get_setup_arguments()

DATA_SETS_NAMES = setup_arguments.sets
NUMBERS = setup_arguments.numbers
RAW_DATA_SETS = get_multi_sets(DATA_SETS_NAMES)

i=1
# plot dynamics of each soil parameter as a seperate graph
for set_name in DATA_SETS_NAMES:

    # input data into DataFrame
    raw_data = get_raw_data(set_name)

    # get basic statistics
    treatment_stats = get_stats(raw_data, 't')
    control_stats = get_stats(raw_data, 'c')
    control_normalized = normalize_to_control(raw_data)
    baseline_normalized = normalize_to_baseline(raw_data)
    initial_normalized = normalize_to_initial(raw_data)
    TOC_normalized_treatment = normalize_to_TOC(raw_data)['treatment']
    TOC_normalized_control = normalize_to_TOC(raw_data)['control']
    TOC_normalized_normal = normalize_to_TOC(raw_data)['normalized']

    # statistics to plot
    treatment_means = treatment_stats.means
    treatment_stde = treatment_stats.stde
    control_means = control_stats.means
    control_stde = control_stats.stde
    control_normalized_means = control_normalized.means
    control_normalized_stde = control_normalized.stde
    baseline_normalized_means = baseline_normalized.means
    baseline_normalized_stde = baseline_normalized.stde
    initial_normalized_means = initial_normalized.means
    initial_normalized_stde = initial_normalized.stde
    TOC_normalized_treatment_means = TOC_normalized_treatment.means
    TOC_normalized_treatment_stde = TOC_normalized_treatment.stde
    TOC_normalized_normal_means = TOC_normalized_normal.means
    TOC_normalized_normal_stde = TOC_normalized_normal.stde

    # plot
    dynamics_figure: Figure= make_figure(raw_data, i, set_name)

    top_axes: Axes = make_axes(dynamics_figure, axes_position='top of 2')
    # middle_axes: Axes = make_axes(dynamics_figure, axes_position='middle')
    bottom_axes: Axes = make_axes(dynamics_figure, axes_position='bottom')

    axis = [top_axes, bottom_axes]
    axis_positions = ['top', 'bottom']
    axis_titles = ['simple means', 'normalized to baseline']

    for axes, title in zip(axis, axis_titles):
        title_position = (0.9, 0.8)
        axes.set_title(title, position=title_position)

    for axes, axes_position in zip(axis, axis_positions):
        draw_labels(dynamics_figure, axes,
                    set_name, axes_position=axes_position)

    # treatment_lines = plot_lines(top_axes, control_normalized_means,
    #                              stde=control_normalized_stde)
    # control_lines = plot_lines(means_axes, control_means,
    # #                                          'control', control_stde)
    simple_means_lines = plot_lines(top_axes, TOC_normalized_treatment_means,
                                    stde=TOC_normalized_treatment_stde)
    # normalized_to_baseline_lines = plot_lines(middle_axes, baseline_normalized_means,
    #                                           stde=baseline_normalized_stde)
    normalized_to_baseline_lines = plot_lines(bottom_axes, TOC_normalized_normal_means,
                                             stde=TOC_normalized_normal_stde)

    # legend
    # handles = top_axes.lines
    handles, labels = top_axes.get_legend_handles_labels()
    dynamics_figure.legend(handles, labels, loc='center right')


    dynamics_figure.savefig(OUTPUT_DIRECTORY_PATH + set_name + FILE_PREFIX + '.png')
    pyplot.cla()

    i += 1


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
