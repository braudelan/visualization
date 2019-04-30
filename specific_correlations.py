import argparse

import pandas
from matplotlib import pyplot
import matplotlib.backends.backend_pdf

from get_stats import get_stats
from get_qCO2 import get_qCO2
from which_round import get_round

file_for_keys = open('corr_input.txt')
key_names = file_for_keys.readlines()

corr_factor = key_names[0]
ind_keys    = key_names[0]
dep_keys    = key_names[[1],,

qCO2 = get_qCO2()

input_file = "all_tests.xlsx"
TESTS = ['MBC','MBN', 'DOC', 'HWE-S', 'ERG','RESP', 'AS','TOC']

stats = {}
for test in [ind_key, dep_key]:
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

    baseline_means = means.xs('t', level=1, axis=1).loc[0].round(get_round(means))

    total_change = treatment_diff.iloc[-1,:] - baseline_means

    stats[test + '_means'] = means
    stats[test + '_effect'] = effect
    stats[test + '_baseline'] = baseline_means
    stats[test + '_total_change'] = total_change

stats['qCO2_means'] = qCO2
stats['qCO2_baseline'] = qCO2.xs('c', level=1, axis=1).loc[0]

 = stats[ind_key + '_baseline']

for key in ind_keys:
    for dep_key in dep_keys:
        if corr_factor == 'means':
            dep = stats[dep_key + '_means']

        elif corr_factor == 'effect':
            dep = stats[dep_key + '_effect']

        else:
            dep = stats[dep_key + '_total_change']

        title_text = r'$\bf{%s}-\bf{%s}\ \ \ \ day\ %s,\ \ %s$' % arguments
        figure = pyplot.figure('correlate', figsize=(10, 10))
        figure.suptitle(title_text, y=0.95 )

        ax = figure.add_subplot(111)

        ax.set_xticklabels([soil + ', ' + str(value) for soil, value in zip(dep.columns, key.values)])
        ax.xaxis.set_major_locator(pyplot.FixedLocator(key.values))

        ax.plot(key, dep.loc[day], 'rh')

        pdf = matplotlib.backends.backend_pdf.PdfPages("./specific_correlations/%s-%s-%s-%s.pdf" % arguments)
        pdf.savefig(figure)
        pdf.close()

        pyplot.cla()

# todo 1) let the script accept a  file with list of ind_keys and list of dep_keys

# todo 2) after 1) enlarge markers and set them away from plot borders.