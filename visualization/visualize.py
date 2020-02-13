from visualization.dynamics import *


def visualize_single_plot(data, y_label, title=None):

    with pyplot.style.context(u'incubation-dynamics'):
        # setup figure, axes
        figure = setup_figure()
        axes = setup_dynamics_axes(figure, y_label, title)

        # plot
        plot_dynamics(data, axes, with_legend=True)

    return axes


if __name__ == '__main__':

    raw_data = get_raw_data('MBC')
    stats = get_stats(raw_data, 't')
    ylabel = r'$y\ not$'
    title = r'$some\ title$'

    axes = visualize_single_plot(stats, ylabel, title)
    # cycle_through_styles(stats, ylabel)

# todo
#   define visualize_a_bunch_of_data_sets()