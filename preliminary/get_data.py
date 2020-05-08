import pdb
import numpy
import pandas
from pandas import DataFrame
from pandas import MultiIndex

import matplotlib.pyplot as plt
import matplotlib.transforms as transforms

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.ticker import MultipleLocator

import constants
import data.helpers as helpers
from data.helpers import Stats
# from data.helpers import *


LTTs = ['ORG', 'MIN']
STTs = ['CON', 'STR', 'KWC']
#--------------------------------------- get the data ------------------------------------------

def get_raw_data(data_name):

    # data set into DataFrame
    raw_data = pandas.read_excel(constants.preliminary_input_file,
                                 index_col=[0, 1, 2],header=1,
                                 sheet_name=data_name,
                                 na_values=["-", " "])

    columns_levels_names =  ['LTT', 'STT', 'replicate']
    levels_new_order = ['STT', 'LTT', 'replicate']

    # name the indices
    raw_data.rename_axis(columns_levels_names, inplace=True)
    raw_data.rename_axis('hours', axis='columns', inplace=True)
    # raw_data = raw_data.reorder_levels(levels_new_order)

    # transpose
    raw_data = raw_data.T

    return raw_data


def get_stats(raw_data, STT=None):
    '''
    get statistics for each LTT.

    :param STT: tuple of strings
    which STT to compute statistics for.

    :return: stats
    Stats instance with means and stnd error.

    '''

    # slice Short Term Treatment if STT is passed
    raw_data = raw_data.loc[:, (slice(None), STT)].droplevel('STT', axis='columns') \
            if STT else raw_data

    # get_statistics
    levels = ('LTT') if STT else ('LTT', 'STT')
    group_by_treatment = raw_data.groupby(level=levels, axis=1)

    means = group_by_treatment.mean()
    stde = group_by_treatment.sem()

    return Stats(
        means=means,
        stde=stde,
    )


def get_stt_stats(
        raw_data,
):
    '''
    return a dictionary with Stats instances for each STT.

    :param raw: DataFrame
    :return: stt_stats: dict
    '''

    stt_stats = {}
    for stt in STTs:

        raw = raw_data.loc[:, (slice(None), stt)].droplevel('STT', axis='columns')

        # get_statistics
        group_by_treatment = raw.groupby(level='LTT', axis=1)

        means = group_by_treatment.mean()
        stde = group_by_treatment.sem()

        stats = Stats(means=means, stde=stde)

        stt_stats[stt] = stats

    return stt_stats


def get_multiple_stats(
        data_sets_names,
        normalize: bool=None,
        is_percent=None,
    ):

    data_stats = {}
    for data_name in data_sets_names:

        raw = get_raw_data(data_name)

        STT_stats = {}
        for STT in STTs:
            not_control = STT != 'CON'
            if normalize and not_control:
                raw_STT = control_normalize(raw, STT, is_percent)
            else:
                raw_STT = raw
            stats = get_stats(raw_STT, STT)
            STT_stats[STT] = stats

        data_stats[data_name] = STT_stats

    return data_stats


def control_normalize(raw_data, STT, is_percent=None):
    '''
    subtract the mean value of control replicates from STT.

    :param raw_data: DataFrame
    the data to be normalized.

    :returns normalized: DataFrame
    of similar shape as raw_data with mean control values subtracted.
    '''

    def negative_to_nan(element):
        '''helper function to pass for applymap.'''

        return None if element < 0 else element
    # raw data
    raw_STT = raw_data.loc[:, (slice(None), STT)]
    control_raw = raw_data.loc[:, (slice(None), 'CON')]

    # control means
    control_means = get_stats(control_raw).means  # shape ->(10,3)

    # empty dataframe with the same shape and indexes as raw_STT
    control_reindexed = DataFrame().reindex_like(raw_STT)  # shape ->(10,12)
    # control_reindexed = control_reindexed.droplevel('replicate', axis=1)

    # fill empty dataframe with the mean value for every set of replicates
    for row in raw_STT.index:
        for column in raw_STT.columns:
            # pdb.set_trace()
            LTT = column[0]
            control_reindexed.loc[row, column] = control_means.loc[row, LTT].values

    # normalize
    diff = raw_STT - control_reindexed
    percent = (raw_STT - control_reindexed) / control_reindexed * 100
    normalized = percent if is_percent else diff


    # # remove negative values
    # negative_to_nan = lambda element: None if element < 0 else element
    # normalized = normalized.applymap(negative_to_nan)

    return  normalized


