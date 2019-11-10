import pdb

from matplotlib import pyplot
from matplotlib.pyplot import Figure, Axes
from raw_data import get_setup_arguments, get_raw_data, get_multi_sets
from stats import get_stats, normalize_to_control, normalize_to_baseline,\
    normalize_to_initial, normalize_to_TOC, get_microbial_C_N, get_ergosterol_to_biomass
from plot import make_figure, make_axes, plot_lines, \
    draw_labels, plot_control_composite, plot_C_N
from significance import significance_between_soils
from helpers import get_week_ends, DataFrame_to_image

# from model_dynamics import plot_model
# from Ttest import get_daily_Ttest
# from growth import get_weekly_growth, tabulate_growth

# set pyplot parameters
pyplot.rc('savefig',  pad_inches=1.5)

# input & output locations
INPUT_FILE = "all_tests.xlsx"
FIGURES_DIRECTORY_PATH = '/home/elan/Dropbox/research/figures'
SPECIFIED_DIRECTORY_PATH = '/ergosterol_to_biomass/'
OUTPUT_DIRECTORY_PATH = FIGURES_DIRECTORY_PATH + SPECIFIED_DIRECTORY_PATH

# setup
setup_arguments = get_setup_arguments()

DATA_SETS_NAMES = setup_arguments.sets
NUMBERS = setup_arguments.numbers
RAW_DATA_SETS = get_multi_sets(DATA_SETS_NAMES)

i=1
# plot dynamics of each soil parameter as a separate graph
# for set_name in DATA_SETS_NAMES:
#
#     # input data into DataFrame
#     raw_data = get_raw_data(set_name)
#
#     # get basic statistics
#     treatment_stats = get_stats(raw_data, 't')
#     control_stats = get_stats(raw_data, 'c')
#     control_normalized = normalize_to_control(raw_data)
#     baseline_normalized = normalize_to_baseline(raw_data)
#     initial_normalized = normalize_to_initial(raw_data)
#     TOC_normalized_treatment = normalize_to_TOC(raw_data)['treatment']
#     TOC_normalized_control = normalize_to_TOC(raw_data)['control']
#     TOC_normalized_normal = normalize_to_TOC(raw_data)['normalized']
#
#     # statistics to plot
#     treatment_means = treatment_stats.means
#     treatment_stde = treatment_stats.stde
#     control_means = control_stats.means
#     control_stde = control_stats.stde
#     control_normalized_means = control_normalized.means
#     control_normalized_stde = control_normalized.stde
#     baseline_normalized_means = baseline_normalized.means
#     baseline_normalized_stde = baseline_normalized.stde
#     initial_normalized_means = initial_normalized.means
#     initial_normalized_stde = initial_normalized.stde
#     TOC_normalized_treatment_means = TOC_normalized_treatment.means
#     TOC_normalized_treatment_stde = TOC_normalized_treatment.stde
#     TOC_normalized_normal_means = TOC_normalized_normal.means
#     TOC_normalized_normal_stde = TOC_normalized_normal.stde
#
#     # figure
#     dynamics_figure: Figure= make_figure(raw_data, i, set_name)
#
#     # axis
#     top_axes: Axes = make_axes(dynamics_figure, axes_position='top of 2')
#     # middle_axes: Axes = make_axes(dynamics_figure, axes_position='middle')
#     bottom_axes: Axes = make_axes(dynamics_figure, axes_position='bottom of 2')
#
#     axis = [top_axes, bottom_axes]
#     axis_positions = ['top', 'bottom']
#     axis_titles = ['MRE treated', 'control']
#
#     #set titles
#     for axes, title in zip(axis, axis_titles):
#         title_position = (0.9, 0.8)
#         axes.set_title(title, position=title_position)
#
#     # insert decorations
#     for axes, axes_position in zip(axis, axis_positions):
#         draw_labels(dynamics_figure, axes,
#                     set_name, axes_position=axes_position)
#     # plot data
#     plot_lines(top_axes, treatment_means,
#                                     stde=treatment_stde)
#     # plot_lines(middle_axes, baseline_normalized_means,
#     #                                            stde=baseline_normalized_stde)
#     plot_lines(bottom_axes, control_means,
#                                     stde=control_stde)
#
#     # legend
#     handles, labels = top_axes.get_legend_handles_labels()
#     dynamics_figure.legend(handles, labels, loc='center right')
#
#
#     dynamics_figure.savefig(OUTPUT_DIRECTORY_PATH + set_name + '.png')
#     pyplot.cla()
#
#     i += 1

# -------------------------------------baseline-------------------------------------------------------------------------

