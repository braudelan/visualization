import pandas
from matplotlib import pyplot
import matplotlib.backends.backend_pdf

from stats import get_stats


input_file = "all_tests.xlsx"

TESTS = ['MBC', 'MBN', 'DOC', 'HWE-S', 'ERG','RESP', 'AS','TOC']
# NUMBERS = range(1, len(TESTS)+1)

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
    means, means_stde, treatment_effect = get_stats(raw_data)

    baseline_means = means.xs('t', level=1, axis=1).loc[0]

    stats[test + '_means'] = means
    stats[test + '_effect'] = treatment_effect
    stats[test + '_baseline'] = baseline_means

independent_keys = ['MBC','RESP','HWE-S', 'AS', 'ERG', 'TOC',   ]
dependent_keys = ['MBC','HWE-S', 'AS', 'TOC', 'DOC', 'MBN', ]

independent_params = [stats[key + '_baseline'] for key in independent_keys]
# dependent_params = [stats[key + '_means'].xs('t', level=1,axis=1) for key in dependent_keys]
dependent_params = [stats[key + '_effect'] for key in dependent_keys]
i = 1

for ind, ind_key in zip(independent_params, independent_keys) :

    figures = []

    for dep, dep_key in zip(dependent_params, dependent_keys):

        figure = pyplot.figure(i, figsize=(10,20))
        figure.subplots_adjust(hspace=0.3, wspace=0.3)
        figure.suptitle(r'$\cal{%s}$' % dep_key)
        i += 1

        n = 1
        axes = {}

        for day in dep.index:

            num_days = len(dep.index)

            if num_days <= 9:
                cols = 3
            else:
                cols = 5

            rows = -(-num_days // cols)

            if n > 1:
                axes[str(n)] = figure.add_subplot(rows, cols, n, sharex=axes['1'], sharey=axes['1'])
            else:
                axes[str(n)] = figure.add_subplot(rows, cols, n)

            axes[str(n)].set_title(str(day))

            axes[str(n)].plot(ind, dep.loc[day], 'rh')


            n += 1

        figures.append(figure)

    pyplot.cla()

    pdf = matplotlib.backends.backend_pdf.PdfPages("./correlations_in_pdf/%s.pdf" % ind_key)
    for fig in figures:
        pdf.savefig(fig)
    pdf.close()


# todo change tick lables into soil catagories
# todo remove y and x labels from inside subplots
# todo increase x_lim so that point markers are not touching the edge of plot
# todo insert argv to be able to run dependent params as either means or effect
#   use an *if* loop for assigning dependent_params on the condition of argv == 'means'
#   or argv == 'effect'

