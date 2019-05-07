"""
test significance between soils on every sampling day for a given data set
"""

from pandas      import DataFrame
from matplotlib  import pyplot
from scipy.stats import ttest_ind

from which_round import get_round


def get_daily_Ttest(raw_data: DataFrame):

    # group raw_data by day
    groupby_day   = raw_data.groupby('days')
    by_day_groups = dict(list(groupby_day))

    by_day_Ttest = {}

    # group by treatment (MRE\control)
    for daily_data in list(by_day_groups.items()):

        day  = daily_data[0]
        data = daily_data[1].T

        groupby_treatment = data.groupby(level=[1])
        treatment_groups  = dict(list(groupby_treatment))

        Ttest_dict = {}

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

            Ttest_dict[label_ab] = Ttest_ab[1]  # index [1] = p-value
            Ttest_dict[label_bc] = Ttest_bc[1]
            Ttest_dict[label_ac] = Ttest_ac[1]

        by_day_Ttest[day] = Ttest_dict

    daily_Ttest = DataFrame.from_dict(by_day_Ttest)  # DataFrame
    daily_Ttest = daily_Ttest.round(get_round(daily_Ttest))

    return daily_Ttest


def tabulate_daily_Ttest(daily_ttest, test):

    title_text = r'%s daily Ttest' %test

    figure_5 = pyplot.figure(3)
    figure_5.tight_layout()

    axes = figure_5.add_subplot(111)
    axes.axis('off')
    axes.axis('tight')
    ttest_title = axes.set_title(title_text, pad=0.2, fontsize=20, position=(0, 1.1))

    # ttest_columns = daily_ttest.columns

    ttest_table = pyplot.table(cellText=daily_ttest.values,
                               loc='center',
                               colLabels=daily_ttest.columns,
                               rowLabels=daily_ttest.index,
                               cellLoc='center',
                               colWidths=[0.1 for x in daily_ttest.columns],
                               # bbox = [0.0, -1.3, 1.0, 1.0]
                               )

    for cell in ttest_table._cells:
        if cell[0] == 0 or cell[1] == -1:
            ttest_table._cells[cell].set_text_props(weight='bold')

    ttest_table.scale(2, 3)

    return figure_5