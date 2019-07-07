import numpy
from pandas import DataFrame

class Constants:

    soils = ['ORG', 'MIN', 'UNC']
    colors = ORG_color, MIN_color, UNC_color = ('xkcd:crimson', 'xkcd:aquamarine', 'xkcd:goldenrod')  #  todo colors (https://python-graph-gallery.com/line-chart/)
    markers = ORG_marker, MIN_marker, UNC_marker = ('*', 'o', 'd')
    treatment_labels = ['c', 't']
    level_labels = ["soil", "treatment", "replicate"]

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



# def replace_nan(data: DataFrame, treatment: str):
#     """replace nan values with the mean of remaining replicates."""
#
#     if len(data.index) >5:
#         week_ends = get_week_ends(data)
#         data = data.loc[week_ends, :]
#
#     data = data.loc[:, (treatment, soils)]
#     data = data.reset_index(col_level=1, col_fill='')
#     data.columns = data.columns.droplevel('treatment')
#
#     for soil in soils:
#         soil_data = data[soil].values
#
#         for i in range(len(soil_data)-1):
#             arr = soil_data[i]
#             where_nan = numpy.isnan(arr)
#             has_nan = numpy.any(where_nan)
#             if has_nan:
#                 mean = arr[numpy.isfinite(arr)].mean()
#                 arr[where_nan] = mean
#
#         data[soil] = soil_data
#
#     return data
#



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

