"""
test significance between soils on every sampling day for a given data set
"""

import pandas
from pandas import DataFrame
from scipy.stats import ttest_ind


def get_daily_Ttest(raw_data: DataFrame):

    # group raw_data by day
    groupby_day   = raw_data.groupby('days')            #  days is index
    by_day_groups = dict(list(groupby_day))      #  {day: four replicates of all soil-treatment pairs}

    by_day_Ttest = {}

    # group by treatment (MRE\control)
    for daily_data in list(by_day_groups.items()):

        day  = daily_data[0]
        data = daily_data[1].T

        groupby_treatment = data.groupby(level=[1])
        treatment_groups  = dict(list(groupby_treatment))

        by_treatment_Ttest = {}

        # group by soil and run Ttest
        for group in treatment_groups.items():

            treatment = group[0]
            data      = group[1]

            # groupby
            groupby_soil = data.groupby(level=[0])
            list_soils   = list(groupby_soil)

            soil_a = list_soils[0]
            soil_b = list_soils[1]
            soil_c = list_soils[2]

            label_ab = (treatment, (soil_a[0], soil_b[0]))
            label_bc = (treatment, (soil_b[0], soil_c[0]))
            label_ac = (treatment, (soil_a[0], soil_c[0]))

            data_a = soil_a[1]
            data_b = soil_b[1]
            data_c = soil_c[1]

            # Ttest
            Ttest_ab = ttest_ind(data_a, data_b, equal_var='False', nan_policy='omit')
            Ttest_bc = ttest_ind(data_b, data_c, equal_var='False', nan_policy='omit')
            Ttest_ac = ttest_ind(data_a, data_c, equal_var='False', nan_policy='omit')

            by_treatment_Ttest[label_ab] = Ttest_ab
            by_treatment_Ttest[label_bc] = Ttest_bc
            by_treatment_Ttest[label_ac] = Ttest_ac

        by_day_Ttest[day] = by_treatment_Ttest


    daily_Ttest = pandas.DataFrame.from_dict(by_day_Ttest)

    return daily_Ttest