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


def replace_nan(raw_data: DataFrame, treatment: str) -> DataFrame:
    """replace nan values with the mean of remaining replicates."""

    SOILS = Constants.groups
    # if len(raw_data.index) >5:
    #     week_ends = get_week_ends(raw_data)
    #     raw_data = raw_data.loc[week_ends, :]

    data = raw_data.loc[:, (treatment, SOILS)]
    data = data.reset_index(col_level=1, col_fill='')
    data.columns = data.columns.droplevel('treatment')

    for soil in SOILS:
        soil_data = data[soil].values

        for i in range(len(soil_data)):
            array = soil_data[i]
            where_nan = numpy.isnan(array)
            has_nan = numpy.any(where_nan)
            if has_nan:
                mean = array[numpy.isfinite(array)].mean()
                array[where_nan] = mean

        data[soil] = soil_data

    return data




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

