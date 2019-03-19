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
    stats[test + ' baseline'] = baseline_means

baseline_params = ['MBC', 'ERG', 'TOC', 'AS']

for p in baseline_params :

    figure =
    figure.add_subplot()


