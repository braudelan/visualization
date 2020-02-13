import math
import matplotlib
from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MultipleLocator

from data.raw_data import *
from data.cumulative_respiration import *

from data.helpers import *


SOILS = Constants.groups
UNITS = Constants.parameters_units
GENERIC_UNITS = Constants.generic_units

MARKERS = Constants.markers
LINE_STYLES = Constants.line_styles
LINE_COLORS = Constants.colors

DPI = 144
FIGURE_SIZE = (8, 4)

MINOR_LOCATOR = MultipleLocator(1)  # minor ticks locations
AXES_ASPECT = 0.5

# general axes parameters
TITLE_FONT_SIZE = 16
TITLE_PAD = 15
X_LABEL = r'$day\ of\ incubation$'
X_LABEL_PAD = 20
Y_LABEL_PAD = X_LABEL_PAD
AXIS_LABEL_FONTSIZE = 14
TICK_LABEL_FONTSIZE = 14

Y_BOTTOM_MARGIN = 0.04
Y_TOP_MARGIN = 0.06

# line parameters
LINE_WIDTH = 2.5
MARKER_SIZE = LINE_WIDTH * 3

# legend parameters
LEGEND_FONTSIZE = AXIS_LABEL_FONTSIZE


def insert_zoom_object(axes, factor, location, data, data_error, xy_lim):
    return

def set_line_parameters(axes, markers=MARKERS,
                        styles=LINE_STYLES, colors=LINE_COLORS):

    handles, labels = axes.get_legend_handles_labels()
    handles_and_labels = dict(zip(handles, labels))

    for handle, soil_label in handles_and_labels.items():
        handle[0].set_marker(markers[soil_label]) # 0 is index for Line2D
        # handle[0].set_linestyle(styles[soil_label])
        handle[0].set_color(colors[soil_label])
        # handle[2][0].set_color(colors[soil_label]) # [2][0] is index for error bars LineCollection


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
        offset_head = 0.2  # horizontal offset of arrow head from annotation point, given in data coordinates(=days)
        offset_base = offset_head + math.sin(arrow_angle)  # offset of arrow base, data coordinates

        head_x = time_point - offset_head
        head_y = -0.01  # given as fraction of axes size
        base_y = head_y - 0.07  # given as fraction of axes size
        base_x = time_point - offset_base

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
    figure = pyplot.figure(figsize=FIGURE_SIZE)
    figure.tight_layout()
    figure.subplots_adjust(hspace=0, wspace=0)

    return figure


def setup_figure_grid():

    figure = pyplot.figure(figsize=(15, 7.5),dpi=144)
    grid = GridSpec(3,1, figure=figure, hspace=0, wspace=0)

    return figure, grid


