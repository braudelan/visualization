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

from stats import get_stats, get_baseline
from helpers import Constants


SOILS = Constants.soils
MARKERS = Constants.markers
COLORS = Constants.colors

# pyplot configuration

pyplot.rc(
          'legend',
          facecolor='inherit',
          framealpha=0,
          markerscale=2
  )

pyplot.rc('font', size=15) # control text size when not defined locally
pyplot.rc('lines', linewidth=5)
# pyplot.rc('marker', size=5)
# pyplot.style.use('ggplot')'

symbol_text_params = {'weight': 'bold',
                      'size': 26,
                      }

line_styles = densly_dashed, solid = ((0, (2, 1)), (0, ()))

MAJOR_LOCATOR = MultipleLocator(7)  # major ticks locations
MINOR_LOCATOR = MultipleLocator(1)  # minor ticks locations


def MRE_notation_marks(axes: Axes):

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


def make_line_axes(figure: Figure, data, axes_lineup=0) -> Axes:
    '''add an axes with basic configuration to a given figure.'''

    last_day = data.index[-1]
    max_value = data.max().max() # highest value measured in any of the soils
    percent_extra_space = 0.2
    upper_ylim = max_value + max_value * percent_extra_space

    # allocate position of axes in figure (0=single axes, 1=first out of two, else=second out of two)
    position = (
                    111 if axes_lineup == 0 else
                    211 if axes_lineup == 1 else
                    212
                    )

    axes: Axes = figure.add_subplot(position)

    axes.set_xlim(0, last_day)
    axes.set_ylim(0, upper_ylim)
    axes.xaxis.set_minor_locator(MINOR_LOCATOR)
    axes.xaxis.set_major_locator(MAJOR_LOCATOR)
    axes.tick_params(axis='x', which='minor', width=1, length=3)

    return axes


def make_lines(axes: Axes, data, stde=None):


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


def plot_dynamics(figure: Figure, data,
                  stde, set_name, axes_lineup):

    last_day = data.index[-1]
    is_normalized = True if axes_lineup == 2 else False # check if the data being plotted is normalized

    # text
    xlabel_text = r'$incubation\ time\ \slash\ days$'
    normalized = 'normalized' if is_normalized else ''
    if set_name == 'RESP':
        ylabel_text = r'$%s\ %s\ \slash$' '\n' r'$mg\ CO_{2}-C\ $'  \
                      r'$\ast\ kg\ soil^{-1}\ \ast\ day^{-1} $' %(normalized, set_name)
    else:
        ylabel_text = r'$%s\ %s\ \slash$' '\n' \
                      r'$mg\ \ast kg\ soil^{-1}$' %(normalized, set_name)

    ylabel_rotation = 65 if set_name == 'RESP' else 45

    # create axes
    axes = make_line_axes(figure, data, axes_lineup=axes_lineup)

    # plot data on axes
    lines = make_lines(axes, data, stde) # todo take out specific data points    (MBC)

    # customize axes
    if axes_lineup == 2 or axes_lineup == 0:
        axes.set_xlabel(xlabel_text, labelpad=40) # x label
        MRE_notation_marks(axes)  # add arrows where MRE was applied
    if axes_lineup == 1:
        axes.get_xaxis().set_visible(False)

    axes.set_ylabel(ylabel_text, labelpad=50,
                    rotation=ylabel_rotation)

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

def plot_control_composite(raw_data_sets):

    # get the data
    raw_data_names = raw_data_sets.keys()
    raw_data = raw_data_sets.values()
    zipped = zip(raw_data_names, raw_data)

    control_data_sets = {}
    for name, data in zipped:
        stats = get_stats(data, 'c')
        means = stats.means
        control_data_sets[name] = means

    # arrays to iterate over
    control_data_names = control_data_sets.keys()
    control_data = control_data_sets.values()
    control_zipped = zip(control_data_names, control_data)

    # make figure
    n_data_sets = len(raw_data_sets)
    is_even = True if n_data_sets % 2 == 0 else False
    n_rows = 4 #n_data_sets / 2 #if is_even else 3
    n_columns = 4 #n_rows #if is_even else 3

    figure, axes = pyplot.subplots(n_rows, n_columns)

    for name, data in control_zipped:
        for n in range(n_data_sets):
            for soil in SOILS:
                x = data.index
                y = data.loc[:,soil]
                axes[n].plot(x, y)

    return figure


def make_bar_axes(figure: Figure, x_locations, soil_width, y_label,
                                                x_label=None, categories=None) -> Axes:

    # position = (
    #             111 if axes_lineup == 0 else
    #             211 if axes_lineup == 1 else
    #             212
    #            )

    axes: Axes = figure.add_subplot(111)

    axes.set_ylabel(y_label, rotation=45, position=(20, 0.65), ha='right', ma='center')
    axes.set_xlabel(x_label)
    axes.set_yticks([])
    axes.set_xticks(x_locations + soil_width)
    axes.set_xticklabels(categories)
    axes.xaxis.set_tick_params(length=1, pad=20)

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


def plot_baseline(raw_data_sets: dict) -> Figure: #todo: horizontal line instead of 'UNC' bars, x_label
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
    baseline_y_label = r'$mean\ baseline\ value\ \slash$'\
                       + '\n' + r'$\%\ of\ UNC$'
    x_label = 'soil properties'

    # figure
    basline_figure = pyplot.figure(figsize=(15,10))

    basline_figure.subplots_adjust(hspace=0)

    # baseline_axes
    baseline_axes = make_bar_axes(basline_figure,
                                  X_LOCATIONS, SOIL_WIDTH,
                                  baseline_y_label,
                                  categories=CATEGORIES
                                  )

    bars = {}
    for x_location, data_set, category_name in zip(X_LOCATIONS, #todo turn into a function
                                                   CATEGORIES_DATA,
                                                   CATEGORIES):
        # baseline data
        baseline_statistics = get_baseline(data_set)
        BASELINE = baseline_statistics[0]
        BASELINE_STDE = baseline_statistics[2]

        NORMALIZATION_FACTOR = BASELINE['UNC']

        # bar plot input
        baseline_bar_heights = BASELINE / NORMALIZATION_FACTOR
        baseline_bar_errors = BASELINE_STDE / NORMALIZATION_FACTOR

        # growth_bar_heights = growth / baseline

        labels = SOILS

        # plot baseline
        baseline_bars = make_bars(baseline_axes, x_location,
                                  baseline_bar_heights, SOIL_WIDTH, labels, baseline_bar_errors)

        bars[category_name] = baseline_bars
        # bars[category_name + '_growth'] = growth_bars

    # legend
    legend_handles = bars['MBC'].values()
    legend_labels = bars['MBC'].keys()
    basline_figure.legend(legend_handles, legend_labels, loc='center right')

    # remove rectangle patch of UNC
    for category in CATEGORIES:
        for soil in SOILS:
            if soil == 'UNC':
                bar = bars[category][soil]
                bar_rectangle = bar.patches
                bar_rectangle.clear()

    return basline_figure


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

    axes.xaxis.set_minor_locator(MINOR_LOCATOR)
    axes.xaxis.set_major_locator(MAJOR_LOCATOR)
    axes.tick_params(axis='x', which='minor', width=1, length=3)

    lines = data.plot(ax=axes)

    return carbon_figure