#------------------------------------------- cumulative respiration -----------------------------------
# todo 'KWC' missing data on 7h and 24h so that INTERVALS need to be reavluated to exclude these sampling events

# get respiration raw data
RAW_DATA = get_raw_data('Resp')

# limits of time intervals between samplings
timepoints = RAW_DATA.index.values
n_intervals = len(timepoints) - 1
INTERVALS = [[timepoints[i], timepoints[i + 1]] for i in range(
    n_intervals)]  # a list of intervals start and end (i.e [0, 2] for the interval between incubation start and 2 h)
intervals_arrayed = numpy.asarray(INTERVALS)
interval_limits = intervals_arrayed.T  # array.shape-->(2, len(SAMPLING_TIMEPOINTS))
BEGININGS = interval_limits[0]
ENDINGS = interval_limits[1]
INTERVALS_TIME = ENDINGS - BEGININGS # intervals time in hours


def get_mean_rates(STT):
    '''
    get average rate between every two consecutive sampling points.

    :param raw_data: DataFrame

    :param STT: tuple of strings
    'control', 'starw', 'compost' or any combination of these.

    :return: class Stats
    mean respiration rates averaged between each two consecutive
    sampling points.
    '''

    # empty DataFrame for mean rates
    levels = [
        # weeks,
        BEGININGS,
        ENDINGS,
    ]
    names = [
        # 'week',
        't_initial',
        't_end'
    ]
    multi_index = MultiIndex.from_arrays(
        arrays=levels, names=names)
    respiration_rates = DataFrame(
        index=multi_index, columns=LTTs)
    rates_stnd_errors = DataFrame(
        index=multi_index, columns=LTTs)

    # data
    RESP_stats = get_stats(RAW_DATA, STT)
    RESP_means = RESP_stats.means
    RESP_stde = RESP_stats.stde

    for soil in LTTs:
        soil_respiration = RESP_means[soil]
        soil_stde = RESP_stde[soil]

        mean_rates = []
        stnd_errors = []
        for interval in INTERVALS:
            t_initial = interval[0]
            t_end = interval[1]

            t_initial_means = soil_respiration.loc[t_initial]
            t_initial_stde = soil_stde.loc[t_initial]
            t_end_means = soil_respiration.loc[t_end]
            t_end_stde = soil_stde.loc[t_end]

            mean = (t_initial_means + t_end_means) / 2
            stde = (t_initial_stde ** 2 + t_end_stde ** 2) ** 0.5 / 2

            mean_rates.append(mean)
            stnd_errors.append(stde)

        respiration_rates[soil] = mean_rates
        rates_stnd_errors[soil] = stnd_errors

    return Stats(
        means=respiration_rates,
        stde=rates_stnd_errors
    )


def get_daily_respiration(STT):

    rates = get_mean_rates(STT)
    mean_rates = rates.means
    rates_stde = rates.stde

    # daily CO2
    daily_respiration = mean_rates.mul(INTERVALS_TIME / 24,
                                       axis='rows')  # rate X time (in days)
    daily_error = rates_stde.mul(INTERVALS_TIME / 24,
                                 axis='rows')  # multiply stnd error by the same constant(i.e. time)

    return Stats(
        means=daily_respiration,
        stde=daily_error
    )


def get_cumulative_respiration(treatment):

    daily_cumulative = get_daily_respiration(treatment)
    daily_mean = daily_cumulative.means
    daily_error = daily_cumulative.stde

    # compute cumulative CO2 for every sampling day
    cumulative_respiration = daily_mean.apply(
        helpers.get_cumulative_sum,
        axis='index',
        raw=True,
    )
    cumulative_error = daily_error.apply(
        helpers.get_cumulative_error,
        axis='index',
        raw=True,
    )
    cumulative_respiration = cumulative_respiration.droplevel(0).rename_axis('hours')
    cumulative_error = cumulative_error.droplevel(0).rename_axis('hours')

    return  Stats(
        means=cumulative_respiration,
        stde=cumulative_error,
    )


# ---------------------------------------------- visualize----------------------------------

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
X_LABEL = r'$hours$'
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


def get_aspect(axes, disp_ratio):
    data_ratio = axes.get_data_ratio()
    aspect_ratio = disp_ratio / data_ratio

    return aspect_ratio