def setup_dynamics_axes(figure: Figure, y_label, title=None, axes_position=111, share=None):
    '''
    setup an axes with time series features.

    parameters
    ----------

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
    axes.tick_params(axis='both', labelsize=AXIS_LABEL_FONTSIZE)
    xticks = numpy.linspace(0,28,5)
    axes.set_xticks(xticks)

    # title
    if title:
        axes.set_title(title, pad=TITLE_PAD, fontsize=TITLE_FONT_SIZE)

    # labels
    axes.set_xlabel(
        X_LABEL,
        fontsize=AXIS_LABEL_FONTSIZE,
        labelpad=X_LABEL_PAD,
    )

    axes.set_ylabel(
        y_label,
        fontsize=AXIS_LABEL_FONTSIZE,
        labelpad=Y_LABEL_PAD
    )

    # add arrows where MRE was applied
    MRE_notation_marks(axes)

    return axes


def plot_dynamics(data_input, axes: Axes, with_legend: bool=False):
    '''
    plot short term dynamics onto axes.

    data_input: Stats
    a Stats instance with means and stnd error (both DataFrame).
    '''

    # data
    data = data_input.means
    std_error = data_input.stde

    # plot
    data.plot(
        ax=axes,
        yerr=std_error,
        linewidth=LINE_WIDTH,
        legend=False,
        markersize=MARKER_SIZE,
        ecolor='k',
        capsize=2,
        capthick=0.7,
        elinewidth=LINE_WIDTH * 0.5,
    )

    # set x limits
    axes.set_xlim(-1, 29)

    # set y limits
    y_bottom, y_top = axes.get_ylim()
    y_range = y_top - y_bottom
    bottom_margin = y_range * Y_BOTTOM_MARGIN
    top_margin = y_range * Y_TOP_MARGIN
    axes.set_ylim(y_bottom - bottom_margin, y_top + top_margin)

    # set line parameters
    set_line_parameters(axes)

    # set the aspect ratio ( y axis length / x axis length)
    aspect_ratio = get_aspect(axes, AXES_ASPECT)
    axes.set_aspect(aspect_ratio)

    # x label
    axes.set_xlabel(X_LABEL, labelpad=X_LABEL_PAD)

    # legend
    if with_legend:
        handles, labels = axes.get_legend_handles_labels()
        new_handles = []
        for h in handles:
            new_handles.append(h[0])
        axes.legend(
            new_handles,
            labels,
            fontsize=LEGEND_FONTSIZE,
            loc='upper right',
            # bbox_to_anchor=(0.98, 0.07)
        )


def plot_two_vertical_subplots(figure, data_sets: dict) -> dict:

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

         subplots: list
         two axes objects. top axes for i=0. bottom axes for i=1.
         '''

        top_axes = subplots[0]
        bottom_axes = subplots[1]

        # remove unnecessary axis
        top_axes.xaxis.set_visible(False) # first axes is the top one

        # remove MRE notation from top axes
        axes_children = top_axes.get_children()
        is_annotation = lambda x: True if isinstance(x, matplotlib.text.Annotation) else False
        annotations = [child for child in axes_children if is_annotation(child)]
        pyplot.setp(annotations, visible=False)

        # remove bottom spine of top axes
        spine = top_axes.spines['bottom']
        spine.set_visible(False)

        # remove unruly tick
        y_ticks = bottom_axes.yaxis.get_major_ticks()
        # y_ticks[-2].set_visible(False)

        # use a single y label
        bottom_ylabel = bottom_axes.yaxis.label
        top_ylabel = top_axes.yaxis.label
        bottom_ylabel.set_visible(False)
        pyplot.setp(top_ylabel, y=0, verticalalignment='center')

        # titles
        bottom_title = r'$Biomass\ Carbon$'
        top_title = r'$Cumulative\ CO_2$'
        title_x, title_y = 0.05, 0.88
        top_axes.text(title_x, title_y, top_title, transform=top_axes.transAxes)
        bottom_axes.text(title_x,  title_y, bottom_title, transform=bottom_axes.transAxes)

    subplots = {}
    for i, item in enumerate(data_sets.items()):

        is_bottom_axes = True if i == 1 else False  # test whether this is the second axes to be set up

        name = item[0] # name of data set
        data = item[1] # a Stats instance

        # y_label
        ylabel = r'${}$'.format(GENERIC_UNITS)


        # share x axis
        share = ('x', subplots[0]) if is_bottom_axes else None

        # subplot position
        position = 2 if is_bottom_axes else 1
        axes_position = int(str(21) + str(position))

        # initialize axes
        axes = setup_dynamics_axes(figure, ylabel,
                           axes_position=axes_position, share=share)

        # plot
        with_legend = False if is_bottom_axes else True # add legend only for the bottom axes
        plot_dynamics(data, axes, with_legend)

        # append the axes to subplots
        subplots[i] = axes


    final_adjustments(subplots)

    return subplots


