import pandas
from matplotlib import pyplot

from raw_data import get_keys
from raw_data import get_raw_data
from stats    import get_stats
from Ttest    import get_daily_Ttest
# from baseline     import get_baseline


# get tab names to import from file
INPUT_FILE = "all_tests.xlsx"

keys_output = get_keys()
if type(keys_output) != tuple:
    KEYS    = get_keys().specific
    NUMBERS = get_keys().numbers
else:
    KEYS    = get_keys()[0]
    NUMBERS = get_keys()[1]

# raw_data = get_raw_data(keys)
#
# means, normalized, means_stde = get_stats(raw_data)
#
# Ttest = get_daily_Ttest(raw_data)
"""
get the p-value of Ttest and a boolean for significance 
"""
# for key in keys:
#
#     raw_data          = get_raw_data(key)
#     Ttest_mask, Ttest = get_daily_Ttest(raw_data)
#
#     mask_day0         = Ttest_mask.loc[:,0]
#     treatment_labels  = [label for label in mask_day0.index if label[-1] == 't']
#     mask_baseline     = mask_day0.loc[treatment_labels]
#
#     Ttest_day0 = Ttest.loc[:, 0]
#     Ttest_baseline = Ttest_day0.loc[treatment_labels]


# for key in [keys]:
#     data = get_raw_data(key)

# # get basic statistics
# means, effect, means_stde = get_stats(raw_data)


# mask, Ttest_values = get_daily_Ttest(raw_data)

# baseline = get_baseline(keys)

