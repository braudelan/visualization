import numpy
from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from data.raw_data import *
from data.stats import *

# ------------------------------------- data --------------------------------------------------------------
# which data sets to use
DATA_SETS_NAMES = ['WEOC', 'HWES', 'MBC']

# get the data
raw_data_sets = get_multi_sets(DATA_SETS_NAMES, treatment='t', wknds=True)
mean_data_sets = get_multiple_stats(raw_data_sets)

mbc_stats = mean_data_sets['MBC']
mbc_means = mbc_stats.means
mbc_error = mbc_stats.stde

hwec_stats = mean_data_sets['HWES']
hwec_means = hwec_stats.means
hwec_error = hwec_stats.stde

doc_stats = mean_data_sets['WEOC']
doc_means = doc_stats.means
doc_error = doc_stats.stde

total = mbc_means + doc_means + hwec_means

mbc_percent = mbc_means / total * 100
doc_percent = doc_means / total * 100
hwec_percent = hwec_means / total * 100

mbc_error_percent = mbc_error /total * 100
doc_error_percent = doc_error /total * 100
hwec_error_percent = hwec_error /total * 100

# data labels
PARAMETER_NAMES = ['MBC', 'HWES', 'WEOC']
LABELS = [r'$MBC$', r'$HWE_{carbohydrates}$', r'$WEOC$']

# data to plot
SOILS = Constants.LTTs
DAYS = mbc_means.loc[1:].index # exclude day 0
DATA = [mbc_percent, hwec_percent, doc_percent]
ERRORS = [mbc_error_percent, hwec_error_percent, doc_error_percent]

# plotting parameters
rap_as_mathtext = lambda x: rf'${str(x)}$'
X_LABELS = [rap_as_mathtext(day) for day in DAYS]
LENGTH_OF_X = len(X_LABELS)
X_LOCATIONS = numpy.arange(0, LENGTH_OF_X)
BAR_WIDTH = 4

XTICK_LABEL_SIZE = 12

COLORS_OPTIONS = Constants.color_options
COLORS = dict(zip(PARAMETER_NAMES, COLORS_OPTIONS))


def setup_axes(figure, axes_lineup):

    is_first_axes = True if axes_lineup == 0 else False

    first_axes = figure.axes[0] if not is_first_axes else None

    axes_position = (
        131 if axes_lineup == 0 else
        132 if axes_lineup == 1 else
        133
    )

    shared_y_axis = first_axes if not is_first_axes else None
    axes: Axes = figure.add_subplot(axes_position, sharey=shared_y_axis)

    # x ticks
    axes.set_xticks(X_LOCATIONS)
    axes.set_xticklabels(X_LABELS)
    axes.xaxis.set_tick_params(
        length=0,
        pad=10,
        labelsize=XTICK_LABEL_SIZE,
    )

    return axes

def plot_stacked_bars(axes: Axes, x_location, heights, errors, labels, parameter_names):

    bars = {}
    for height, error, label, name in zip(heights, errors, labels, parameter_names):
        error_kw = {
            'elinewidth': 0.8
        }
        bar = axes.bar(
            x=x_location,
            height=height,
            width=BAR_WIDTH,
            yerr=error,
            label=label,
            color=COLORS[name],
            capsize=2,
            error_kw=error_kw
        )

        bars[name] = bar

    return bars


def soil_stacked_bars(soil, figure, axes_lineup):

    axes: Axes = setup_axes(figure, axes_lineup)
    axes.set_title(soil)

    data_sets = [data[soil] for data in DATA]
    errors = [error[soil] for error in ERRORS]

    daily_bars = {}
    for day in DAYS:

        bar_heights = [data_set.loc[day] for data_set in data_sets]
        bar_errors = [error.loc[day] for error in errors]

        bars = plot_stacked_bars(axes, day, bar_heights, bar_errors, LABELS, PARAMETER_NAMES)
        daily_bars[day] = bars

    bars_ = daily_bars[DAYS[0]]
    handles = [value[0] for value in bars_.values()]
    labels = LABELS
    if axes_lineup == 2:
        axes.legend(handles, labels)


# intialize figure
figure: Figure = pyplot.figure()
figure.subplots_adjust(wspace=0)

for i, soil in enumerate(SOILS):

    soil_stacked_bars(soil, figure, i)



