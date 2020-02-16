from matplotlib.figure import Figure

from data.raw_data import get_multi_sets, get_setup_arguments
from data.stats import get_multiple_stats
from visualization.dynamics import *
from data.constants import parameters_units, figures_directory


TOP_DIRECTORY = figures_directory
DPI = 144

def visualize_single_plot(data, y_label, title=None):

    with pyplot.style.context(u'incubation-dynamics'):
        # setup figure, axes
        figure: Figure = setup_figure()
        axes = setup_dynamics_axes(figure, y_label, title)

        # plot
        plot_dynamics(data, axes, with_legend=True)

    return figure

def visualize_multiple_plots(output_dir, treatment,
                             data_sets_names=None, title_prefix: str=None):

    raw_data_sets_names = data_sets_names if data_sets_names else get_setup_arguments()
    raw_data_sets = get_multi_sets(raw_data_sets_names, treatment=treatment)
    data_sets = get_multiple_stats(raw_data_sets)

    for data_name, data in data_sets.items():

        title = f'${title_prefix} {data_name}' if title_prefix else data_name
        ylabel = parameters_units[data_name]
        figure = single_plot(data, ylabel, title)

        file_path = f'{TOP_DIRECTORY}/{output_dir}/{data_name}'
        figure.savefig(file_path, format='png', bbox_inches='tight', dpi=DPI )


if __name__ == '__main__':

    visualize_multiple_plots(output_dir='absolute_values/control',
                             treatment='c', title_prefix='control dynamics')
