
from matplotlib.figure import Figure

from data.raw_data import *
from data.stats import get_multiple_stats
from visualization.dynamics import *
from data.constants import *

# matplotlib.use("pgf")

TOP_DIRECTORY = figures_directory
DPI = 144

def visualize_single_plot(data, data_name, y_label, output_dir):

    with pyplot.style.context(u'incubation-dynamics'):
        # setup figure, axes
        figure: Figure = setup_figure()
        axes = setup_dynamics_axes(figure, y_label)

        # plot
        plot_dynamics(data, axes, with_legend=True)

        # save
        file_path = f'{TOP_DIRECTORY}/{output_dir}/{data_name}'
        figure.savefig(file_path, format='png', bbox_inches='tight', dpi=DPI)

    return figure

def visualize_multiple_plots(output_dir, treatment=None, normalize=None,
                             data_sets_names=None, title_prefix: str=None):

    raw_data_sets_names = data_sets_names if data_sets_names else get_setup_arguments()
    raw_data_sets = get_multi_sets(
        raw_data_sets_names,
        treatment=treatment,
        normalize_by=normalize,
    )
    data_sets = get_multiple_stats(raw_data_sets)

    for data_name, data in data_sets.items():

        # title = f'${PARAMETERS_TITLES[data_name]}{title_prefix}$' if title_prefix else PARAMETERS_TITLES[data_name]
        ylabel = f'${parameters_units[data_name]}$'
        figure = visualize_single_plot(data, data_name, ylabel, output_dir)




if __name__ == '__main__':
    names = ['RESP']
    normalize = None
    visualize_multiple_plots(
        output_dir='absolute_values/control',
        treatment='c',
        normalize=normalize,
        data_sets_names=names,
    )
