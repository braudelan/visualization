import math

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.ticker import MultipleLocator

from data.raw_data import *
from data.cumulative_respiration import *

import constants

SOILS = constants.LONG_TERM_TREATMENTS
UNITS = constants.parameters_units
GENERIC_UNITS = constants.generic_units

MARKERS = constants.markers
LINE_STYLES = constants.line_styles
LINE_COLORS = constants.colors

DPI = 144
FIGURE_SIZE = (8, 4)

MINOR_LOCATOR = MultipleLocator(1)  # minor ticks locations
AXES_ASPECT = 0.5

# general axes parameters
TITLE_FONT_SIZE = 16
TITLE_PAD = 15
X_LABEL = r'$days$'
X_LABEL_PAD = 20
Y_LABEL_PAD = X_LABEL_PAD
AXIS_LABEL_FONTSIZE = 14
TICK_LABEL_FONTSIZE = 14

Y_BOTTOM_MARGIN = 0
Y_TOP_MARGIN = 0.06

# line parameters
LINE_WIDTH = 2.5
MARKER_SIZE = LINE_WIDTH * 3

# legend parameters
LEGEND_FONTSIZE = AXIS_LABEL_FONTSIZE


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


def make_line_plot(stats, data_set_name, output_dir):
    '''
    plot short term dynamics onto axes.

    :param stats: Stats
    :param axes: Axes
    :param with_legend: bool
    whether to plot a legend or not

    '''
    # todo include all function inside function (setup figure, axes and save figure)
    #   update doc string
    #   drop with_legend argument, always plot legend

    plt.style.use('incubation-dynamics')

    # data
    means = stats.means
    std_error = stats.stde

    # intialize figure
    figure = plt.figure(figsize=FIGURE_SIZE)
    figure.tight_layout()

    # intialize axes
    axes: Axes = figure.add_subplot(111)

    # ticks
    axes.xaxis.set_minor_locator(MINOR_LOCATOR)
    axes.tick_params(axis='x', which='minor', width=1, length=3)
    # axes.tick_params(axis='both', labelsize=AXIS_LABEL_FONTSIZE)
    xticks = numpy.linspace(0, 28, 5)
    axes.set_xticks(xticks)

    # add arrows where MRE was applied
    MRE_notation_marks(axes)

    # plot
    means.plot(
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

    # set y limits
    # todo wrap as function
    y_bottom, y_top = axes.get_ylim()
    y_range = y_top - y_bottom
    bottom_margin = y_range * Y_BOTTOM_MARGIN
    top_margin = y_range * Y_TOP_MARGIN
    axes.set_ylim(y_bottom - bottom_margin, y_top + top_margin)

    # set x limits
    index = means.index
    last_sampling = index[-1]
    axes.set_xlim(-1, last_sampling + 1)

    # labels
    axes.set_xlabel(
        X_LABEL,
        # fontsize=AXIS_LABEL_FONTSIZE,
        labelpad=X_LABEL_PAD,
    )

    y_label = f'${constants.parameters_units[data_set_name]}$'
    axes.set_ylabel(
        y_label,
        # fontsize=AXIS_LABEL_FONTSIZE,
        labelpad=Y_LABEL_PAD
    )
    # set line parameters
    set_line_parameters(axes)

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
        # fontsize=LEGEND_FONTSIZE,
        loc='upper right')
        # bbox_to_anchor=(0.98, 0.07)

    # save
    top_directory = constants.figures_directory
    file_path = f'{top_directory}/{output_dir}/{data_set_name}.pdf'
    figure.savefig(file_path, format='pdf', bbox_inches='tight', dpi=DPI)


def make_bar_plot(stats, data_set_name, output_dir):
    # todo remove vlines from grid
    #   adjust ylim
    plt.style.use('incubation-dynamics')

    COLORS = constants.colors
    color = [COLORS.get(x, '#333333') for x in SOILS]

    # get the data
    means = stats.means
    stnd_err = stats.stde

    #intialize figure and axes
    figure: Figure = plt.figure(figsize=FIGURE_SIZE)
    ax: Axes = figure.add_subplot(111)

    # plot
    error_kw_dict = {
        'capsize': 2.5,
        'lw': 1,
        'capthick': 0.7,
    }
    means.plot.bar(ax=ax,
                   yerr=stnd_err,
                   color=color,
                   error_kw=error_kw_dict,
                   rot=0,
                   legend=False)

    # remove xtick lines
    for l in ax.xaxis.get_majorticklines():
        l.set_visible(False)

    # axis labels
    ax.set_xlabel(
        X_LABEL,
        labelpad=X_LABEL_PAD
    )
    ylabel = f'${constants.parameters_units[data_set_name]}$'
    ax.set_ylabel(
        ylabel,
        labelpad=Y_LABEL_PAD
    )

    # set y limits
    # todo wrap as function
    y_bottom, y_top = ax.get_ylim()
    y_range = y_top - y_bottom
    bottom_margin = y_range * Y_BOTTOM_MARGIN
    top_margin = y_range * Y_TOP_MARGIN
    ax.set_ylim(y_bottom - bottom_margin, y_top + top_margin)

    # legend
    h, l = ax.get_legend_handles_labels()
    ax.legend(h, l)

    # set the aspect ratio ( y axis length / x axis length)
    aspect_ratio = get_aspect(ax, AXES_ASPECT)
    ax.set_aspect(aspect_ratio)

    # save
    top_directory = constants.figures_directory
    file_path = f'{top_directory}/{output_dir}/{data_set_name}.pdf'
    figure.savefig(file_path, format='pdf', bbox_inches='tight', dpi=DPI)

    return figure


