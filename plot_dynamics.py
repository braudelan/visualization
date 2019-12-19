import math
import numpy
import matplotlib
from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.ticker import MultipleLocator

from raw_data import *
from stats import *
from cumulative_CO2 import *

from helpers import *


pyplot.style.use('seaborn-ticks')


SOILS = Constants.groups
UNITS = Constants.parameters_units
GENERIC_UNITS = Constants.generic_units

MAJOR_LOCATOR = MultipleLocator(7)  # major ticks locations
MINOR_LOCATOR = MultipleLocator(1)  # minor ticks locations
AXES_ASPECT = 0.6

TITLE_PAD = 15
X_LABEL = r'$day\ of\ incubation$'
X_LABEL_PAD = 15
Y_LABEL_PAD = X_LABEL_PAD

def set_line_parameters(axes, data):

    markers = Constants.markers
    linestyles = Constants.line_styles
    line_colors = Constants.colors

    handles, labels = axes.get_legend_handles_labels()
    lines = [handle[0] for handle in handles]
    lines_and_labels = dict(zip(lines, labels))

    for line, soil_label in lines_and_labels.items():
        line.set_marker(markers[soil_label])
        line.set_linestyle(linestyles[soil_label])
        line.set_color(line_colors[soil_label])


def get_aspect(axes, disp_ratio):
    data_ratio = axes.get_data_ratio()
    aspect_ratio = disp_ratio / data_ratio

    return aspect_ratio


def MRE_notation_marks(axes: Axes):

    MRE_TIME_POINTS = [0, 7, 14 ] # days when MRE was applied

    arrow_properties = dict(
                            arrowstyle="wedge,tail_width=0.7",
                            fc="0.8",
                            ec="0.1",
                           )

    for time_point in MRE_TIME_POINTS:

        arrow_angle = numpy.pi * 0.5  # radians from a downwards line perpendicular to x axis
        offset_head = 0.2  # offset of arrow head from annotation point, given in data coordinates(=days)
        offset_base = offset_head + math.sin(arrow_angle)  # offset of arrow base

        head_x = time_point + offset_head
        head_y = 0.01  # given as fraction of axes size
        base_y = head_y + 0.07  # given as fraction of axes size
        base_x = time_point + offset_base

        axes.annotate(
                    s='',
                    xy=(head_x, head_y ), # arrow head coordinates
                    xytext=(base_x, base_y), # arrow base coordinates
                    xycoords=('data','axes fraction'),
                    textcoords=('data', 'axes fraction'),
                    arrowprops=(arrow_properties)
                   )


def setup_figure():

    # create and adjut figure
    figure = pyplot.figure()
    figure.tight_layout()
    figure.subplots_adjust(hspace=0, wspace=0)

    return figure


def setup_dynamics_axes(figure: Figure, y_label, title, axes_position=111, share=None):
    '''
    setup an axes with time series features.

    share: tuple, or None
    whether to share one of the axis with other axes.
     tuple[0] can be either 'x' or 'y' or 'both' to designate which axis to share.
     tuple[1] is the instance of the other axes.

    '''

    # whether and which axis to share
    if share:
        which_axis = share[0]
        other_axes = share[1]
        share_x = other_axes if (which_axis == 'x' or which_axis == 'both') else None
        share_y = other_axes if (which_axis == 'y' or which_axis == 'both') else None
    else:
        share_x = None
        share_y = None

    # intialize axes
    axes: Axes = figure.add_subplot(axes_position, sharex=share_x, sharey=share_y )

    # ticks
    axes.xaxis.set_minor_locator(MINOR_LOCATOR)
    axes.tick_params(axis='x', which='minor', width=1, length=3)
    xticks = numpy.linspace(0,28,5)
    axes.set_xticks(xticks)

    # title
    axes.set_title(title, pad=TITLE_PAD)

    # labels
    axes.set_xlabel(
        X_LABEL,
        labelpad=X_LABEL_PAD,
    )

    axes.set_ylabel(
        y_label,
        labelpad=Y_LABEL_PAD
    )

    # add arrows where MRE was applied
    MRE_notation_marks(axes)

    return axes


