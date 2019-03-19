import pandas

from stats import get_stats

input_file = "all_tests.xlsx"

TESTS = ['MBC', 'MBN', 'DOC', 'HWE-S', 'ERG','RESP', 'AS','TOC']
NUMBERS = range(1, len(TESTS)+1)

stats = {}

for test, number in zip(TESTS, NUMBERS):
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

independent_keys = ['MBC', 'ERG', 'TOC', 'AS']
dependent_keys = ['MBC', 'MBN', 'DOC', 'HWE-S', 'ERG','RESP', 'AS','TOC']

independent_params = [stats[key + '_baseline'] for key in independent_keys]
dependent_params = [stats[key + '_means'] for key in dependent_keys]

i = 1

for ind_p in independent_params :

    figure = pyplot.figure(i)

    for dep_p in dependent_params:
        for day in dep
        figure.add_subplot()


