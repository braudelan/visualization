import numpy
from pandas import DataFrame


SOILS = ['ORG', 'MIN', 'UNC']


def get_week_ends(dataframe):

    every_7th = dataframe.index.isin([0, 7, 14, 21, 28])

    return every_7th

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


def replace_nan(data: DataFrame, treatment: str):
    """replace nan values with the mean of remaining replicates."""

    if len(data.index) >5:
        week_ends = get_week_ends(data)
        data = data.loc[week_ends, :]

    data = data.loc[:, (treatment, SOILS)]
    data = data.reset_index(col_level=1, col_fill='')
    data.columns = data.columns.droplevel('treatment')

    for soil in SOILS:
        soil_data = data[soil].values

        for i in range(len(soil_data)-1):
            arr = soil_data[i]
            where_nan = numpy.isnan(arr)
            has_nan = numpy.any(where_nan)
            if has_nan:
                mean = arr[numpy.isfinite(arr)].mean()
                arr[where_nan] = mean

        data[soil] = soil_data

    return data


