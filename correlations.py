import pandas
from matplotlib import pyplot
import matplotlib.backends.backend_pdf

from raw_data import get_raw_data, get_keys
from stats    import get_stats
from get_qCO2     import get_qCO2


def get_correlation_variables():

    INPUT_FILE = "all_tests.xlsx"

    WHICH_EFFECT_KEY = get_keys().which
    INDEPENDENT_KEY  = get_keys().independent

    if get_keys().specific:
        DEPENDENT_KEYS = get_keys().specific
    else:
        DEPENDENT_KEYS = ['MBC', 'MBN', 'DOC', 'ERG', 'HWE-S', 'RESP', 'AS', 'TOC']

    All_KEYS = list(set(DEPENDENT_KEYS) | set(INDEPENDENT_KEY))


    stats = {}
    for test in All_KEYS:

        # input data into DataFrame
        raw_data = get_raw_data(test)

        # statistics
        means, means_stde, normalized, difference = get_stats(raw_data)

        baseline_means = means.xs('t', level=1, axis=1).loc[0]

        stats[parameter + 'means']        = means
        stats[parameter + 'diff']         = difference
        stats[parameter + 'normalized']   = normalized
        stats[parameter + 'baseline']     = baseline_means

    # METABOLIC_QUATIENT = get_qCO2()
    # stats['qCO2_means'] = qCO2
    # stats['qCO2_baseline'] = qCO2.xs('c', level=1, axis=1).loc[0]

    independent_variables = stats[INDEPENDENT_KEY + 'baseline']

    if  WHICH_EFFECT_KEY == 'norm':
        dependent_variables = [stats[key + 'normalized'] for key in dependent_keys]
    else:
        dependent_variables = [stats[key + 'difference'] for key in dependent_keys]

return indepndent_variables, dependent_variables

i = 1

figures = []

for dependent, dep_key in zip(, dependent_keys):

    figure = pyplot.figure(i, figsize=(16, 8))
    figure.subplots_adjust(hspace=0.3, wspace=0.3)
    figure.suptitle(r'$\bf{%s}$' % dep_key)
    i += 1

    n = 0
    plot_loc = 1
    for day in dep.index:

        plots = pyplot.gcf().get_axes()
        plot_col = [plots[i].colNum for i in range(len(plots) )]
        plot_row = [plots[i].rowNum for i in range(len(plots) )]
        num_days = len(dep.index)
        ind_values = ind.astype(int).values

        if num_days <= 9:
            cols = 3
        else:
            cols = 5

        rows = -(-num_days // cols)

        if n == 0:
            ax = figure.add_subplot(rows, cols, plot_loc)
        else:
            ax = figure.add_subplot(rows, cols, plot_loc, sharex=plots[0], sharey=plots[0])

        # if not plot_col[n] == 0: # Index Error -->on last iteration, n=len(dep.index) while plot_col index is length 9
        #     ax.yaxis.set_major_locator(pyplot.NullLocator())
        # else:
        #     None
        #
        # if not plot_row[n] == 1:
        #     ax.xaxis.set_major_locator(pyplot.NullLocator())
        # else:
        #     None

        ax.set_title(str(day))

        ax.set_xticklabels([soil + ', ' + str(value) for soil, value in zip(dep.columns, ind_values)])
        ax.xaxis.set_major_locator(pyplot.FixedLocator(ind.values))

        ax.plot(ind, dep.loc[day], 'rh')


        n += 1
        plot_loc += 1

    figures.append(figure)


pdf = matplotlib.backends.backend_pdf.PdfPages("./correlations_effect/%s.pdf" % ind_key)
# pdf = matplotlib.backends.backend_pdf.PdfPages("./correlations_means/%s.pdf" % ind_key)
# pdf = matplotlib.backends.backend_pdf.PdfPages("./correlations_total_change/%s.pdf" % ind_key)
for fig in figures:
    pdf.savefig(fig)
pdf.close()


# todo change tick lables into soil catagories
# todo remove y and x labels from inside subplots
# todo increase x_lim so that point markers are not touching the edge of plot
# todo insert argv to be able to run dependent params as either means or effect
#   use an *if* loop for assigning dependent_params on the condition of argv == 'means'
#   or argv == 'effect'

