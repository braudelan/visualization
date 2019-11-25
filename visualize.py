import pdb

from matplotlib import pyplot
from matplotlib.pyplot import Figure, Axes
from raw_data import get_setup_arguments, get_raw_data, get_multi_sets, get_ergosterol_to_biomass, get_microbial_C_N, \
    baseline_normalize, control_normalize
from stats import get_stats,\
from plot import make_figure, make_axes, plot_lines, \
    draw_labels, plot_control_composite, plot_C_N
from significance import visualize_daily_significance
from helpers import Constants, get_week_ends, DataFrame_to_image

# from model_dynamics import plot_model
# from Ttest import get_daily_Ttest
# from growth import get_weekly_growth, tabulate_growth

# set pyplot parameters
pyplot.rc('savefig',  pad_inches=1.5)

# input & output locations
INPUT_FILE = Constants.input_file_name
FIGURES_DIRECTORY_PATH = Constants.output_directory
SPECIFIED_DIRECTORY_PATH = '/dynamics/'
OUTPUT_DIRECTORY_PATH = FIGURES_DIRECTORY_PATH + SPECIFIED_DIRECTORY_PATH

# setup
setup_arguments = get_setup_arguments()

DATA_SETS_NAMES = setup_arguments.sets
NUMBERS = setup_arguments.numbers
RAW_DATA_SETS = get_multi_sets(DATA_SETS_NAMES)

TABLE_CSS = Constants.table_css

def dynamics(data_set_names):
    '''visualize dynamics of each parameter and save as a separate image file.'''


    def plot_data_pairs(data_pair, data_label: str,
                 figure_number, titles: list = None):

        # statistics to plot
        data_1 = data_pair[0]
        data_2 = data_pair[1]
        means_1 = data_1.means
        stde_1 = data_1.stde
        means_2 = data_2.means
        stde_2 = data_2.stde

        # figure
        dynamics_figure: Figure = \
            make_figure(raw_data, figure_number, data_set_name)

        # axis
        top_axes: Axes = make_axes(dynamics_figure,
                                   axes_position='top of 2')
        bottom_axes: Axes = make_axes(dynamics_figure,
                                      axes_position='bottom of 2')

        axis = [top_axes, bottom_axes]
        positions = ['top', 'bottom']

        # set titles
        if titles:
            axis_titles = zip(axis, titles)
            for axes, title in axis_titles:
                title_position = (0.9, 0.8)
                axes.set_title(title, position=title_position)

        # insert decorations
        axis_positions = zip(axis, positions)
        for axes, axes_position in axis_positions:
            draw_labels(dynamics_figure, axes,
                        data_set_name, axes_position=axes_position)
        # plot data
        plot_lines(top_axes, means_1, stde=stde_1)
        plot_lines(bottom_axes, means_2, stde=stde_2)

        # legend
        handles, labels = top_axes.get_legend_handles_labels()
        dynamics_figure.legend(handles, labels,
                               loc='center right')

        output_file = f'{OUTPUT_DIRECTORY_PATH}{data_set_name}_{data_label}.png'
        dynamics_figure.savefig(output_file)
        pyplot.clf()

    i = 1
    for data_set_name in data_set_names:

        # raw data
        if data_set_name == 'ERG':
            raw_data = get_ergosterol_to_biomass()
        else:
            raw_data = get_raw_data(data_set_name)

        raw_treatment = raw_data['t']
        raw_control = raw_data['c']
        raw_control_normalized = control_normalize(raw_data)
        raw_basline_normalized = baseline_normalize(raw_data)

        raw_data_sets = [
            ('MRE treated', raw_treatment),
            ('control', raw_control),
            ('control normalized', raw_control_normalized),
            ('baseline normalized', raw_basline_normalized),
        ]

        # significance between soils on each day
        for label, set in raw_data_sets:
            output_file = f'{OUTPUT_DIRECTORY_PATH}{data_set_name}'
            visualize_daily_significance(set, TABLE_CSS, OUTPUT_DIRECTORY_PATH, label)

        # get basic statistics
        treatment_stats = get_stats(raw_data, 't')
        control_stats = get_stats(raw_data, 'c')
        control_normalized = get_stats(control_normalize(raw_data))
        baseline_normalized = get_stats(baseline_normalize(raw_data))

        # visualize dynamics
        absolute = (treatment_stats, control_stats)
        normalized = (control_normalized, baseline_normalized)
        absolute_titles = ['MRE treated', 'control']
        normalized_titles = ['control normalized','baseline normalized']
        plot_arguments = (
            (absolute, 'absolute', absolute_titles),
            (normalized, 'normalized', normalized_titles)
        )
        for pair, label, titles in plot_arguments:
            plot_data_pairs(data_pair=pair, data_label=label,
                                figure_number=i, titles=titles)


        i += 1

