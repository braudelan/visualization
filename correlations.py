import pandas
from matplotlib import pyplot
import matplotlib.backends.backend_pdf

from stats import get_stats
from get_qCO2 import get_qCO2

qCO2 = get_qCO2()

input_file = "all_tests.xlsx"
TESTS = ['MBC','MBN', 'DOC', 'HWE-S', 'ERG','RESP', 'AS','TOC']

stats = {}
for test in TESTS:
    # input data into DataFrame
    raw_data = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                     sheet_name=test,
                                     na_values=["-", " "]).rename_axis("days")
    raw_data.columns.rename(["soil", "treatment", "replicate"],
                            level=None, inplace=True)
    raw_data.columns.set_levels(["c", "t"], level=1, inplace=True)

    #get statistics and parameters
    means, means_stde, effect = get_stats(raw_data)

    diff = means.diff(periods=1, axis=1)
    treatment_diff = diff.xs("t", axis=1, level=1)

    baseline_means = means.xs('t', level=1, axis=1).loc[0]

    total_change = treatment_diff.iloc[-1,:] - baseline_means

    stats[test + '_means'] = means
    stats[test + '_effect'] = effect
    stats[test + '_baseline'] = baseline_means
    stats[test + '_total_change'] = total_change

stats['qCO2_means'] = qCO2
stats['qCO2_baseline'] = qCO2.xs('c', level=1, axis=1).loc[0]

independent_keys = ['MBC','MBN', 'DOC', 'HWE-S', 'ERG','RESP', 'AS','TOC','qCO2']
dependent_keys = ['MBC','HWE-S', 'MBN', 'DOC', 'ERG','RESP', 'AS','TOC',]

independent_params = [stats[key + '_baseline'] for key in independent_keys]
# dependent_params = [stats[key + '_means'].xs('t', level=1,axis=1) for key in dependent_keys]
dependent_params = [stats[key + '_effect'] for key in dependent_keys]
# dependent_params = [stats[key + '_total_change'] for key in dependent_keys]

i = 1

for ind, ind_key in zip(independent_params, independent_keys) :

    figures = []

    for dep, dep_key in zip(dependent_params, dependent_keys):

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

