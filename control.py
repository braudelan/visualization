from matplotlib import pyplot
from matplotlib.ticker import MultipleLocator

from which_round import get_round

def plot_control(control_means, test, number):

# data
    control_means = control_means
    round_factor = get_round(control_means)
    control_means = control_means.round(round_factor)

# plotting parameters
    majorLocator = MultipleLocator(7)
    minorLocator = MultipleLocator(1)

    pyplot.rc('legend', facecolor='inherit', frameon=False, markerscale=1.5)
    pyplot.rc('font', size=18)
    pyplot.rc('lines', linewidth=3)

# text for labels
    title_text = r'mean values of %s for control samples across 28 days of incubation.' % test
    xlabel_text = r'$incubation\ time\ \slash\ days$'

    if test == 'RESP':
        ylabel_text = r'$%s\ \slash\ mg \ast kg\ soil^{-1} \ast day^{-1}$' % test
    else:
        ylabel_text = r'$%s\ \slash\ mg \ast kg\ soil^{-1}$' % test

    labels_text_params = {'size': 19
                          }
# plotting
    control_figure = pyplot.figure(number, figsize=(15,20))

    control_figure.text(0.05, 0, title_text, fontsize=20) # figure title

    axes = control_figure.add_subplot(111)

    control_means.plot(ax=axes,
                       xlim=(0,30),
                      )

    axes.xaxis.set_major_locator(majorLocator)
    axes.xaxis.set_minor_locator(minorLocator)
    axes.tick_params(axis='x', which='minor', width=1, length=3)
    axes.set_ylabel(ylabel_text, labelpad=30, fontdict=labels_text_params)
    axes.set_xlabel(xlabel_text, labelpad=30, fontdict=labels_text_params)

    pyplot.tight_layout(rect=[0.1, 0.1, 0.1, 0.1])

    return control_figure