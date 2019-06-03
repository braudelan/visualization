import math

import numpy
from matplotlib import pyplot
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator, NullLocator
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from pandas import Series

from get_stats import get_stats
from helper_functions import get_week_ends

# pyplot parameters

# pyplot.style.use('seaborn-darkgrid')

pyplot.rc('legend',
          facecolor='inherit',
          framealpha=0,
          markerscale=1.5)
pyplot.rc('font', size=19) # control text size when not defined locally
pyplot.rc('lines', linewidth=5)

symbol_text_params = {'weight': 'bold',
                      'size': 26,
                      }

colors = ['xkcd:crimson', 'xkcd:aquamarine', 'xkcd:goldenrod']  #  todo colors (https://python-graph-gallery.com/line-chart/)
line_styles = densly_dashed, solid = ((0, (2, 1)), (0, ()))

major_locator = MultipleLocator(7)  # major ticks locations
minor_locator = MultipleLocator(1)  # minor ticks locations

# todo adjust plot_data for plotting a single axes (e.g. control)
# todo for MRE_&_normalized work on legend and x_label
# todo work on MRE_notation_marks()
def plot_data(data, data_SE, number, set_name, normalized=None):


    # local variables and parameter adjutments
    # excluded = normalized.iloc[1:, :]  # treatment effect without day 0


    # figure text

    last_day = data.index[-1]

    title_text = r'$\bf{Figure %s.}$ means of %s across %s days of incubation. (a) all soils, ' \
                 r'(b) normalized to control' % (number, set_name, last_day)

    xlabel_text = r'$incubation\ time\ \slash\ days$'

    if set_name == 'RESP':
        means_ylabel_text = r'$%s\ \slash\ mg\ CO_{2}-C\ \ast\ kg\ soil^{-1}\ \ast\ h^{-1} $' % set_name
    else:
        means_ylabel_text = r'$%s\ \slash\ mg \ast kg\ soil^{-1}$' % set_name

    normalized_ylabel_text = r'$%s\ normalized\ \slash\ percent\ of\ control$' % set_name


    # create and adjut figure
    treatment_figure = pyplot.figure(number, figsize=(25,20)) # todo better name for figure
    treatment_figure.tight_layout()
    treatment_figure.subplots_adjust(hspace=0)
    treatment_figure.suptitle(title_text, x=0.5, y=0, fontsize=22)

    # create means axes and set parameters
    means_axes = make_axes(treatment_figure, last_day, major_locator, minor_locator,
                                                          x_label='', y_label=means_ylabel_text, axes_lineup=1)

    # plot_means
    means_lines = plot_lines(means_axes, data, data_SE=data_SE) # todo take out specific data points (MBC)


    # create normalized axes and set parameters
    normalized_axes = make_axes(treatment_figure, last_day, major_locator, minor_locator,
                                                x_label=xlabel_text,y_label=normalized_ylabel_text, axes_lineup=2)

    # plot normalized
    normalized_lines = plot_lines(normalized_axes, normalized)

    # costumize legend
    list_lines = list(means_lines.items())  # item of the from e.g.  'ORG': <ErrorbarContainer object of 3 artists>
    lables = []
    handles = []
    for line in list_lines:
        label = line[0]
        handel = line[1]
        lables.append(label)
        handles.append(handel)
    treatment_figure.legend(handles, lables, loc='center right')  # todo remove error bars from legend objects.


    return treatment_figure


def make_axes(figure: Figure, last_day, major_locator, minor_locator, x_label='', y_label='', axes_lineup=0):

    position = (
                    111 if axes_lineup == 0 else
                    211 if axes_lineup == 1 else
                    212
                    )

    axes = figure.add_subplot(position)

    axes.set_xlim((0, last_day))
    axes.xaxis.set_minor_locator(minor_locator)
    axes.xaxis.set_major_locator(major_locator)
    axes.tick_params(axis='x', which='minor', width=1, length=3)
    set_ylabel = axes.set_ylabel(y_label, labelpad=30) if bool(y_label) == True else None
    set_xlabel = axes.set_xlabel(x_label) if bool(x_label) == True else None
    if axes_lineup == 2:
        MRE_notation_marks(axes)  # add arrows where MRE was applied
    if axes_lineup == 1:
        axes.get_xaxis().set_visible(False)

    return axes


