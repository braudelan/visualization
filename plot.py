import pdb
import math

import numpy
from matplotlib import pyplot
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator, NullLocator
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from pandas import Series

from get_stats import get_stats, get_baseline
from helpers import get_week_ends, SOILS

# constants
# SOILS = ['ORG', 'MIN', 'UNC']

# pyplot parameters

# # pyplot.style.use('seaborn-darkgrid')

pyplot.rc('legend',
          facecolor='inherit',
          framealpha=0,
          markerscale=2)
pyplot.rc('font', size=19) # control text size when not defined locally
pyplot.rc('lines', linewidth=3)
# pyplot.rc('marker', size=5)

symbol_text_params = {'weight': 'bold',
                      'size': 26,
                      }

COLORS = ['xkcd:crimson', 'xkcd:aquamarine', 'xkcd:goldenrod']  #  todo colors (https://python-graph-gallery.com/line-chart/)
MARKERS = ['h', '*', 'D']
line_styles = densly_dashed, solid = ((0, (2, 1)), (0, ()))

major_locator = MultipleLocator(7)  # major ticks locations
minor_locator = MultipleLocator(1)  # minor ticks locations

# todo adjust plot_dynamics for plotting a single axes (e.g. control)
# todo for MRE_&_normalized work on legend and x_label
# todo work on MRE_notation_marks()
# todo change rcparams for marker size to stand
def plot_dynamics(data, data_SE, number, set_name, normalized=None):


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
    treatment_figure = pyplot.figure(number, figsize=(20,15)) # todo better name for figure
    treatment_figure.tight_layout()
    treatment_figure.subplots_adjust(hspace=0)
    treatment_figure.suptitle(title_text, x=0.5, y=0, fontsize=22)

    # create means axes and set parameters
    means_axes = make_line_axes(treatment_figure, last_day, major_locator, minor_locator,
                                x_label='', y_label=means_ylabel_text, axes_lineup=1)

    # plot_means
    means_lines = plot_lines(means_axes, data, data_SE=data_SE) # todo take out specific data points (MBC)


    # create normalized axes and set parameters
    normalized_axes = make_line_axes(treatment_figure, last_day, major_locator, minor_locator,
                                     x_label=xlabel_text, y_label=normalized_ylabel_text, axes_lineup=2)

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


def make_line_axes(figure: Figure, last_day, major_locator, minor_locator, x_label='', y_label='', axes_lineup=0) -> Axes:

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
                 COLORS[0] if (soil_label == 'ORG') else
                 COLORS[1] if (soil_label == 'MIN') else
                 COLORS[2]
                )

        marker = (
                  MARKERS[0] if (soil_label == 'ORG') else
                  MARKERS[1] if (soil_label == 'MIN') else
                  MARKERS[2]
                 )

        # style = densly_dashed if treatment_label == 'c' else solid

        if data_SE is not None:
            line = axes.errorbar(
                               x_data,
                               y_data,
                               yerr=y_error,
                               label=label,
                               color=color,
                               marker=marker,
                               )  # todo add merkers? conflict with error bars
        else:
            line = axes.plot(
                           x_data,
                           y_data,
                           label=label,
                           color=color,
                           marker=marker
                          )  # todo add merkers? conflict with error bars


        lines[label] = line

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