def plot_two_horizontal_subplots(figure, data_sets: dict) -> dict:

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

         subplots: list
         two axes objects. top axes for i=0. bottom axes for i=1.
         '''

        right_axes = subplots[0]
        left_axes = subplots[1]

        # remove unnecessary axis
        right_axes.xaxis.set_visible(False) # first axes is the top one

        # remove MRE notation from top axes
        axes_children = right_axes.get_children()
        is_annotation = lambda x: True if isinstance(x, matplotlib.text.Annotation) else False
        annotations = [child for child in axes_children if is_annotation(child)]
        pyplot.setp(annotations, visible=False)

        # remove bottom spine of top axes
        spine = right_axes.spines['bottom']
        spine.set_visible(False)

        # remove unruly tick
        y_ticks = left_axes.yaxis.get_major_ticks()
        # y_ticks[-2].set_visible(False)

        # use a single y label
        bottom_ylabel = left_axes.yaxis.label
        top_ylabel = right_axes.yaxis.label
        bottom_ylabel.set_visible(False)
        pyplot.setp(top_ylabel, y=0, verticalalignment='center')

        # titles
        bottom_title = r'$Biomass\ Carbon$'
        top_title = r'$Cumulative\ CO_2$'
        title_x, title_y = 0.05, 0.88
        right_axes.text(title_x, title_y, top_title, transform=right_axes.transAxes)
        left_axes.text(title_x,  title_y, bottom_title, transform=left_axes.transAxes)

    subplots = {}
    for i, item in enumerate(data_sets.items()):

        is_left_axes = True if i == 1 else False  # test whether this is the second axes to be set up

        name = item[0] # name of data set
        data = item[1] # a Stats instance

        # y_label
        ylabel = r'${}$'.format(GENERIC_UNITS)


        # share x axis
        share = ('x', subplots[0]) if is_left_axes else None

        # subplot position
        position = 2 if is_left_axes else 1
        axes_position = int(str(12) + str(position))

        # initialize axes
        axes = setup_dynamics_axes(figure, ylabel,
                           axes_position=axes_position, share=share)

        # plot
        with_legend = True if is_left_axes else False # add legend only for the bottom axes
        plot_dynamics(data, axes, with_legend)

        # append the axes to subplots
        subplots[i] = axes


    final_adjustments(subplots)

    return subplots


if __name__ == '__main__':

    # microbial activity
    wknds = [0, 7, 14, 21, 28]
    raw_mbc = get_raw_data('MBC')['t'].loc[wknds]

    generic_ylabel = r'$mg\ast kg\ soil^{-1}$'


    # hws to mbc
    raw_hws_mbc = get_HWS_to_MBC()['t'].loc[[7, 14, 21, 28]]
    hws_mbc_stats = get_stats(raw_hws_mbc)

    ylabel = r'$\%\ of\ MBC$'
    title = r'$HWE_{carbohydrates}$'

    # HWE carbs
    raw_hwec = get_raw_data('HWS')
    hwec_stats = get_stats(raw_hwec, 't')

    hws_title = r'$HWE_{carbohydrates}$'
    # MBC
    mbc_stats = get_stats(raw_mbc)
    mbc_title = r'$Microbial\ Biomass\ Carbon$'

    # cumulative respiration
    cumulative_stats = get_cumulative_respiration('t')
    respiration_title = r'$cumulative\ CO_2$'

    # visualize single plot
    fig = setup_figure()
    ax = setup_dynamics_axes(fig, ylabel, title)
    plot_dynamics(hws_mbc_stats, ax, with_legend=True)

    # visualize two subplots
    # fig = setup_figure()
    #
    # subplots = plot_two_vertical_subplots(fig, data_sets) # microbial activity

    # save figure
    dir = '/home/elan/Dropbox/research/student_conference/figures/'
    file = f'HWS_to_MBC_dynamics.png'
    file_path = f'{dir}{file}'
    fig.savefig(file_path, format='png', bbox_inches='tight', dpi=DPI)

# todo
#   for dynamics plot:
#       remove first and last minor xticks
#       sort zorder as follows lines < errors < markers (lines will be drawn first and so on)
#       maybe put a box around legend to make clearer
#       maybe define insert_zoom_object()
#   rewrite MRE_notation_marks() so that it returns the object that was drawn (i.e arrow).
#       in this way, the object can be reproduced and used in the legend or any other explanatory
#       note around the plot.
