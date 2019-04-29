"""
test significance between soils for a given data set and for every sampling day
"""

import pandas
from pandas import DataFrame
from scipy.stats import ttest_ind


def get_daily_Ttest(raw_data: DataFrame):

    grouped_by_day  = raw_data.groupby('days')        #  days isindex
    by_day_dict     = {}
    for group in grouped_by_day:
        key    = group[0]
        Series = group[1].

    by_day_groups   = dict(list(grouped_by_day))      # dataframe of all soil-treatment pairs for every day

    grouped = raw_data.groupby(level=[0, 1], axis=1)
    groups  = dict(list(grouped))

    Ttest_dic = {}

    for dataframe in by_day_groups.values():

        dataframe   = dataframe.T                              # turn soil-treatment into index
        grouped     = dataframe.groupby(level=[0, 1], axis=1)  # groupby soil-treatment

        # create a dictionary with soil-treatment as key and pandas.Series as value
        list_groups = list(grouped)
        groups      = {}
        labels      = []
        for tup in list_groups:
            key         = tup[0]
            value       = tup[1].iloc[:,0]
            groups[key] = value
            labels.append(key)

        for group in groups:
            for label in labels:




        COM_MIN_t = list(ttest_ind(raw_data.xs(["COM", 't'], level=[0,1]).loc[:, day],
                                 raw_data.xs(["MIN", 't'], level=[0,1]).loc[:, day],
                                 equal_var=False, nan_policy='omit')
                                )
        COM_UNC_t = list(ttest_ind(raw_data.xs(["COM", 't'], level=[0,1]).loc[:, day],
                                 raw_data.xs(["UNC", 't'], level=[0,1]).loc[:, day],
                                 equal_var=False, nan_policy='omit')
                                )
        MIN_UNC_t = list(ttest_ind(raw_data.xs(["MIN", 't'], level=[0,1]).loc[:, day],
                                 raw_data.xs(["UNC", 't'], level=[0,1]).loc[:, day],
                                 equal_var=False, nan_policy='omit')
                                )

        COM_MIN_c = list(ttest_ind(raw_data.xs(["COM", 'c'], level=[0, 1]).loc[:, day],
                                 raw_data.xs(["MIN", 'c'], level=[0, 1]).loc[:, day],
                                 equal_var = False, nan_policy = 'omit')
                                )
        COM_UNC_c = list(ttest_ind(raw_data.xs(["COM", 'c'], level=[0, 1]).loc[:, day],
                                 raw_data.xs(["UNC", 'c'], level=[0, 1]).loc[:, day],
                                 equal_var = False, nan_policy = 'omit')
                                )
        MIN_UNC_c = list(ttest_ind(raw_data.xs(["MIN", 'c'], level = [0, 1]).loc[:, day],
                                 raw_data.xs(["UNC", 'c'], level = [0, 1]).loc[:,day],
                                 equal_var = False, nan_policy = 'omit')
                                )

        all_pairs = {
                     "COM_MIN_t": COM_MIN_t[1],
                     "COM_UNC_t": COM_UNC_t[1],
                     "MIN_UNC_t": MIN_UNC_t[1],
                     "COM_MIN_c": COM_MIN_c[1],
                     "COM_UNC_c": COM_UNC_c[1],
                     "MIN_UNC_c": MIN_UNC_c[1],
                     }

        Ttest_dic[day] = all_pairs

    daily_ttest = pandas.DataFrame.from_dict(Ttest_dic)
    daily_ttest = daily_ttest.astype(float, copy=False).round(5)
    daily_ttest.rename_axis("days", inplace=True)

    mask = daily_ttest < 0.05

    return mask, daily_ttest