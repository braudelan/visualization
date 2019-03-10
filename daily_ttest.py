# test sgnificance between soils for every sampling day

import pandas
from scipy.stats import ttest_ind

def get_daily_ttest()
Ttest_dic = {}
for day in list(dataframe.index):
    data_MRE = dataframe.T.xs("t", level=1)

    COM_MIN = list(ttest_ind(data_MRE.xs("COM", level=0).loc[:, day],
                             data_MRE.xs("MIN", level=0).loc[:, day],
                             equal_var=False, nan_policy='omit')
                   )
    COM_UND = list(ttest_ind(data_MRE.xs("COM", level=0).loc[:, day],
                             data_MRE.xs("UND", level=0).loc[:, day],
                             equal_var=False, nan_policy='omit')
                   )
    MIN_UND = list(ttest_ind(data_MRE.xs("MIN", level=0).loc[:, day],
                             data_MRE.xs("UND", level=0).loc[:, day],
                             equal_var=False, nan_policy='omit')
                   )

    all_pairs = {"COM-MIN": COM_MIN[1],
                 "COM-UND": COM_UND[1],
                 "MIN-UND": MIN_UND[1]
                 }
    Ttest_dic[day] = all_pairs

daily_ttest = pandas.DataFrame.from_dict(Ttest_dic).T
daily_ttest.rename_axis("days", inplace=True)
