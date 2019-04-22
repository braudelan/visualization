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
                     "COM-MIN_t": COM_MIN_t[1],
                     "COM-UNC_t": COM_UNC_t[1],
                     "MIN-UNC_t": MIN_UNC_t[1],
                     "COM_MIN_c": COM_MIN_c[1],
                     "COM_UNC_c": COM_UNC_c[1],
                     "MIN_UNC_c": MIN_UNC_c[1],
                     }

        Ttest_dic[day] = all_pairs

    daily_ttest = pandas.DataFrame.from_dict(Ttest_dic)
    daily_ttest = daily_ttest.astype(float, copy=False).round(5)
    daily_ttest.rename_axis("days", inplace=True)

    return daily_ttest
    return Ttest_dic


# create a boelean mask dataframe of significance
# for every pair of soils on every sampling day

def significance(Ttest_dict):

    for day in Ttest_dict.keys():
            mask = pandas.DataFrame.from_dict(Ttest_dict[day], orient='index', columns=day)