# -------------------------------------baseline-------------------------------------------------------------------------

# # plot baseline
# soil_properties_figure = plot_baseline(raw_data_sets)
# soil_properties_figure.savefig('%sbaseline.png' % OUTPUT_DIRECTORY, bbox_inches='tight')

# -------------------------------------control--------------------------------------------------------------------------
# # plot composite image of control dynamics
# control_composite_figure = plot_control_composite(RAW_DATA_SETS)
# control_composite_figure.savefig('%scontrol.png' % OUTPUT_DIRECTORY_PATH)

# -------------------------------------C-to-N ratio---------------------------------------------------------------------

def visualize_C_N(label: str, MBC_raw, MBN_raw):

    C_to_N_raw = get_microbial_C_N(MBC_raw, MBN_raw)
    C_to_N_stats = get_stats(C_to_N_raw)

    means = C_to_N_stats.means
    stde = C_to_N_stats.stde

    figure = make_figure()
    axes = make_axes(figure)
    plot_lines(axes,means, stde=stde)
    figure.savefig(f'{OUTPUT_DIRECTORY_PATH}/{label}_C_to_N.png' % (OUTPUT_DIRECTORY_PATH, label))


# -------------------------------------ergostrol-to-microbial-biomass ratio----------------------------------------------
# # todo fix scale of labels and MRE marks
# raw_ERG_to_MBC = get_ergosterol_to_biomass()
# ERG_to_MBC_treatment = raw_ERG_to_MBC['t']
# ERG_to_MBC_control = raw_ERG_to_MBC['c']
# ERG_to_MBC_by_control = control_normalize(raw_ERG_to_MBC)
# ERG_to_MBC_by_baseline = baseline_normalize(raw_ERG_to_MBC)
#
#
# stats_tuples = [
#     ERG_to_MBC_control,
#     ERG_to_MBC_treatment,
#     ERG_to_MBC_by_baseline,
#     ERG_to_MBC_by_control,
# ]
#
# tuples_names = [
#     'control',
#     'treatment',
#     'baseline_normalized',
#     'control_normalized',
# ]
#
# y_label = r'$\% \frac{sergosterol}{MBC}$'
# zipped = zip(tuples_names, stats_tuples)
# i = 1
# for name, tuple in zipped:
#     means = tuple.means
#     stde = tuple.stde
#     figure = make_figure(i)
#     axes = make_axes(figure)
#     plot_lines(axes,means,stde=stde)
#     draw_labels(figure,axes,y_label=y_label, label_rotation=45)
#
#     figure.savefig(OUTPUT_DIRECTORY_PATH + name + '.png')
#
#     i += 1


# -------------------------------------significance---------------------------------------------------
#
# css = """
#     <style type=\"text/css\">
#     table {
#     color: #333;
#     font-family: Helvetica, Arial, sans-serif;
#     width: 640px;
#     border-collapse:
#     collapse;
#     border-spacing: 0;
#     }
#     td, th {
#     border: 1px solid transparent; /* No more visible border */
#     height: 30px;
#     }
#     th {
#     background: #DFDFDF; /* Darken header a bit */
#     font-weight: bold;
#     }
#     td {
#     background: #FAFAFA;
#     text-align: center;
#     }
#     table tr:nth-child(odd) td{
#     background-color: white;
#     }
#     </style>
#     """ # html code specifying the appearence of significance table
#
# def visualize_significance(set_name, notations, css, label: str=None):
#
#     notations_output_file = f'{OUTPUT_DIRECTORY_PATH}{set_name}_{label}.png'
#     DataFrame_to_image(notations, css, outputfile=notations_output_file)
#
# # visualize significance between soils for every day of incubation
# def daily_between_soils_significance(data_sets_names, label: str=None):
#
#     for set_name in DATA_SETS_NAMES:
#         raw_data = get_raw_data(set_name)
#         normalized_raw_data = subtract_baseline(raw_data)
#         significance = daily_significance_between_soils(normalized_raw_data)
#         visualize_significance(set_name, significance, css, label)