def set_line_parameters(axes, markers=MARKERS, colors=LINE_COLORS):

    handles, labels = axes.get_legend_handles_labels()
    handles_and_labels = dict(zip(handles, labels))

    for handle, soil_label in handles_and_labels.items():
        handle[0].set_marker(markers[soil_label]) # 0 is index for Line2D
        handle[0].set_color(colors[soil_label])


def setup_figure():

    # create and adjut figure
    figure = plt.figure(figsize=FIGURE_SIZE)
    figure.tight_layout()
    figure.subplots_adjust(hspace=0, wspace=0)

    return figure


def setup_dynamics_axes(
        figure: Figure,
        y_label: str,
        data: Stats,
    ):
    '''
    setup an axes with time series features.

    :param figure:
    :param y_label:
    :param data:
    :param title:
    :param axes_position:
    :param share:
    :return:
    '''


    # intialize axes
    axes: Axes = figure.add_subplot(111)

    # ticks
    timepoints = data.means.index
    n_hours = timepoints[-1]
    major_time_unit = 24
    n_major_periods = n_hours / major_time_unit
    # axes.tick_params(
    #     axis='both', labelsize=AXIS_LABEL_FONTSIZE)
    xticks = numpy.linspace(
        0,n_hours,n_major_periods + 1)
    axes.set_xticks(xticks)

    # # labels
    # axes.set_xlabel(
    #     X_LABEL,
    #     fontsize=AXIS_LABEL_FONTSIZE,
    #     labelpad=X_LABEL_PAD,
    # )

    axes.set_ylabel(
        y_label,
        # fontsize=AXIS_LABEL_FONTSIZE,
        labelpad=Y_LABEL_PAD
    )

    return axes



def single_line_plot(
        stats,
        axes: Axes,
        legend=False,
):
    '''
    plot short term dynamics onto axes.

    :param stats: Stats
    :param axes: Axes
    :param legend: bool
    whether to plot a legend or not

    '''

    data = stats.means
    std_error = stats.stde

    # plot
    plot = data.plot(
        ax=axes,
        yerr=std_error,
        # linewidth=LINE_WIDTH,
        legend=False,
        # markersize=MARKER_SIZE,
        ecolor='k',
        capsize=2,
        capthick=0.7,
        elinewidth=LINE_WIDTH * 0.5,
    )

    # set x limits
    timepoints = stats.means.index
    n_hours = timepoints[-1]
    axes.set_xlim(-1, n_hours +1)

    # set y limits
    y_bottom, y_top = axes.get_ylim()
    y_range = y_top - y_bottom
    bottom_margin = y_range * Y_BOTTOM_MARGIN
    top_margin = y_range * Y_TOP_MARGIN
    axes.set_ylim(y_bottom - bottom_margin, y_top + top_margin)

    # set the aspect ratio ( y axis length / x axis length)
    aspect_ratio = get_aspect(axes, AXES_ASPECT)
    axes.set_aspect(aspect_ratio)

    # # x label
    # axes.set_xlabel(X_LABEL, labelpad=X_LABEL_PAD)

    set_line_parameters(axes)

    # legend
    handles, labels = axes.get_legend_handles_labels()
    axes.legend(handles,
                labels,
                loc='upper right',)
                # fontsize=LEGEND_FONTSIZE,
                # bbox_to_anchor=(0.98, 0.07))

    return axes


def visualize_single_plot(
        data,
        output_file_name,
        y_label,
        output_dir,
        set_lines=None
    ):

    with plt.style.context(u'incubation-dynamics'):

        # setup figure, axes
        figure: Figure = setup_figure()
        axes = setup_dynamics_axes(figure, y_label, data)

        # plot
        single_line_plot(data, axes)

        # save
        top_dir = constants.figures_directory
        file_path = f'{top_dir}/{output_dir}/{output_file_name}'
        figure.savefig(file_path, format='pdf', bbox_inches='tight', dpi=DPI)

    return figure


