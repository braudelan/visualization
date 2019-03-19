import pandas
from matplotlib import pyplot

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
    stats[test + '_baseline'] = baseline_means

independent_keys = ['MBC', ]
dependent_keys = ['HWE-S',]

independent_params = [stats[key + '_baseline'] for key in independent_keys]
dependent_params = [stats[key + '_means'].xs('t', level=1,axis=1) for key in dependent_keys]

i = 1

for ind, ind_key in zip(independent_params, independent_keys) :

    for dep, dep_key in zip(dependent_params, dependent_keys):

        figure = pyplot.figure(i)
        figure.subplots_adjust(hspace=0.2, wspace=0.2)

        i += 1

        n = 1
        for day in dep.index:

            num_days = len(dep.index)

            if num_days <= 9:
                cols = 3
            else:
                cols = 5

            rows = -(-num_days // cols)
            axes = figure.add_subplot(rows, cols, n)

            axes.plot(ind, dep.loc[day], 'ro')

            n += 1

        figure.savefig("./correlation_figures/%s_%s.png" %(ind_key, dep_key) , bbox_inches='tight', pad_inches=2)

