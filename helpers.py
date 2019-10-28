import pdb
import numpy
from pandas import DataFrame

class Constants:

    groups = ['ORG', 'MIN', 'UNC']
    color_options = ('darkred', 'royalblue', 'dimgrey')
    colors =  dict(zip(groups, color_options))
    marker_options = ('*', 'o', 'd')
    markers =  dict(zip(groups, marker_options))
    line_style_labels = ('solid', 'broken', 'dotted')
    line_style_options = ('-', '-.', ':')
    line_styles = dict(zip(line_style_labels, line_style_options))
    treatment_labels = ['c', 't']
    level_labels = ["soil", "treatment", "replicate"]
    input_file_name = "all_tests.xlsx"
    output_folder = '/home/elan/Dropbox/research/figures'


def get_week_ends(dataframe):

    every_7th = dataframe.index.isin([0, 7, 14, 21, 28])

    return every_7th


def delay_factor(x, delay):
    ''' return a function alternating between 0 and 1 with delay.'''

    N_HARMONICS = 1000
    CYCLE = 28

    def bn(n):
        n = int(n)
        if (n % 2 != 0):
            return 2 / (pi * n)
        else:
            return 0

    # Wn
    def wn(n):
        wn = (2 * pi * n) / CYCLE
        return wn

    a0 = 0.5
    partialSums = a0
    for n in range(1, N_HARMONICS):
        partialSums = partialSums + bn(n) * sin(wn(n) * (x - delay))
    return partialSums


def replace_None(raw_data):

    TREATMENTS = Constants.treatment_labels
    SOILS = Constants.groups
    DAYS = raw_data.index

    for treatment in TREATMENTS:
        for soil in SOILS:
            for day in DAYS:
                daily_data = raw_data.loc[day, (treatment, soil)]
                daily_mean = daily_data.mean()
                daily_data.fillna(daily_mean, inplace=True)

    return raw_data


# def get_round(dataframe):
#
#     number = dataframe.min().min()
#     bounds = h, m, l = (10, 0.1, 0.01)
#
#     if number >= h:
#         return 0
#
#     if number < h and number >= m:
#         return 2
#
#     elif number < m  and number >= l:
#         return 3
#
#     else:
#         return 4

