from typing import Tuple, Dict

import numpy
from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from data.raw_data import get_multi_sets
from data.stats import get_baseline_stats
from data.helpers import Constants

SOILS = Constants.LTTs
COLORS = Constants.colors

PLOT_STYLE = 'seaborn-ticks'
pyplot.style.use(PLOT_STYLE)

TITLE_PAD = 20
XLABEL_PAD = 20
YLABEL_PAD = 25
TICK_LABEL_SIZE = 12
AXIS_LABEL_SIZE = 14


def make_bar_axes(figure: Figure,x_locations, soil_width, title,
                       y_label, x_label=None, categories=None) -> Axes:


    axes: Axes = figure.add_subplot(111)

    # spines
    spines = axes.spines
    spines['bottom'].set_position('zero')
    spines['right'].set_bounds(low=0, high=150)

    # labels
    axes.set_title(title, pad=TITLE_PAD)
    axes.set_ylabel(
        y_label,
        rotation=90,
        verticalalignment='center',
        labelpad=YLABEL_PAD,
        fontsize= AXIS_LABEL_SIZE
    )
    if x_label:
        axes.set_xlabel(
            x_label,
            fontsize=AXIS_LABEL_SIZE,
            labelpad=XLABEL_PAD
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
        rotation=0
    )

    # y ticks
    major_yticks = numpy.arange(-50, 150,50)
    axes.set_yticks(major_yticks)
    minor_yticks = numpy.arange(-100, 100, 10)
    axes.set_yticks(minor_yticks, minor=True)
    axes.yaxis.set_tick_params(labelsize=TICK_LABEL_SIZE)
    axes.set_ylim(-80, 150)


    # # plot a line at y=zero, indicating the refernce level (=UNC)
    # xlim = axes.get_xlim()
    # lower_x = xlim[0]
    # upper_x = xlim[1]
    # x = numpy.arange(lower_x, upper_x)
    # y = numpy.zeros(len(x))
    # axes.plot(
    #     x,
    #     y,
    #     linewidth=0.8,
    #     color='black',
    # )

    return axes

def plot_bars(axes: Axes, x_location, heights, width, labels, bar_error=None):

    bars = {}
    i = 0
    for soil_label, height in zip(labels, heights):
        if bar_error is not None:
            error_kw = {
                'elinewidth': 0.8
            }
            bar = axes.bar(
                   x=x_location + i,
                   height=height,
                   width=width,
                   yerr=bar_error[soil_label],
                   label=soil_label,
                   color=COLORS[soil_label],
                   edgecolor='k',
                   capsize=2,
                   error_kw=error_kw
            )
        else:
            bar = axes.bar(
                   x=x_location + i,
                   height=height,
                   width=width,
                   label=soil_label,
                   color=COLORS[soil_label],
                   edgecolor = 'k'
            )

        i += width

        bars[soil_label] = bar

    return bars


def plot_baseline(raw_data_sets: dict,
                  spacing, relative_width,
                  labels: list=None) -> Tuple[Figure, Dict[str, dict]]:
    """plot baseline values of multiple data sets."""

    # data and plotting parameters
    CATEGORIES_DATA = raw_data_sets.values()
    CATEGORIES = raw_data_sets.keys()
    LABELS = labels
    NUMBER_OF_CATEGORIES = len(raw_data_sets)
    LENGTH_OF_X = NUMBER_OF_CATEGORIES * spacing
    X_LOCATIONS = numpy.arange(0, LENGTH_OF_X, spacing)
    SOIL_WIDTH = spacing * relative_width

    # labels
    title = r'$BASELINE$'
    y_label = r'$\%\ increase$' + '\n' + r'$over\ UNC$'
    x_label = r'$soil\ features$'

    # figure
    figure = pyplot.figure()

    figure.subplots_adjust(hspace=0)

    # baseline_axes
    axes = make_bar_axes(
          figure=figure,
          x_locations=X_LOCATIONS,
          soil_width=SOIL_WIDTH,
          title=title,
          y_label=y_label,
          categories=labels
    )

    # plot bars for each category(=data_set)
    bars = {}
    for x_location, data_set, data_set_name in zip(X_LOCATIONS, #todo turn into a function
                                                   CATEGORIES_DATA, CATEGORIES):
        # baseline data
        statistics = get_baseline_stats(data_set)
        means = statistics.means
        stde = statistics.stde

        mean_unc = means['UNC']
        stde_unc = stde['UNC']

        # bar heights
        subtract = means - mean_unc
        divide = (subtract) / mean_unc
        bar_heights = divide * 100

        # bar errors
        rel_err_unc = stde_unc / mean_unc
        err_sub = (stde**2 + stde_unc**2)**0.5
        rel_err_sub = err_sub / subtract
        rel_err_div = (rel_err_sub**2 + rel_err_unc**2)**0.5
        err_div = rel_err_div *divide
        bar_errors = err_div * 100
        bar_errors['UNC'] = bar_errors['MIN'] * 0.5677

        labels = SOILS

        # plot baseline
        baseline_bars = plot_bars(axes, x_location,
                                  bar_heights, SOIL_WIDTH, labels, bar_error=bar_errors)

        bars[data_set_name] = baseline_bars

    # remove rectangle patch of UNC
    for category in CATEGORIES:
            bar = bars[category]['UNC']
            rectangle = bar.get_children()[0]
            rectangle.set_visible(False)

    xtick_labels = axes.get_xmajorticklabels()

    # move the 'ERG' label above 0
    erg_label = xtick_labels[-1]
    erg_label.set_position((8.0, 40))
    erg_label.set_fontsize(16)

    # reposition other x tick labels
    xtick_labels.pop()
    other_xtick_labels = xtick_labels  # remove 'ERG' tick label
    for label in other_xtick_labels:
        old_x = label.get_position()[0]
        new_x = old_x - 0.2
        new_y = -10
        label.set_position((new_x, new_y))

    # x label
    axes.set_xlabel(x_label, labelpad=25, fontsize=AXIS_LABEL_SIZE)

    # color bottom spine with 'UNC' color and make wider
    unc_patch = bars['MBC']['UNC'][0]
    unc_color = unc_patch.get_facecolor()

    bottom_spine = axes.spines['bottom']
    bottom_spine.set_color(unc_color)
    bottom_spine_width = bottom_spine.get_linewidth()
    increase_width_by = 2
    new_width = bottom_spine_width * increase_width_by
    bottom_spine.set_linewidth(new_width)
    bottom_spine.set_zorder(1)

    # add a legend entry for the bottom spine (representing 'UNC')
    spine_handle = Line2D([1, 2, 3], [0, 0, 0],
                   linewidth=new_width, color=unc_color)

    # legend
    legend_handles = [bars['MBC']['ORG'], bars['MBC']['MIN'], spine_handle]
    legend_labels = ['ORG', 'MIN', 'UNC']
    figure.legend(
        legend_handles,
        legend_labels,
        loc='upper right',
        bbox_to_anchor=(1, 1),
        bbox_transform=axes.transAxes,
        fontsize=12,
    )

    return figure, bars

def baseline_table(baseline_means,
                   baseline_significance, output_dir):

    


if __name__ == '__main__':


    keys = Constants.parameters
    keys = ['TOC', 'MBC', 'RESP', 'DOC', 'HWS', 'AS', 'ERG']
    labels = []
    raw_data_sets = get_multi_sets(keys)
    figure, bars = plot_baseline(raw_data_sets, 2, 0.2, labels = keys)

# todo
#   change 'ERG-to-MBC' label into something shorter