def plot_lines(axes, data, data_SE=None):
    """
    plot a dataframe columns onto pyplot axes.

    each column is plotted using a seperate command with specific
    properties assigned to it (color, marker, linestyle, etc.).

    :parameter
    data(DataFrame):
            time series data.
            must have the time points as the [0] indexed column.
    stnd_error(DataFrame):
            standard error of data.
    axes():
            the axes where data will be plotted.
    :returns
    lines(dict):
        keys = names of data columns.
        values = pyplot line objects.

    """
    data.reset_index(inplace=True)

    x_data = data['days']
    y_data_labels = data.columns[1:]

    lines = {}
    for label in y_data_labels:
        soil_label = label

        y_data = data[label]
        y_error = data_SE[label] if data_SE is not None else None

        color = (
            colors[0] if (soil_label == 'ORG') else
            colors[1] if (soil_label == 'MIN') else
            colors[2]
        )
        # style = densly_dashed if treatment_label == 'c' else solid

        if data_SE is not None:
            ax = axes.errorbar(
                x_data,
                y_data,
                yerr=y_error,
                label=label,
                color=color,
            )  # todo add merkers? conflict with error bars
        else:
            ax = axes.plot(
                x_data,
                y_data,
                label=label,
                color=color,
            )  # todo add merkers? conflict with error bars

        lines[label] = ax

    return lines


def MRE_notation_marks(axes):  # todo work on notation marks. use matplotlib.patches.FancyArrowPatch instead of annotate

    MRE_time_points = [0, 7, 14 ] # days when MRE was applied
    offset_head_x = 0.2 # offset of arrow head x coordinate from annotation point, given in data coordinates(=days)
    arrow_angle = 0.4 # radians from a downwards line perpendicular to x axis
    offset_base_x = 0.2 + math.sin(arrow_angle) # offset of arrow base
    head_y = -0.02 # fraction of axes size
    base_y = -0.1 # fraction of axes size

    arrow_properties = dict(
                            arrowstyle='wedge',
                            facecolor='r',
                            mutation_scale=1.2,
                           )

    for time_point in MRE_time_points:
      axes.annotate(
                    s='',
                    xy=(time_point - offset_head_x, head_y ), # arrow head coordinates
                    xytext=(time_point - offset_base_x, base_y), # arrow base coordinates
                    xycoords=('data', 'axes fraction'),
                    arrowprops=arrow_properties,
                    )


def plot_baseline(raw_data_sets: dict) -> dict:
    """plot baseline values of multiple data sets on a bar plot"""

    # data parameters
    CATEGORIES = raw_data_sets.keys()
    N = len(raw_data_sets)
    X_LOCATIONS = numpy.arange(N)
    CATEGORIES_DATA = raw_data_sets.values()

    # axes parameters
    category_width = 0.5
    soil_width = category_width / 3

    # text
    y_label = r'normalized means \\' + '\n' + 'percent of smallest mean'

    # figure
    baseline_figure = pyplot.figure(figsize=(15,10))

    # axes
    axes = baseline_figure.add_subplot(111)

    axes.set_xticks(X_LOCATIONS + category_width/2)
    axes.set_xticklabels(CATEGORIES)
    axes.set_ylabel(y_label, rotation=45, position=(20, 0.65), ha='right')
    axes.set_yticks([])

    all_bars = {}
    for x_location, raw_data in zip(X_LOCATIONS, CATEGORIES_DATA):

        # data
        data = get_stats(raw_data).control  # get means of control samples
        data_
        week_ends = data.loc[get_week_ends(data)]  # drop week days
        means = week_ends.mean()  # average across day 1 and all week ends for every soil
        normalization_factor = means.min()
        normalized_control = means / normalization_factor * 100

        heights = normalized_control.values
        soil_labels = means.index

        category_bars = {}
        i = 0

        # plot
        for label, value in zip(soil_labels, heights):
            bar = axes.bar(x=x_location + i,
                           height=value,
                           width=soil_width,
                           label=label,
                           color=(
                               colors[0] if (label == 'ORG') else
                               colors[1] if (label == 'MIN') else
                               colors[2]
                           )
                           )

            i += soil_width

            category_bars[label] = bar
        # plot_baseline_bars(axes, data_set, data_set_name, x_location)

    return baseline_figure


def plot_baseline_bars(axes, data_set, data_set_name, x_location):

    data_set = get_stats(data_set).control  # get means of control samples
    week_ends = data_set.loc[get_week_ends(data_set)]  # drop week days
    control_averages = week_ends.mean()  # average across day 1 and all week ends for every soil
    max_value = control_averages.max()
    normalized_control = control_averages / max_value * 100

    width = 0.3
    category = data_set_name

    heights = normalized_control.values
    labels = control_averages.index

    category_bars={}
    i = 0
    width_indent = width/3
    for label, value in zip(labels, heights):

        bar = axes.bar(x=x_location + i,
                       height=value,
                       width=width_indent,
                       label=label,
                       color= (
                               colors[0] if (label == 'ORG') else
                               colors[1] if (label == 'MIN') else
                               colors[2]
                              )
                       )

        i += width_indent

        category_bars[label] = bar

    return category_bars

def plot_c_to_n(data):

    carbon_figure = pyplot.figure(figsize=(15,10))

    axes = carbon_figure.add_subplot(111)

    axes.xaxis.set_minor_locator(minor_locator)
    axes.xaxis.set_major_locator(major_locator)
    axes.tick_params(axis='x', which='minor', width=1, length=3)

    lines = data.plot(ax=axes)

    return carbon_figure