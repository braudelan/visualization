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


SOILS = Constants.groups
MARKERS = Constants.markers
COLORS = Constants.colors
LINE_STYLES = Constants.line_styles

MAJOR_LOCATOR = MultipleLocator(7)  # major ticks locations
MINOR_LOCATOR = MultipleLocator(1)  # minor ticks locations

pyplot.rc(
          'legend',
          facecolor='inherit',
          framealpha=0,
          markerscale=2
  )

pyplot.rc('font', size=15) # control text size when not defined locally
pyplot.rc('lines', linewidth=3)

# palette = pyplot.get_cmap('tab10')
pyplot.style.use('seaborn-talk')



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


def make_figure(data=None, number=None, data_set_name=None):


    # last_day = data.index[-1]

    # title_text = r'$\bf{Figure %s.}$ means of %s across %s days of incubation. (a) all soils, ' \
    #              r'(b) normalized to control' % (number, data_set_name, last_day)

    title_text = data_set_name
    # create and adjut figure
    figure = pyplot.figure(number, figsize=(20, 15))
    figure.tight_layout()
    figure.subplots_adjust(hspace=0)
    figure.suptitle(title_text, x=0.5, y=0, fontsize=22)

    return figure


def make_axes(figure: Figure,
                axes_position='single') -> Axes:
    '''create and configure axes'''

    # allocate position of axes in figure
    position = (
                    111 if axes_position == 'single' else
                    211 if axes_position == 'top of 2' else
                    311 if axes_position == 'top of 3' else
                    312 if axes_position == 'middle' else
                    313 if axes_position == 'bottom of 3' else
                    212
            )
    # intialize axes
    axes: Axes = figure.add_subplot(position)

    # axes parameters
    axes.xaxis.set_minor_locator(MINOR_LOCATOR)
    axes.xaxis.set_major_locator(MAJOR_LOCATOR)
    axes.tick_params(axis='x', which='minor', width=1, length=3)
    axes.margins(x=0.03, y=0.1)

    return axes


def plot_lines(axes: Axes, data, linestyle='solid', stde=None):


    """
    plot dataframe columns onto pyplot axes.

    each column is plotted using a seperate command with specific
    properties assigned to it (color, marker, linestyle, etc.).


    :parameter
    axes():
            the axes where data will be plotted.
    data(DataFrame):
            time series.
    stnd_error(DataFrame):
            standard error of data with same shape as data.
    label(string):
            a string designating what kind of data is being ploted. for purpose of assigning
            a line style. can be one of 'control', 'treatment' or 'normalized'
    :returns
    lines(dict):
        keys = names of data columns.
        values = pyplot line objects.

    """

    # turn index 'days' into first column
    data.reset_index(inplace=True)

    x_data = data['days']

    lines = {}
    i=0
    for soil in SOILS:
        i += 1
        y_data = data[soil]
        y_error = stde[soil] if stde is not None else None

        line = axes.errorbar(
                           x_data,
                           y_data,
                           ls=LINE_STYLES[linestyle],
                           yerr=y_error,
                           label=soil,
                           color=COLORS[soil],
                           marker=MARKERS[soil],
        )

        lines[soil] = line

    return lines


def draw_labels(figure: Figure, axes: Axes,
                    y_label: str, label_rotation=90, axes_position='bottom'):

    # text and text parameters
    xlabel_text = r'$incubation\ time\ \slash\ days$'
    ylabel_text = y_label

    ylabel_rotation = label_rotation

    is_bottom = True if ('bottom' in axes_position or
                           axes_position == 'single') else False
    # MRE notation,
    if is_bottom:
        MRE_notation_marks(axes)  # add arrows where MRE was applied

    # remove x axis from top and middle axes
    if not is_bottom:
        axes.get_xaxis().set_visible(False)

    # x label
    figure.text(0.5, 0.03, xlabel_text, ha='center')
    # y label
    figure.text(0.05, 0.5, ylabel_text, va='center', rotation=ylabel_rotation)

    # legend
    axes.get_lines()
    handles = axes.get_lines()
    labels = SOILS
    figure.legend(handles, labels, 'center right')


def plot_control_composite(raw_data_sets):

    def configure_axes(axes: Axes):
        axes.margins(x=0.1, y=0.1)
        axes.xaxis.set_minor_locator(MINOR_LOCATOR)
        axes.xaxis.set_major_locator(MAJOR_LOCATOR)
        data_name = axes.get_label()
        axes.text(27, 0.8, data_name)
        axes.label_outer()

    # get the data
    data_names = raw_data_sets.keys()
    raw_data = raw_data_sets.values()
    zipped = zip(data_names, raw_data)

    control_means = {}
    stde = {}
    for name, data in zipped:

        treatment_stats = get_stats(data, 't')
        treatment_means = treatment_stats.means
        treatment_stde = treatment_stats.stde
        treatment_relative_stde = treatment_stde / treatment_means

        control_stats = get_stats(data, 'c')
        control_means = control_stats.means
        # max = control_means.max().max() # highest value measured for all 3 soils
        control_means_normalized = (control_means / treatment_means) * 100
        control_stde = control_stats.stde
        control_relative_stde = control_stde / control_means
        control_stde_normalized = (control_relative_stde**2 + treatment_relative_stde**2)**0.5

        control_means[name] = control_means_normalized * 100
        stde[name] = control_stde_normalized * 100

    # arrays to iterate over
    control_data = control_means.values()
    control_data_stde = stde.values()
    control_zipped = zip(data_names, control_data, control_data_stde)

    # subplots rows & columns
    n_rows = int(4)
    n_columns = int(2)

    # make figure and subplots
    figure, axes = pyplot.subplots(n_rows, n_columns,
                                   sharex=True, sharey=True, figsize=(15,20),
                                   gridspec_kw={'hspace': 0, 'wspace': 0},)
    figure.text(0.5, 0.05, r'$incubation\ time\ \/\ days$', ha='center')
    figure.text(0.05, 0.5, r'$%\ of treatment mean$', va='center', rotation=0.45)

    # plot
    i = 0
    for name, data, error in control_zipped:
        x = data.index.values
        for soil in SOILS:
            axes = axes.flatten()
            y = data[soil].values
            err = error[soil].values
            axes[i].errorbar(x, y, yerr=err)
            axes[i].set_label(name)

        i += 1

    # configure axes
    for ax in axes:
        configure_axes(ax)

    # legend
    handles = axes[0].get_lines()
    labels = SOILS
    figure.legend(handles, labels, 'center right')

    return figure


def make_bar_axes(figure: Figure, x_locations, soil_width, y_label,
                                                x_label=None, categories=None) -> Axes:

    # position = (
    #             111 if axes_position == 0 else
    #             211 if axes_position == 1 else
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
                                                   CATEGORIES_DATA, CATEGORIES):
        # baseline data
        baseline_statistics = get_baseline(data_set)
        BASELINE = baseline_statistics.means
        BASELINE_STDE = baseline_statistics.stde

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


def plot_C_N(data):

    carbon_figure = pyplot.figure(figsize=(15,10))

    axes = carbon_figure.add_subplot(111)

    axes.xaxis.set_minor_locator(MINOR_LOCATOR)
    axes.xaxis.set_major_locator(MAJOR_LOCATOR)
    axes.tick_params(axis='x', which='minor', width=1, length=3)

    lines = data.plot(ax=axes)

    return carbon_figure