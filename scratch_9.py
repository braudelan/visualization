from pandas import DataFrame
from matplotlib import pyplot
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MultipleLocator, NullLocator

from raw_data import get_setup_arguments
from raw_data import get_raw_data
from stats    import get_stats

def plot_data(data, std_error, axes):
    """
    plot a time series data.

    plot a dataframe into a single subplot
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
    x_data = data['days']
    data_columns = data.columns[1:]
    colors = ['b', 'g', 'r']
    which_data = 'means' if len(data.columns) == 7 else 'normalized'

    chart_kind = 'line' if num_data_points > 5 else 'bar'

    lines = {}
    for column_name in data_columns:

        treatment_label = column_name[0]
        soil_label = column_name[2:] if  which_data == 'means' else column_name

        y_data = data[column_name]
        y_error = std_error[column_name] if which_data == 'means' else None

        color = (
                 colors[0] if (soil_label == 'COM') else
                 colors[1] if (soil_label == 'MIN') else
                 colors[2]
                )
        style = densly_dashed if treatment_label == 'c' else solid

        ax = axes.errorbar(
                  x_data,
                  y_data,
                  yerr=y_error,
                  label=column_name,
                  color=color,
                  ls=style,
                 )

        lines[column_name] = ax

    return lines

# arguments to specify which data sets to load from INPUT_FILE
setup_arguments = get_setup_arguments()

set_name = setup_arguments.sets[0]
number = setup_arguments.numbers[0]

raw_data = get_raw_data(set_name)

BasicStats = get_stats(raw_data)

means = BasicStats.means
normalized = BasicStats.normalized_diff
means_stde = BasicStats.means_stde
normalized_stde = None
for frame in [means, means_stde]:
    frame.columns = frame.columns.map('_'.join)
    frame.reset_index(inplace=True)
normalized.reset_index(inplace=True)

# local parameters
last_day = means.index[-1]     # last sampling day
num_data_points = len(means.index)    # number of sampling days
excluded = normalized.iloc[1:, :]  # treatment effect without day 0


# pyplot parameters
major_locator = MultipleLocator(7)  # major ticks locations
minor_locator = MultipleLocator(1)  # minor ticks locations

pyplot.rc('legend', facecolor='inherit', frameon=False, markerscale=1.5)
pyplot.rc('font', size=18)
pyplot.rc('lines', linewidth=3)

symbol_text_params = {'weight': 'bold',
                      'size': 26,
                      }
label_text_params = {'size': 19}

marker_treatment_line = []

line_styles = densly_dashed, solid = ((0, (2, 1)), (0, ()))

# text
title_text = r'$\bf{Figure %s.}$ means of %s across %s days of incubation. (a) all soils, ' \
             r'(b) normalized to control' % (number, set_name, last_day)

xlabel_text = r'$incubation\ time\ \slash\ days$'

if set_name == 'RESP':
    means_ylabel_text = r'$%s\ \slash\ mg\ CO_{2}-C\ \ast\ kg\ soil^{-1}\ \ast\ h^{-1} $' % set_name
else:
    means_ylabel_text = r'$%s\ \slash\ mg \ast kg\ soil^{-1}$' % set_name

normalized_ylabel_text = r'$%s\ normalized\ \slash\ percent\ of\ control$' % set_name


# create and adjut figure
figure_1 = pyplot.figure(number, figsize=(15,20))
figure_1.tight_layout()
figure_1.subplots_adjust(hspace=0.3)
figure_1.text(0.05, 0.01, title_text, fontsize=20)


# create all means axes and set parameters
means_axes = figure_1.add_subplot(211)

means_axes.xaxis.set_minor_locator(minor_locator)
means_axes.xaxis.set_major_locator(major_locator)
means_axes.tick_params(axis='x', which='minor', width=1, length=3)
means_axes.text(0.03, 1.05, "a", transform=means_axes.transAxes, fontdict=symbol_text_params)  # symbol
means_axes.set_ylabel(means_ylabel_text, labelpad=30, fontdict=label_text_params)
means_axes.set_xlabel('')


# plot all means
means_lines = plot_data(means, means_stde, num_data_points, means_axes)

# costumize all means legend
list_lines = list(means_lines.items())
lables = []
handles = []
for line in list_lines[3:]:
    label = line[0][2:]
    handel = line[1]
    lables.append(label)
    handles.append(handel)
treatment_labels = ['MRE apllied', 'control']
lables.extend(treatment_labels)
treatment_handles = [Line2D([0], [0], linewidth=5, linestyle=solid, color='k'),
                     Line2D([0], [0], linewidth=5, linestyle=densly_dashed, color='k')]
handles.extend(treatment_handles)
means_legend = means_axes.legend(handles, lables)

Patch


# create normalized axes and set parameters
normalized_axes = figure_1.add_subplot(212)

normalized_axes.xaxis.set_major_locator(major_locator)
normalized_axes.xaxis.set_minor_locator(minor_locator)
normalized_axes.set_ylabel(normalized_ylabel_text, labelpad=30, fontdict=label_text_params)
normalized_axes.set_xlabel(xlabel_text, labelpad=30, fontdict=label_text_params)
normalized_axes.tick_params(axis='x', which='minor', width=1,length=3)
normalized_axes.text(0.03, 1.05, "b", transform=normalized_axes.transAxes, fontdict=symbol_text_params)

# plot normalized
normalized_lines = plot_data(normalized, normalized_stde, num_data_points, normalized_axes )

normalized_axes.legend()
figure_1.savefig('./test.png')