def plot_all_parameters(raw_data_sets: dict) -> Figure:
    """plot baseline values of multiple data sets.

    this function takes only the control replicates from every data set(=category or analysis)
    and produces the average for every soil over day 0 and every week end.
    all replicates from all sampling days are pooled together representing replicates of the same sample
    and the mean and std error are calculated accordingly.
    means and std errors are divided by the mean of UNC soil to normalize the results.

    """

    # data parameters
    CATEGORIES = raw_data_sets.keys()
    N = len(raw_data_sets)
    X_LOCATIONS = numpy.arange(N)
    CATEGORIES_DATA = raw_data_sets.values()

    # plot parameters
    CATEGORY_WIDTH = 0.5
    SOIL_WIDTH = CATEGORY_WIDTH / 2

    # labels
    baseline_y_label = r'normalized means \\' + '\n' + 'percent of smallest mean'
    growth_y_label = ''
    x_label = ''

    # figure
    basline_growth_figure = pyplot.figure(figsize=(15,10))

    basline_growth_figure.subplots_adjust(hspace=0)

    # baseline_axes
    baseline_axes = make_bar_axes(basline_growth_figure, X_LOCATIONS, SOIL_WIDTH, baseline_y_label, axes_lineup=1)

    # growth axes
    growth_axes = make_bar_axes(basline_growth_figure, X_LOCATIONS, SOIL_WIDTH, growth_y_label,
                                                        x_label=x_label, categories= CATEGORIES, axes_lineup=2)
    all_bars = {}
    for x_location, data_set, category_name in zip(X_LOCATIONS, CATEGORIES_DATA, CATEGORIES):


        # baseline data
        baseline_statistics = get_baseline(data_set)
        baseline = baseline_statistics[0]
        baseline_SD = baseline_statistics[1]
        baseline_SE = baseline_statistics[2]

        normalization_factor = baseline['UNC']

        # total growth data
        MRE_means = get_stats(data_set).MRE
        MRE_SD = get_stats(data_set).MRE_SD
        last_day_mean = MRE_means.iloc[-1]
        last_day_SD = MRE_SD.iloc[-1]
        growth = last_day_mean - baseline
        growth_SD = (baseline_SD ** 2 + last_day_SD ** 2) ** 0.5


        # bar plot input
        baseline_bar_heights = baseline / normalization_factor
        baseline_bar_errors = baseline_SE / normalization_factor

        growth_bar_heights = growth / baseline

        labels = SOILS

        # plot baseline
        baseline_bars = {}
        baseline_bars = plot_bars(baseline_axes, x_location,
                                        baseline_bar_heights, SOIL_WIDTH, SOILS , baseline_bar_errors)

        # plot growth
        growth_bars = plot_bars(growth_axes, x_location, growth_bar_heights, SOIL_WIDTH, labels, )

        all_bars[category_name + '_baseline'] = baseline_bars
        all_bars[category_name + '_growth'] = growth_bars

    legend_handles = all_bars['MBC_growth'].values()
    legend_labels = all_bars['MBC_growth'].keys()
    basline_growth_figure.legend(legend_handles, legend_labels, loc='center right')                                                                                   # baseline_category_names = [ key for key in all_bars.keys() if 'baseline' in key]
                                                                                        ## remove rectangle patch of UNC
    return basline_growth_figure                                                       # for category in baseline_category_names:
                                                                                        #     for soil in all_bars[category].keys():
                                                                                        #         if soil == 'UNC':
                                                                                        #             bar = all_bars[category][soil]
                                                                                        #             bar_rectangle = bar.patchs
                                                                                        #             bar_rectangle.clear()


def make_bar_axes(figure: Figure, x_locations, soil_width, y_label,
                                                x_label=None, categories=None, axes_lineup=0) -> Axes:

    position = (
                111 if axes_lineup == 0 else
                211 if axes_lineup == 1 else
                212
               )

    axes = figure.add_subplot(position)

    axes.set_ylabel(y_label, rotation=45, position=(20, 0.65), ha='right')
    axes.set_yticks([])

    if categories is not None:
        axes.set_xticks(x_locations + soil_width)
        axes.set_xticklabels(categories)
        axes.xaxis.set_tick_params(length=1, pad=20)
        axes.set_xlabel(x_label)
    else:
        axes.set_xticks([])

    return axes

def plot_bars(axes: Axes, x_location, heights, width, labels, bar_error=None):

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
                           color=(
                                  COLORS[0] if (soil_label == 'ORG') else
                                  COLORS[1] if (soil_label == 'MIN') else
                                  COLORS[2]
                                 )
                           )
        else:
            bar = axes.bar(
                           x=x_location + i,
                           height=height,
                           width=width,
                           label=soil_label,
                           color=(
                                  COLORS[0] if (soil_label == 'ORG') else
                                  COLORS[1] if (soil_label == 'MIN') else
                                  COLORS[2]
                                 ),
                           )

        i += width

        bars[soil_label] = bar

    return bars


def plot_total_increase(raw_data_sets: dict) -> Figure:

    for data_set_name, data_set in raw_data_sets.items():

        # baseline
        baseline = get_baseline(data_set)[0]
        baseline_std_error = get_baseline(data_set)[1]

        # last day of incubation
        MRE_means = get_stats(data_set).MRE
        MRE_std_error = get_stats(data_set).MRE_SE
        last_day_means = MRE_means.iloc[-1]
        last_day_std_error = MRE_std_error.iloc[-1]

        # total increase
        baseline_increase = last_day_means - baseline
        normalized = baseline_increase / baseline





def plot_c_to_n(data):

    carbon_figure = pyplot.figure(figsize=(15,10))

    axes = carbon_figure.add_subplot(111)

    axes.xaxis.set_minor_locator(minor_locator)
    axes.xaxis.set_major_locator(major_locator)
    axes.tick_params(axis='x', which='minor', width=1, length=3)

    lines = data.plot(ax=axes)

    return carbon_figure