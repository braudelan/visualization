import argparse

import pandas
from matplotlib import pyplot
import matplotlib.backends.backend_pdf

from raw_data import get_raw_data, get_setup_arguments
from get_stats import get_stats
from get_qCO2 import get_qCO2
from which_round import get_round


file_for_keys = open('corr_input.txt')
keys_lines    = file_for_keys.readlines()

WHICH_NORMALIZATION   = keys_lines[0]
INDEPENDENT_VARIABLES = keys_lines[1]
SOILS                 = ['COM', 'MIN', 'UNC']


i = 2
for ind_key in INDEPENDENT_VARIABLES:
    DEPENDENT_VARIABLES = keys_lines[i]

    independent_raw_data = get_raw_data(ind_key).T
    independent_baseline = independent_raw_data.loc[('control',SOILS), 0]

    for dep_key DEPENDENT_VARIABLES:
        dependent_raw_data = get_raw_data(dep_key).T
        dependent_data = dependent_data.loc[('MRE', SOILS), :]

        for day in independent_raw_data.columns:

# todo plot *ind* against every *dep* in DEPENDENT_VARIABLES using *ind*, *dep* and *day* as title















for ind_key in INDEPENDENT_KEY:
    for dep_key in DEPENDENT_VARIABLES:
        if WHICH_TO_CORRELATE_KEY == 'means':
            dep = stats[dep_key + '_means']

        elif WHICH_TO_CORRELATE_KEY == 'normalized':
            dep = stats[dep_key + '_normalized']


        title_text = r'$\bf{%s}-\bf{%s}\ \ \ \ day\ %s,\ \ %s$' % arguments
        figure = pyplot.figure('correlate', figsize=(10, 10))
        figure.suptitle(title_text, y=0.95 )

        ax = figure.add_subplot(111)

        ax.set_xticklabels([soil + ', ' + str(value) for soil, value in zip(dep.columns, ind_key.values)])
        ax.xaxis.set_major_locator(pyplot.FixedLocator(ind_key.values))

        ax.plot(ind_key, dep.loc[day], 'rh')

        pdf = matplotlib.backends.backend_pdf.PdfPages("./specific_correlations/%s-%s-%s-%s.pdf" % arguments)
        pdf.savefig(figure)
        pdf.close()

        pyplot.cla()

# todo 1) let the script accept a  file with list of ind_keys and list of dep_keys

# todo 2) after 1) enlarge markers and set them away from plot borders.