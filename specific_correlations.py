import argparse

import pandas
from matplotlib import pyplot
import matplotlib.backends.backend_pdf

from raw_data import get_raw_data, get_keys
from stats import get_stats
from get_qCO2 import get_qCO2
from which_round import get_round

file_for_keys = open('corr_input.txt')
keys          = file_for_keys.readlines()

WHICH_DEPENDENT_LINE  = keys[0]
INDEPENDENT_KEYS_LINE = keys[1]

independent_dependent = {}
i = 2
for key in INDEPENDENT_KEYS_LINE:
    dependent_keys = keys[i]

    independent_raw_data = get_raw_data(key).T
    independent_baseline = independent_raw_data.loc[]







    independent_dependent['key'] = dependent_keys
    i += 1

for item in independent_dependent.items():
    independent_key = item[0]
    dep































                    qCO2 = get_qCO2()

d_variabels, i_variabels = get_keys()

input_file = "all_tests.xlsx"
TESTS = ['MBC','MBN', 'DOC', 'HWE-S', 'ERG','RESP', 'AS','TOC']

stats = {}
for test in [ind_key, dep_key]:
    # input data into DataFrame
    raw_data = get_raw_data(test)

    #get statistics and parameters
    means, normalized, normalized, difference = get_stats(raw_data)

    baseline_means = means.xs('t', level=1, axis=1).loc[0].round(get_round(means))

    total_change = treatment_diff.iloc[-1,:] - baseline_means

    stats[test + '_means']    = means
    stats[test + '_normalized']   = normalized
    stats[test + '_diff']     = difference
    stats[test + '_baseline'] = baseline_means

stats['qCO2_means'] = qCO2
stats['qCO2_baseline'] = qCO2.xs('c', level=1, axis=1).loc[0]


for key in INDEPENDENT_KEY:
    for dep_key in DEPENDENT_KEYS:
        if WHICH_TO_CORRELATE_KEY == 'means':
            dep = stats[dep_key + '_means']

        elif WHICH_TO_CORRELATE_KEY == 'normalized':
            dep = stats[dep_key + '_normalized']


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