def jointly_plot_stts(stats: Stats, data_set_name):
    '''
    plot all STTs on one axes.

    :param stats: Stats
     data from all STTs
    :return:
    '''

    # STTs
    treatments = ['STR', 'KWC']

    # data
    means: DataFrame = stats.means
    stnd_err: DataFrame = stats.stde

    # reorder columns levels and remove 'CON' STT
    means = means.reorder_levels(['STT', 'LTT'], axis=1)
    means = means.loc[:, treatments]
    stnd_err = stnd_err.reorder_levels(['STT', 'LTT'], axis=1)
    stnd_err = stnd_err.loc[:, treatments]

    # figure and axs
    plt.style.use('incubation-dynamics')
    figure, axs = plt.subplots(nrows=2,
                               ncols=1,
                               tight_layout=True)
    upper_ax = axs[0]
    lower_ax = axs[1]

    # plot
    for stt, ax in zip(treatments, axs):

        err = stnd_err[stt]
        means[stt].plot(
            ax=ax,
            yerr=err,
            legend=False,
            ecolor='k',
            capsize=2,
            capthick=0.7,
        )

    for ax in axs:
        # set the axis limits
        # y limits
        relative_margin = 0.2
        limits = ax.get_ylim()
        upper_lim = limits[1]
        new_upper_lim = upper_lim + upper_lim * relative_margin
        ax.set_ylim(0, new_upper_lim)

        # set x limits
        timepoints = stats.means.index
        n_hours = timepoints[-1]
        ax.set_xlim(-1, n_hours + 1)

        # set line parameters
        set_line_parameters(ax)

        # set the aspect ratio ( y axis length / x axis length)
        aspect_ratio = get_aspect(ax, AXES_ASPECT)
        ax.set_aspect(aspect_ratio)

    # remove x label and  xtick lables for upper ax
    upper_ax.set_xlabel('')
    x_tick_labels = upper_ax.xaxis.get_majorticklabels()
    for label in x_tick_labels:
        label.set_visible(False)

    # ylabel as a figure text
    trans = transforms.blended_transform_factory(
        lower_ax.transAxes, figure.transFigure)
    ylabel = f'${constants.parameters_units[data_set_name]}$'
    figure.text(-0.3, 0.55, ylabel, rotation=90,
                va='center', transform=trans)

    # identifiers for axs
    text_x = 0.85
    text_y = 0.75
    upper_ax_letter = 'A'
    lower_ax_letter = 'B'
    text_params = {
        'size': 15,
        'fontweight': 'bold'
    }
    upper_ax.text(
        text_x,
        text_y,
        upper_ax_letter,
        transform=upper_ax.transAxes,
        fontdict=text_params
    )
    lower_ax.text(
        text_x,
        text_y,
        lower_ax_letter,
        transform=lower_ax.transAxes,
        fontdict=text_params,
    )

    # legend
    anchor = (0.7, 0.9)
    h, l = upper_ax.get_legend_handles_labels()

    # figure.figlegend(h, l, loc='center left', bbox_to_anchor=anchor)
    figure.legend(h, l, bbox_to_anchor=(0., 1.02, 0.6, .102), loc='center',
           ncol=2, mode="expand", borderaxespad=0., bbox_transform=upper_ax.transAxes)

    return figure


def visualize_jointed_stts(
        data_sets_names,
        output_dir,
        
    ):

    for data_set in data_sets_names:

        raw = get_raw_data(data_set)
        stats = get_stats(raw)

        figure = jointly_plot_stts(stats, data_set)

#         figure.suptitle(f'{data_set}')
        output_file_name = f'{data_set}.pdf'
        top_dir = constants.figures_directory
        file_path = f'{top_dir}/{output_dir}/{output_file_name}'
        figure.savefig(file_path, format='pdf', bbox_inches='tight', dpi=DPI)

def visualize_multiple_plots(
        data_sets_names,
        output_dir,
        normalize=None,
        is_percent=None,
        with_title=None,
    ):

    multiple_stats = get_multiple_stats(data_sets_names,
                                        normalize=normalize, is_percent=is_percent)
    # pdb.set_trace()
    for data_name, value in multiple_stats.items():

        units = constants.parameters_units
        ylabel = f'${units[data_name]}$'


        for STT, stats in value.items():
            file_name = f'{data_name}_{STT}.pdf'
            visualize_single_plot(data=stats, output_file_name=file_name,
                                  y_label=ylabel, output_dir=output_dir)
            plt.close()

def visualize_control_plots(
        data_sets_names,
        output_dir,
    ):

    multiple_stats = get_multiple_stats(data_sets_names)
    # pdb.set_trace()
    for data_name, value in multiple_stats.items():

        units = constants.parameters_units
        ylabel = f'${units[data_name]}$'

        stats = value['CON']

        file_name = f'{data_name}.pdf'
        visualize_single_plot(data=stats, output_file_name=file_name,
                              y_label=ylabel, output_dir=output_dir)
        plt.close()


