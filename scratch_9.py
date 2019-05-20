from pandas import DataFrame
from matplotlib import pyplot
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MultipleLocator, NullLocator

from raw_data import get_setup_arguments
from raw_data import get_raw_data
from stats import get_stats
from Ttest import get_daily_Ttest

# arguments to specify which data sets to load from INPUT_FILE
setup_arguments = get_setup_arguments()

set_name = setup_arguments.sets[0]
number = setup_arguments.numbers[0]

raw_data = get_raw_data(set_name)
stats_output = get_stats(raw_data)
means = stats_output.means

# raw_data.res
# group raw_data by day
groupby_day   = raw_data.groupby('days')
by_day_groups = dict(list(groupby_day))

by_day_Ttest = {}
#
# # group by treatment (MRE\control)
# for daily_data in list(by_day_groups.items()):
#
#     day  = daily_data[0]
#     data = daily_data[1].T
#
#     groupby_treatment = data.groupby(level=[1])
#     treatment_groups  = dict(list(groupby_treatment))
#
#     Ttest_dict = {}
#
#     # group by soil and run Ttest
#     for group in treatment_groups.items():
#
#         treatment = group[0]
#         data      = group[1]
#
#         # groupby
#         groupby_soil = data.groupby(level=[0])
#         list_soils   = list(groupby_soil)
#
#         soil_a = list_soils[0]
#         soil_b = list_soils[1]
#         soil_c = list_soils[2]
#
#         label_ab = (treatment, (soil_a[0], soil_b[0]))
#         label_bc = (treatment, (soil_b[0], soil_c[0]))
#         label_ac = (treatment, (soil_a[0], soil_c[0]))
#
#         data_a = soil_a[1]
#         data_b = soil_b[1]
#         data_c = soil_c[1]
#
#         # Ttest
#         Ttest_ab = ttest_ind(data_a, data_b, equal_var='False', nan_policy='omit')
#         Ttest_bc = ttest_ind(data_b, data_c, equal_var='False', nan_policy='omit')
#         Ttest_ac = ttest_ind(data_a, data_c, equal_var='False', nan_policy='omit')
#
#         Ttest_dict[label_ab] = Ttest_ab[1]  # index [1] = p-value
#         Ttest_dict[label_bc] = Ttest_bc[1]
#         Ttest_dict[label_ac] = Ttest_ac[1]
#
#     by_day_Ttest[day] = Ttest_dict
#
# daily_Ttest = DataFrame.from_dict(by_day_Ttest)  # DataFrame
# daily_Ttest = daily_Ttest.round(get_round(daily_Ttest))
#
