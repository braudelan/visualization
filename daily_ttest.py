# test sgnificance between soils for every sampling day

import pandas
from pandas import DataFrame
from scipy.stats import ttest_ind


def get_daily_ttest(raw_data: DataFrame):

    raw_data = raw_data.T
    Ttest_dic = {}

    for day in list(raw_data.columns):

        COM_MIN_t = list(ttest_ind(raw_data.xs(["COM", 't'], level=[0,1]).loc[:, day],
                                 raw_data.xs(["MIN", 't'], level=[0,1]).loc[:, day],
                                 equal_var=False, nan_policy='omit')
                                )
        COM_UND_t = list(ttest_ind(raw_data.xs(["COM", 't'], level=[0,1]).loc[:, day],
                                 raw_data.xs(["UND", 't'], level=[0,1]).loc[:, day],
                                 equal_var=False, nan_policy='omit')
                                )
        MIN_UND_t = list(ttest_ind(raw_data.xs(["MIN", 't'], level=[0,1]).loc[:, day],
                                 raw_data.xs(["UND", 't'], level=[0,1]).loc[:, day],
                                 equal_var=False, nan_policy='omit')
                                )

        COM_MIN_c = list(ttest_ind(raw_data.xs(["COM", 'c'], level=[0, 1]).loc[:, day],
                                 raw_data.xs(["MIN", 'c'], level=[0, 1]).loc[:, day],
                                 equal_var = False, nan_policy = 'omit')
                                )
        COM_UND_c = list(ttest_ind(raw_data.xs(["COM", 'c'], level=[0, 1]).loc[:, day],
                                 raw_data.xs(["UND", 'c'], level=[0, 1]).loc[:, day],
                                 equal_var = False, nan_policy = 'omit')
                                )
        MIN_UND_c = list(ttest_ind(raw_data.xs(["MIN", 'c'], level = [0, 1]).loc[:, day],
                                 raw_data.xs(["UND", 'c'], level = [0, 1]).loc[:,day],
                                 equal_var = False, nan_policy = 'omit')
                                )

        all_pairs = {
                     "COM-MIN_t": COM_MIN_t[1],
                     "COM-UND_t": COM_UND_t[1],
                     "MIN-UND_t": MIN_UND_t[1],
                     "COM_MIN_c": COM_MIN_c[1],
                     "COM_UND_c": COM_UND_c[1],
                     "MIN_UND_c": MIN_UND_c[1],
                     }

        Ttest_dic[day] = all_pairs

        daily_ttest = pandas.DataFrame.from_dict(Ttest_dic).T
        daily_ttest = daily_ttest.rename_axis("days", inplace=True)

        return daily_ttest