def plot_dynamics(data_input, axes: Axes):
    '''
    plot short term dynamics onto axes.

    data_input:
    either a class instance with means and stnd error (both DataFrame)
    or a Dataframe.
    '''

    # data
    data = data_input.means
    std_error = data_input.stde

    # plot
    data.plot(
        ax=axes,
        yerr=std_error,
        legend=False
    )

    # x data limits
    axes.set_xlim(0,30)

    # set line parameters
    set_line_parameters(axes, data)

    # set the aspect ratio ( y axis length / x axis length)
    aspect_ratio = get_aspect(axes, AXES_ASPECT)
    axes.set_aspect(aspect_ratio)

    # legend
    handles, labels = axes.get_legend_handles_labels()
    new_handles = []
    for h in handles:
        new_handles.append(h[0])
    axes.legend(
        new_handles,
        labels,
        loc='best',
    )


def plot_two_subplots(figure, data_sets: dict, n_rows=1) -> dict:

    '''
    plot two data sets onto a figure.

    subplots will be either on top of each other or side by side,
    depending on n_rows.

    figure: Figure
    the Figure to be plotted onto.

    data_sets: dict
    data set name as key and a Stats instance as value.

    n_rows: int
    1 if subplots should be arranged side by side or 2 if
     on top of each other.

    return: dict
    value is data set name and key is the axes onto which
     the corresponding data set plotted.
    '''

    def final_adjustments(subplots):
        '''
        fix the subplots to look nicer.

         remove redundant objects and move others to better location.
         '''

        first_axes = subplots[0]
        second_axes = subplots[1]

        # remove unnecessary axis
        if IS_HORIZONTAL:
            second_axes.yaxis.set_visible(False) # seconed axes is to the right
        else:
            first_axes.xaxis.set_visible(False) # first axes is on top of the second

        # remove MRE notation from top axes (if subplots are stacked)
        if not IS_HORIZONTAL:
            axes_children = first_axes.get_children()
            is_annotation = lambda x: True if isinstance(x, matplotlib.text.Annotation) else False
            annotations = [child for child in axes_children if is_annotation(child)]
            pyplot.setp(annotations, visible=False)


    IS_HORIZONTAL = True if n_rows == 1 else False
    n_columns = 2 if IS_HORIZONTAL else 1

    subplots = {}
    for i, item in enumerate(data_sets.items()):

        is_first = True if i == 0 else False # test whether this is the first axes to be set up

        name = item[0] # name of data set
        data = item[1] # a Stats instance

        # labels
        ylabel = r'${}$'.format(GENERIC_UNITS)
        parameter_name = 'cumulative\ CO_2' if\
                                name == 'RESP' else name
        title = r'${}, MRE\ treated$'.format(parameter_name)

        # share both axis if the subplots are stacked on top of each other
        share = ('x', subplots[0]) if not is_first and not IS_HORIZONTAL else None

        # subplot position
        position = 1 if is_first else 2
        axes_position = int(
            str(n_rows) + str(n_columns) + str(position))

        # initialize axes
        axes = setup_dynamics_axes(
            figure, ylabel, title, axes_position, share=share)

        # plot
        plot_dynamics(data, axes)

        subplots[i] = axes

    final_adjustments(subplots)

    return subplots


if __name__ == '__main__':

    wknds = [0, 7, 14, 21, 28]
    raw_mbc = get_raw_data('MBC')['t'].loc[wknds]
    mbc_stats = get_stats(raw_mbc)
    cumulative_co2 = get_cumulative_respiration('t')
    data_sets = {
        'MBC': mbc_stats,
        'RESP': cumulative_co2
    }

    fig = setup_figure()
    subplots = plot_two_subplots(fig, data_sets, n_rows=2)



# todo
#   in plot_dynamics()
#       persistent colors for each soil. use a set_colors() function like set_markers() etc.
#   in plot_two_subplots()
#       remove or thin down the spine between the two subplots
#       single y_label for both plots
#       single legend for both plots
#   rewrite MRE_notation_marks() so that it returns the object that was drawn (i.e arrow).
#       in this way, the object can be reproduced and used in the legend or any other explanatory
#       note around the plot.