def make_table(
    stats,
    data_set_name,
    output_dir,
    treatment,
):

    #
    def insert_error(means, err):

        means_error = means.copy()
        for row in means.index:
            for column in means.columns:
                mean = means.loc[row, column]
                err = error.loc[row, column]

                means_error.loc[row, column] = \
                '{:.2f} +-'.format(mean) + ' {:.2f}'.format(err)
                
        return means_error

    # get the data
    means = stats.means
    error = stats.stde

    # append a ±error to each mean value
    means_error = insert_error(means, error)

    # output path
    top_dir = constants.figures_directory
    output_file = f'{top_dir}/'\
                  f'{output_dir}/'\
                  f'{data_set_name}.tex'

    # table caption and lable
    treatment_title = 'MRE treated' if treatment == 't' else 'Control'
    parameter_title = constants.PARAMETERS_TITLES[data_set_name]
    caption = f'{parameter_title} in {treatment_title} samples'
    label_treatment_title = 'treated_main'
    label = f'{data_set_name.lower}_{label_treatment_title}'
    means_error.to_latex(buf=output_file,
                         bold_rows=True,
                         caption=caption,
                         label=label)




#
# def axes_final_adujst(axes, with_legend: bool=None):
#
#     # set y limits
#     y_bottom, y_top = axes.get_ylim()
#     y_range = y_top - y_bottom
#     bottom_margin = y_range * Y_BOTTOM_MARGIN
#     top_margin = y_range * Y_TOP_MARGIN
#     axes.set_ylim(y_bottom - bottom_margin, y_top + top_margin)
#
#     # set line parameters
#     set_line_parameters(axes)
#
# #     # set the aspect ratio ( y axis length / x axis length)
# #     aspect_ratio = get_aspect(axes, AXES_ASPECT)
# #     axes.set_aspect(aspect_ratio)
#
#     # x label
#     axes.set_xlabel(X_LABEL, labelpad=X_LABEL_PAD)
#
#     # legend
#     if with_legend:
#         handles, labels = axes.get_legend_handles_labels()
#         new_handles = []
#         for h in handles:
#             new_handles.append(h[0])
#         axes.legend(
#             new_handles,
#             labels,
#             fontsize=LEGEND_FONTSIZE,
#             loc='upper right',
#             # bbox_to_anchor=(0.98, 0.07)
#         )
#
# def setup_figure():
#
#     # create and adjut figure
#     figure = plt.figure(figsize=FIGURE_SIZE)
#     figure.tight_layout()
#
#     return figure
#
#
# def setup_axes(
#         figure: Figure,
#         y_label,
#         title=None,
#     ):
#     '''setup an axes with time series features.'''
#
#     # intialize axes
#     axes: Axes = figure.add_subplot(111)
#
#     # ticks
#     axes.xaxis.set_minor_locator(MINOR_LOCATOR)
#     axes.tick_params(axis='x', which='minor', width=1, length=3)
#     # axes.tick_params(axis='both', labelsize=AXIS_LABEL_FONTSIZE)
#     xticks = numpy.linspace(0,28,5)
#     axes.set_xticks(xticks)
#
#     # title
#     if title:
#         axes.set_title(title, pad=TITLE_PAD, fontsize=TITLE_FONT_SIZE)
#
#     # labels
#     axes.set_xlabel(
#         X_LABEL,
#         # fontsize=AXIS_LABEL_FONTSIZE,
#         labelpad=X_LABEL_PAD,
#     )
#
#     axes.set_ylabel(
#         y_label,
#         # fontsize=AXIS_LABEL_FONTSIZE,
#         labelpad=Y_LABEL_PAD
#     )
#
#     # add arrows where MRE was applied
#     MRE_notation_marks(axes)
#
#     return axes
