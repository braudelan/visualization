import pdb
import math

import numpy
from numpy import exp
from pandas import DataFrame
from matplotlib import pyplot
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator, NullLocator
from matplotlib.figure import Figure
from matplotlib.axes import Axes
# from scipy.optimize import curve_fit
# from sklearn.metrics import r2_score
# from pandas import Series

from stats import get_stats, get_baseline
from helpers import Constants


# constants
SOILS = Constants.soils
MARKERS = Constants.markers
COLORS = Constants.colors
# pyplot parameters

# pyplot.style.use('ggplot')

pyplot.rc(
          'legend',
          facecolor='inherit',
          framealpha=0,
          markerscale=2
  )

pyplot.rc('font', size=19) # control text size when not defined locally
pyplot.rc('lines', linewidth=5)
# pyplot.rc('marker', size=5)

symbol_text_params = {'weight': 'bold',
                      'size': 26,
                      }

line_styles = densly_dashed, solid = ((0, (2, 1)), (0, ()))

major_locator = MultipleLocator(7)  # major ticks locations
minor_locator = MultipleLocator(1)  # minor ticks locations


# todo adjust plot_dynamics for plotting a single axes (e.g. control)
# todo for MRE_&_normalized work on legend and x_label
# todo work on MRE_notation_marks()
# todo change rcparams for marker size to stand

def make_figure(data, number, data_set_name):

    # figure text
    last_day = data.index[-1]

    title_text = r'$\bf{Figure %s.}$ means of %s across %s days of incubation. (a) all soils, ' \
                 r'(b) normalized to control' % (number, data_set_name, last_day)

    # create and adjut figure
    figure = pyplot.figure(number, figsize=(20, 15))  # todo better name for figure
    figure.tight_layout()
    figure.subplots_adjust(hspace=0)
    figure.suptitle(title_text, x=0.5, y=0, fontsize=22)

    return figure


def make_line_axes(figure: Figure, last_day, major_locator, minor_locator, x_label='', y_label='', axes_lineup=0) -> Axes:

    # allocate position of axes in figure (0=single axes, 1=first out of two, else=second out of two)
    position = (
                    111 if axes_lineup == 0 else
                    211 if axes_lineup == 1 else
                    212
                    )

    axes = figure.add_subplot(position)

    axes.set_xlim((0, last_day))
    # axes.set_ylim(0, max_value)
    axes.xaxis.set_minor_locator(minor_locator)
    axes.xaxis.set_major_locator(major_locator)
    axes.tick_params(axis='x', which='minor', width=1, length=3)
    axes.set_ylabel(y_label, labelpad=30) if bool(y_label) == True else None

    if axes_lineup == 2 or axes_lineup == 0:
        MRE_notation_marks(axes)  # add arrows where MRE was applied
    if axes_lineup == 1:
        axes.get_xaxis().set_visible(False)

    return axes


def make_lines(axes, data, stde=None):


    """
    plot dataframe columns onto pyplot axes.

    each column is plotted using a seperate command with specific
    properties assigned to it (color, marker, linestyle, etc.).

    :parameter
    data(DataFrame):
            time series.
            must have the time series index as the [0] indexed column.
    stnd_error(DataFrame):
            standard error of data with same shape as data.
    axes():
            the axes where data will be plotted.
    :returns
    lines(dict):
        keys = names of data columns.
        values = pyplot line objects.

    """

    # turn index 'days' into first column
    data.reset_index(inplace=True)

    x_data = data['days']
    y_data_labels = data.columns[1:] # exclude 'days' column

    lines = {}
    for soil_label in y_data_labels:

        y_data = data[soil_label]
        y_error = stde[soil_label] if stde is not None else None

        # style = densly_dashed if treatment_label == 'c' else solid

        if stde is not None:
            line = axes.errorbar(
                               x_data,
                               y_data,
                               yerr=y_error,
                               label=soil_label,
                               color=COLORS[soil_label],
                               marker=MARKERS[soil_label],
                               )  # todo add merkers? conflict with error bars
        else:
            line = axes.plot(
                           x_data,
                           y_data,
                           label=soil_label,
                           color=COLORS[soil_label],
                           marker=MARKERS[soil_label]
                          )  # todo add merkers? conflict with error bars


        lines[soil_label] = line

    return lines


def plot_dynamics(figure, data, stde, set_name, axes_lineup, stdv=None):

    last_day = data.index[-1]
    is_normalized = True if axes_lineup == 2 else False # check if the data being plotted is normalized

    # text
    xlabel_text = r'$incubation\ time\ \slash\ days$'
    normalized = 'normalized' if is_normalized else ''
    if set_name == 'RESP':
        ylabel_text = r'$%s\ %s\ mg\ CO_{2}-C\ ' \
                      r'\ast\ kg\ soil^{-1}\ \ast\ day^{-1} $' %(normalized, set_name)
    else:
        ylabel_text = r'$%s\ %s\ \slash\ mg' \
                      r' \ast kg\ soil^{-1}$' %(normalized, set_name)

    # create means axes and set parameters
    axes = make_line_axes(figure, last_day, major_locator, minor_locator,
                                    x_label='', y_label=ylabel_text, axes_lineup=axes_lineup)

    # shared x label for figure with two plots
    if axes_lineup == 2 or axes_lineup == 0:
        axes.set_xlabel(xlabel_text, labelpad=40)

    # plot data on axes
    lines = make_lines(axes, data, stde) # todo take out specific data points    (MBC)

    # customize legend
    list_lines = list(lines.items())  #e.g.'ORG': <ErrorbarContainer object of 3 artists>
    lables = []
    handles = []
    for line in list_lines:
        label = line[0]
        handel = line[1]
        lables.append(label)
        handles.append(handel)
    figure.legend(handles, lables, loc='center right')  # todo remove error bars from legend objects.


def MRE_notation_marks(axes):

    MRE_TIME_POINTS = [0, 7, 14 ] # days when MRE was applied

    arrow_angle = 0.7 # radians from a downwards line perpendicular to x axis
    offset_head_x = 0.3 # offset of arrow head from annotation point, given in data coordinates(=days)
    offset_base_x = offset_head_x + math.sin(arrow_angle) # offset of arrow base
    head_y = -0.03 # fraction of axes size
    base_y = head_y -0.07 # fraction of axes size

    arrow_properties = dict(
                            arrowstyle="wedge,tail_width=0.7",
                            fc="0.6",
                            ec="0.1",
                            # connectionstyle="arc3,rad=0.5"
                           )

    for time_point in MRE_TIME_POINTS:

      # axes.annotate(
      #               s='',
      #               xy=(time_point - offset_head_x, head_y ), # arrow head coordinates
      #               xytext=(time_point - offset_base_x, base_y), # arrow base coordinates
      #               xycoords=('data', 'axes fraction'),
      #               arrowprops=arrow_properties,
      #               )
      axes.annotate(
                    s='',
                    xy=(time_point - offset_head_x, head_y ), # arrow head coordinates
                    xytext=(time_point - offset_base_x, base_y), # arrow base coordinates
                    xycoords=('data','axes fraction'),
                    textcoords=('data', 'axes fraction'),
                    arrowprops=(arrow_properties)
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
        MRE_means = get_stats(data_set, 't').MRE
        MRE_SD = get_stats(data_set, 't').MRE_SD
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
                                  baseline_bar_heights, SOIL_WIDTH, labels, baseline_bar_errors)

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