# # plot baseline
# soil_properties_figure = plot_baseline(raw_data_sets)
# soil_properties_figure.savefig('%sbaseline.png' % OUTPUT_DIRECTORY, bbox_inches='tight')

# -------------------------------------control--------------------------------------------------------------------------
# # plot composite image of control dynamics
# control_composite_figure = plot_control_composite(RAW_DATA_SETS)
# control_composite_figure.savefig('%scontrol.png' % OUTPUT_DIRECTORY_PATH)

# -------------------------------------C-to-N ratio---------------------------------------------------------------------
# visualize microbial C_to_N
def visualize_C_N(label: str, treatment: str=None,
                  normalization=None):

    MBC_raw = get_raw_data('MBC')
    MBN_raw = get_raw_data('MBN')
    if normalization is not None:
        MBC_stats = normalization(MBC_raw)
        MBN_stats = normalization(MBN_raw)
    else:
        MBC_stats = get_stats(MBC_raw, treatment)
        MBN_stats = get_stats(MBN_raw, treatment)

    print ('MBC means: ', MBC_stats.means)
    print('MBN means: ', MBN_stats.means)
    print('MBC stde: ', MBC_stats.stde)
    print('MBN stde: ', MBN_stats.stde)

    C_to_N_stats = get_microbial_C_N(MBC_stats, MBN_stats)
    C_to_N = C_to_N_stats.means
    C_to_N_stde = C_to_N_stats.stde


    figure = make_figure()
    axes = make_axes(figure)
    plot_lines(axes,C_to_N, stde=C_to_N_stde)
    figure.savefig('%s/%s_C_to_N.png' % (OUTPUT_DIRECTORY_PATH, label))

# normalization_functions = [
#                             normalize_to_control,
#                             normalize_to_baseline,
#                             normalize_to_initial
#                        ]
# labels = ['control','baseline', 'initial'] #'control'
# for function, label in zip(normalization_functions, labels):
#     visualize_C_N(label, normalization=function)
# visualize_C_N('simple_means', 't')


# -------------------------------------significance between treatmetns---------------------------------------------------

def visualize_significance(set_name, notations, p_values):

    css = """
    <style type=\"text/css\">
    table {
    color: #333;
    font-family: Helvetica, Arial, sans-serif;
    width: 640px;
    border-collapse:
    collapse; 
    border-spacing: 0;
    }
    td, th {
    border: 1px solid transparent; /* No more visible border */
    height: 30px;
    }
    th {
    background: #DFDFDF; /* Darken header a bit */
    font-weight: bold;
    }
    td {
    background: #FAFAFA;
    text-align: center;
    }
    table tr:nth-child(odd) td{
    background-color: white;
    }
    </style>
    """
    notations_output_file = OUTPUT_DIRECTORY_PATH + set_name + '_letters'
    values_output_file = OUTPUT_DIRECTORY_PATH + set_name + '_p_values'
    DataFrame_to_image(notations, css, outputfile=notations_output_file)
    DataFrame_to_image(p_values, css, outputfile=values_output_file)

# # visualize significance
# for set_name in DATA_SETS_NAMES:
#     raw_data = get_raw_data(set_name)
#     significance = significance_between_soils(raw_data, 't')
#     letters = significance[0]
#     p_values = significance[1]
#     visualize_significance(set_name, letters, p_values)

# visualize_significance()

# -------------------------------------ergostrol-to-microbial-biomass ratio----------------------------------------------
# todo fix scale of labels and MRE marks
ERG_to_MBC_treatment = get_ergosterol_to_biomass('t')
ERG_to_MBC_control = get_ergosterol_to_biomass('c')
ERG_to_MBC_by_control = get_ergosterol_to_biomass(normalize_by=normalize_to_control)
ERG_to_MBC_by_baseline = get_ergosterol_to_biomass(normalize_by=normalize_to_baseline)

stats_tuples = [
    ERG_to_MBC_control,
    ERG_to_MBC_treatment,
    ERG_to_MBC_by_baseline,
    ERG_to_MBC_by_control,
]

tuples_names = [
    'control',
    'treatment',
    'baseline_normalized',
    'control_normalized',
]

y_label = r'$\% \frac{sergosterol}{MBC}$'
zipped = zip(tuples_names, stats_tuples)
i = 1
for name, tuple in zipped:
    means = tuple.means
    stde = tuple.stde
    figure = make_figure(i)
    axes = make_axes(figure)
    plot_lines(axes,means,stde=stde)
    draw_labels(figure,axes,y_label=y_label, label_rotation=45)

    figure.savefig(OUTPUT_DIRECTORY_PATH + name + '.png')

    i += 1



