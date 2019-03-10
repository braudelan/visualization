# test sgnificance between soils for every sampling day

import pandas
from pandas import DataFrame
from scipy.stats import ttest_ind


def get_daily_ttest(raw_data: DataFrame)

    Ttest_dic = {}

    for day in list(raw_data.index):

        COM_MIN = list(ttest_ind(raw_data.xs("COM", level=0).loc[:, day],
                                 raw_data.xs("MIN", level=0).loc[:, day],
                                 equal_var=False, nan_policy='omit')
                       )
        COM_UND = list(ttest_ind(raw_data.xs("COM", level=0).loc[:, day],
                                 raw_data.xs("UND", level=0).loc[:, day],
                                 equal_var=False, nan_policy='omit')
                       )
        MIN_UND = list(ttest_ind(raw_data.xs("MIN", level=0).loc[:, day],
                                 raw_data.xs("UND", level=0).loc[:, day],
                                 equal_var=False, nan_policy='omit')
                       )

        all_pairs = {"COM-MIN": COM_MIN[1],
                     "COM-UND": COM_UND[1],
                     "MIN-UND": MIN_UND[1]
                     }
        Ttest_dic[day] = all_pairs

    daily_ttest = pandas.DataFrame.from_dict(Ttest_dic).T
    daily_ttest = daily_ttest.rename_axis("days", inplace=True)

    return daily_ttest