from typing import Tuple, Dict

import numpy
from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from raw_data import get_multi_sets
from stats import get_baseline_stats
from helpers import Constants


SOILS = Constants.groups
COLORS = Constants.colors

PLOT_STYLE = 'seaborn-ticks'
pyplot.style.use(PLOT_STYLE)


def make_bar_axes(figure: Figure,x_locations, soil_width, title,
                       y_label, x_label=None, categories=None) -> Axes:

    TITLE_PAD = 20
    XLABEL_PAD = 2
    YLABEL_PAD = 25
    TICK_LABEL_SIZE = 12
    AXIS_LABEL_SIZE = 12

    axes: Axes = figure.add_subplot(111)

    # labels
    axes.set_title(title, pad=TITLE_PAD)
    axes.set_ylabel(
        y_label,
        rotation=90,
        verticalalignment='center',
        labelpad=YLABEL_PAD,
        fontsize= AXIS_LABEL_SIZE
    )
    axes.set_xlabel(
        x_label,
        fontsize=AXIS_LABEL_SIZE,
    )

    # x ticks
    axes.set_xticks(x_locations + soil_width)
    axes.set_xticklabels(categories)
    axes.xaxis.set_tick_params(
        length=0,
        pad=10,
        labelsize=TICK_LABEL_SIZE,
    )
    x_majortick_labels = axes.get_xmajorticklabels()
    axes.set_xticklabels(
        x_majortick_labels,
        ha='center',
        rotation=-30
    )

    # y ticks
    major_yticks = numpy.arange(-50, 150,50)
    axes.set_yticks(major_yticks)
    minor_yticks = numpy.arange(-100, 100, 10)
    axes.set_yticks(minor_yticks, minor=True)
    axes.yaxis.set_tick_params(
        labelsize=TICK_LABEL_SIZE,
    )
    axes.set_ylim(-80, 120)

    # change the '0' tick_label into 'UNC'
    zero = axes.yaxis.get_majorticklabels()[1]
    zero.set_label('UNC')

    # plot a line at y=zero, indicating the refernce level (=UNC)
    xlim = axes.get_xlim()
    lower_x = xlim[0]
    upper_x = xlim[1]
    x = numpy.arange(lower_x, upper_x)
    y = numpy.zeros(len(x))
    axes.plot(
        x,
        y,
        linewidth=0.8,
        color='black',
    )
    return axes

def make_bars(axes: Axes, x_location, heights, width, labels, bar_error=None):

    bars = {}
    i = 0
    for soil_label, height in zip(labels, heights):
        if bar_error is not None:
            bar = axes.bar(
                   x=x_location + i,
                   height=height,
                   width=width,
                   yerr=bar_error[soil_label],
                   label=soil_label,
                   color=COLORS[soil_label]
            )
        else:
            bar = axes.bar(
                   x=x_location + i,
                   height=height,
                   width=width,
                   label=soil_label,
                   color=COLORS[soil_label]
            )

        i += width

        bars[soil_label] = bar

    return bars


def plot_baseline(raw_data_sets: dict, spacing, relative_width) -> Tuple[Figure, Dict[str, dict]]:
    """plot baseline values of multiple data sets.

    this function takes only the control replicates from every data set(=category or analysis)
    and produces the average for every soil over day 0 and every week end.
    these replicates are pooled together and the mean and std error are computed.
    means and std errors are divided by the mean of UNC soil to normalize the results.

    """

    # data and plotting parameters
    CATEGORIES_DATA = raw_data_sets.values()
    CATEGORIES = raw_data_sets.keys()
    NUMBER_OF_CATEGORIES = len(raw_data_sets)
    LENGTH_OF_X = NUMBER_OF_CATEGORIES * spacing
    X_LOCATIONS = numpy.arange(0, LENGTH_OF_X, spacing)
    SOIL_WIDTH = spacing * relative_width

    # labels
    title = r'$BASELINE$'
    y_label = r'$\%\ increase$' + '\n' + r'$over\ UNC$'
    x_label = r'$soil\ features$'

    # figure
    basline_figure = pyplot.figure()

    basline_figure.subplots_adjust(hspace=0)

    # baseline_axes
    baseline_axes = make_bar_axes(
          figure=basline_figure,
          x_locations=X_LOCATIONS,
          soil_width=SOIL_WIDTH,
          title=title,
          y_label=y_label,
          x_label=x_label,
          categories=CATEGORIES
    )

    # plot bars for each category(=data_set)
    bars = {}
    for x_location, data_set, data_set_name in zip(X_LOCATIONS, #todo turn into a function
                                                   CATEGORIES_DATA, CATEGORIES):
        # baseline data
        baseline_statistics = get_baseline_stats(data_set)
        baseline_means = baseline_statistics.means

        normalization_factor = baseline_means['UNC']

        # bar plot input
        baseline_bar_heights = (baseline_means - normalization_factor) / normalization_factor * 100

        labels = SOILS

        # plot baseline
        baseline_bars = make_bars(baseline_axes, x_location,
                                  baseline_bar_heights, SOIL_WIDTH, labels)

        bars[data_set_name] = baseline_bars

    # legend
    legend_handles = [bars['MBC']['ORG'], bars['MBC']['MIN']]
    legend_labels = ['ORG', 'MIN']
    basline_figure.legend(
        legend_handles,
        legend_labels,
        loc='upper right',
        bbox_to_anchor=(1, 1),
        bbox_transform=baseline_axes.transAxes
    )

    # remove rectangle patch of UNC
    for category in CATEGORIES:
            bar = bars[category]['UNC']
            rectangle = bar.get_children()[0]
            rectangle.set_visible(False)

    # move the 'ERG' label above 0
    xtick_labels = baseline_axes.get_xmajorticklabels()
    erg_label = xtick_labels[-1]
    erg_label.set_position((1, 1))

    # plot a line for the height of UN

    return basline_figure, bars

if __name__ == '__main__':

    keys = Constants.parameters
    keys = list(set(keys) - set(['ERG', 'MBN', 'TON', 'RESP', 'DOC']))
    raw_data_sets = get_multi_sets(keys)
    figure, bars = plot_baseline(raw_data_sets, 2, 0.2)

# todo
#   get the zero line to continue to the edges
#   remove bottom spine and lower half of right spine
#       spines = ax.spines
#       bottom_spine = spines['bottom']
#       bottom_spine.set_position(('data', 0))
#       right_spine = spines['right']
#       right_spine.set_bounds(0,120)
#   change 'ERG-to-MBC' label into something shorter
#   bring this label to top