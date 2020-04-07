import pdb

import pandas
from pandas import DataFrame
from pandas import MultiIndex
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.ticker import MultipleLocator

from visualization.visualize import visualize_single_plot
from preliminary.constants import *
from data.helpers import *


LTTs = ['ORG', 'MIN']
STTs = ['CON', 'STR', 'KWC']
#--------------------------------------- get the data ------------------------------------------

def get_raw_data(data_name):

    # data set into DataFrame
    raw_data = pandas.read_excel(INPUT_FILE_PATH,
                                 index_col=[0, 1, 2],header=1,
                                 sheet_name=data_name,
                                 na_values=["-", " "])

    index_names =  ['LTT', 'STT', 'replicate']

    # name the index
    raw_data.rename_axis(index_names, inplace=True)
    raw_data.rename_axis('hours of incubation', axis='columns', inplace=True)

    # transpose
    raw_data = raw_data.T

    return raw_data


def get_stats(raw_data, STT: tuple=None):
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


def get_multiple_stats(data_sets_names, normalize: bool=None):

    data_stats = {}
    for data_name in data_sets_names:

        raw = get_raw_data(data_name)

        STT_stats = {}
        for STT in STTs:
            # pdb.set_trace()
            raw_STT = control_normalize(raw, STT) if normalize and STT != 'CON' else raw
            stats = get_stats(raw_STT, STT)
            STT_stats[STT] = stats

        data_stats[data_name] = STT_stats

    return data_stats


def control_normalize(raw_data, STT):
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

    # fill empty dataframe with the mean value for every set of replicates
    for row in raw_STT.index:
        for column in raw_STT.columns:
            LTT = column[0]
            control_reindexed.loc[row, column] =\
                                control_means.loc[row, LTT]

    # normalize
    normalized = raw_STT - control_reindexed

    # remove negative values
    negative_to_nan = lambda element: None if element < 0 else element
    normalized = normalized.applymap(negative_to_nan)

    return  normalized


#------------------------------------------- cumulative respiration -----------------------------------

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

    # frame for mean rates
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
        get_cumulative_sum,
        axis='index',
        raw=True,
    )
    cumulative_error = daily_error.apply(
        get_cumulative_error,
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
    figure = pyplot.figure(figsize=FIGURE_SIZE)
    figure.tight_layout()
    figure.subplots_adjust(hspace=0, wspace=0)

    return figure


def setup_dynamics_axes(
        figure: Figure,
        y_label: str,
        data: Stats,
        title: str=None,
        axes_position=111,
        share: tuple=None,
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
    timepoints = data.means.index
    n_hours = timepoints[-1]
    major_time_unit = 24
    n_major_periods = n_hours / major_time_unit
    # axes.xaxis.set_minor_locator(MINOR_LOCATOR)
    # axes.tick_params(
    #     axis='x', which='minor', width=1, length=3)
    axes.tick_params(
        axis='both', labelsize=AXIS_LABEL_FONTSIZE)
    xticks = numpy.linspace(
        0,n_hours,n_major_periods + 1)
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


    return axes



def plot_dynamics(data_input, axes: Axes, with_legend: bool=False):
    '''
    plot short term dynamics onto axes.

    :param data_input: Stats
    :param axes: Axes
    :param with_legend: bool
    whether to plot a legend or not

    '''

    # data
    data = data_input.means
    std_error = data_input.stde

    # plot
    plot = data.plot(
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
    timepoints = data_input.means.index
    n_hours = timepoints[-1]
    axes.set_xlim(-1, n_hours +1)

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
        # new_handles = []
        # for h in handles:
        #     new_handles.append(h[0])
        axes.legend(
            handles,
            # new_handles,
            labels,
            fontsize=LEGEND_FONTSIZE,
            loc='upper right',
            # bbox_to_anchor=(0.98, 0.07)
        )


def visualize_single_plot(
        data,
        data_name,
        y_label,
        output_dir,
    ):

    with pyplot.style.context(u'incubation-dynamics'):
        # setup figure, axes
        figure: Figure = setup_figure()
        axes = setup_dynamics_axes(figure, y_label, data)

        # plot
        plot_dynamics(data, axes, with_legend=True)

        # save
        file_path = f'{TOP_OUTPUT_DIRECTORY}/{output_dir}/{data_name}'
        figure.savefig(file_path, format='png', bbox_inches='tight', dpi=DPI)

    return figure


def visualize_all_data(data_sets_names, output_dir, normalize: bool=None):

    multiple_stats = get_multiple_stats(data_sets_names, normalize=normalize)

    for data_name, value in multiple_stats.items():
        for STT, stats in value.items():

            visualize_single_plot(stats, f'{data_name}_{STT}', 'ylabel', output_dir)


