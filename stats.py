import pandas
from matplotlib import pyplot
from matplotlib.ticker import MultipleLocator

def get_stats(raw_data):

    # means
    groupby_soil_treatment = raw_data.groupby(level=[0, 1],axis=1)  # group 4 replicates from every soil-treatment pair
    means                  = groupby_soil_treatment.mean()          # means of 4 replicates
    means_stde             = groupby_soil_treatment.sem()           # stnd error of means

    # means of control
    control      = means.xs('c', axis=1, level=1)

    #treatment effect
    substract  = means.diff(periods=1, axis=1)       # substracting across columns, right to left
    difference = substract.xs("t", axis=1, level=1)  # treatment - control
    normalized = difference / control * 100          # difference normalized to control (percent)

    stats = {'control': control}

    return means, normalized, means_stde, difference



def plot_stats(means, normalized, means_stde, number, test):

# local variabels
    last_day = means.index[-1]     # last sampling day
    len_days = len(means.index)    # number of sampling days
    excluded = normalized.iloc[1:, :]  # treatment effect without day 0

# pyplot parameters
    majorLocator = MultipleLocator(7)  # major ticks locations
    minorLocator = MultipleLocator(1)  # minor ticks locations

    pyplot.rc('legend', facecolor='inherit', frameon=False, markerscale=1.5)
    pyplot.rc('font', size=18)
    pyplot.rc('lines', linewidth=3)

    symbol_text_params = {'weight': 'bold',
                          'size': 26,
                          }
    label_text_params = {'size': 19}

    marker_treatment_line = []

# text
    title_text = r'$\bf{Figure %s.}$ means of %s across %s days of incubation. (a) all soils, ' \
                 r'(b) normalized to control' % (number, test, last_day)

    xlabel_text = r'$incubation\ time\ \slash\ days$'

    if test == 'RESP':
        means_ylabel_text = r'$%s\ \slash\ mg\ CO_{2}-C\ \ast\ kg\ soil^{-1}\ \ast\ h^{-1} $' % test
    else:
        means_ylabel_text = r'$%s\ \slash\ mg \ast kg\ soil^{-1}$' %test

    normalized_ylabel_text = r'$%s\ normalized\ \slash\ percent\ of\ control$' %test

# create and adjut figure
    figure_1 = pyplot.figure(number, figsize=(15,20))
    figure_1.tight_layout()
    figure_1.subplots_adjust(hspace=0.3)
    figure_1.text(0.05, 0.01, title_text, fontsize=20)


# plot means of all expr. units
    means_axes = figure_1.add_subplot(211)

    if len_days > 5:
        means.plot(
                   ax=means_axes,
                   xlim=(0,last_day + 1),
                   yerr=means_stde,
                   )

        means_axes.xaxis.set_major_locator(majorLocator)
        means_axes.xaxis.set_minor_locator(minorLocator)
        means_axes.legend(means_axes.get_lines(), (means.columns))

    else:
        means.plot(
                   ax=means_axes,
                   kind='bar',
                   xlim=(0, last_day + 1),
                   yerr=means_stde,
                   )

    means_axes.tick_params(axis='x', which='minor', width=1, length=3)
    means_axes.text(0.03, 1.05, "a", transform=means_axes.transAxes, fontdict=symbol_text_params)  # symbol
    means_axes.set_ylabel(means_ylabel_text, labelpad=30, fontdict=label_text_params)
    means_axes.set_xlabel('')


# plot treatment effect as percent of control
    normalized_axes = figure_1.add_subplot(212)

    if len_days > 5 :
        normalized.plot(
                    ax=normalized_axes,
                    xlim=(0,last_day + 1),
                   )

        normalized_axes.xaxis.set_major_locator(majorLocator)
        normalized_axes.xaxis.set_minor_locator(minorLocator)
        normalized_axes.legend(normalized_axes.get_lines(), (normalized.columns))

    elif len_days > 3:

        normalized.plot(ax=normalized_axes,
                              kind='bar',
                              xlim=(0, last_day + 1),
                              )
        normalized_axes.legend(normalized_axes.containers, (normalized.columns))

    else:

        excluded.plot(ax=normalized_axes,
                    kind='bar',
                    xlim=(0, last_day + 1),
                    )
        normalized_axes.legend(normalized_axes.containers, (normalized.columns))

    normalized_axes.set_ylabel(normalized_ylabel_text, labelpad=30, fontdict=label_text_params)
    normalized_axes.set_xlabel(xlabel_text, labelpad=30, fontdict=label_text_params)
    normalized_axes.tick_params(axis='x', which='minor', width=1,length=3)
    normalized_axes.text(0.03, 1.05, "b", transform=normalized_axes.transAxes, fontdict=symbol_text_params)

    return figure_1
