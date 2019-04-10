from matplotlib import pyplot
from matplotlib.ticker import MultipleLocator

from which_round import get_round

def plot_control(control_means, test):


    control_means = control_means * 24
    round_factor = get_round(control_means)
    control_means = control_means.round(round_factor)

    majorLocator = MultipleLocator(7)
    minorLocator = MultipleLocator(1)

    pyplot.rc('legend', facecolor='inherit', frameon=False, markerscale=1.5)
    pyplot.rc('font', size=18)
    pyplot.rc('lines', linewidth=3)

    title_text = r' %s, control samples, means across 28 days of incubation.' % test
    xlabel_text = r'$incubation\ time\ \slash\ days$'

    if test == 'RESP':
        ylabel_text = r'$%s\ \slash\ mg \ast kg\ soil^{-1} \ast day^{-1}$' % test
    else:
        ylabel_text = r'$%s\ \slash\ mg \ast kg\ soil^{-1}$' % test

    labels_text_params = {'size': 19
                          }

    figure = pyplot.figure(1, figsize=(15,20))
    figure.tight_layout()
    figure.text(0.05, 0.01, title_text, fontsize=20)

    axes = figure.add_subplot(111)

    control_means.plot(ax=axes,
                       xlim=(0,30),
                      )

    axes.xaxis.set_major_locator(majorLocator)
    axes.xaxis.set_minor_locator(minorLocator)
    #
    # else:
    #     control_means.plot(ax=axes,
    #                        kind='bar',
    #                        xlim=(0, 30),
    #                        yerr=means_stde,
    #                )
    axes.tick_params(axis='x', which='minor', width=1, length=3)
    ylabel = axes.set_ylabel(ylabel_text, labelpad=30, fontdict=labels_text_params)
    xlabel = axes.set_xlabel(xlabel_text, labelpad=30, fontdict=labels_text_params)

    return figure