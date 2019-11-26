import pdb
from pandas import DataFrame
from statsmodels.stats.multicomp import MultiComparison, pairwise_tukeyhsd
from scipy.stats import ttest_ind

from raw_data import get_setup_arguments, get_raw_data
from stats import get_stats, normalize_to_control
from MBC_growth import get_weekly_growth, tabulate_growth
from helpers import Constants, replace_nan


def visualize_dynamics(set_name, normalize_by=normalize_to_control,
                       TOC_normalize_with='control', configure_plots=2):
    # input data into DataFrame
    raw_data = get_raw_data(set_name)

    # get basic statistics
    treatment_stats = get_stats(raw_data, 't')
    control_stats = get_stats(raw_data, 'c')

    treatment_effect = normalize_by(raw_data)

    TOC_normalized = normalize_to_TOC(raw_data)[TOC_normalize_with]

    # statistics to plot
    treatment_means = treatment_stats.means
    treatment_stde = treatment_stats.stde

    normalized_means = treatment_effect.means
    normalized_stde = treatment_effect.stde

    TOC_normalized_means = TOC_normalized_treatment.means
    TOC_normalized_stde = TOC_normalized_treatment.stde

    # plot
    dynamics_figure: Figure = make_figure(raw_data, i, set_name)


    top_axes: Axes = make_axes(dynamics_figure, axes_position='top of 3')
    middle_axes: Axes = make_axes(dynamics_figure, axes_position='middle')
    bottom_axes: Axes = make_axes(dynamics_figure, axes_position='bottom of 3')

    axis = [top_axes, middle_axes, bottom_axes]
    axis_positions = ['top', 'middle' 'bottom']
    axis_titles = ['control', 'baseline', 'intial']

    for axes, title in zip(axis, axis_titles):
        title_position = (0.9, 0.8)
        axes.set_title(title, position=title_position)

    for axes, axes_position in zip(axis, axis_positions):
        draw_labels(dynamics_figure, axes,
                    set_name, axes_position=axes_position)

    plot_lines(top_axes, control_normalized_means,
                                    stde=control_normalized_stde)
    plot_lines(middle_axes, baseline_normalized_means,
                                               stde=baseline_normalized_stde)
    plot_lines(bottom_axes, initial_normalized_means,
                                             stde=initial_normalized_stde)

    # legend
    handles, labels = top_axes.get_legend_handles_labels()
    dynamics_figure.legend(handles, labels, loc='center right')

    dynamics_figure.savefig(OUTPUT_DIRECTORY_PATH + set_name + FILE_PREFIX + '.png')
    pyplot.cla()

    i += 1
