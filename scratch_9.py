import pandas
from matplotlib import pyplot

from get_raw_data import get_keys
from get_raw_data import get_single_set
from get_stats    import get_stats
# from get_Ttest    import get_daily_Ttest
# from baseline     import get_baseline


# get tab names to import from file
keys      = get_keys()[0][0]

raw_data = get_single_set(keys)

means, normalized, means_stde = get_stats(raw_data)

"""
get the p-value of Ttest and a boolean for significance 
"""
# for key in keys:
#
#     raw_data          = get_single_set(key)
#     Ttest_mask, Ttest = get_daily_Ttest(raw_data)
#
#     mask_day0         = Ttest_mask.loc[:,0]
#     treatment_labels  = [label for label in mask_day0.index if label[-1] == 't']
#     mask_baseline     = mask_day0.loc[treatment_labels]
#
#     Ttest_day0 = Ttest.loc[:, 0]
#     Ttest_baseline = Ttest_day0.loc[treatment_labels]


# for key in [keys]:
#     data = get_single_set(key)

# # get basic statistics
# means, effect, means_stde = get_stats(raw_data)


# mask, Ttest_values = get_daily_Ttest(raw_data)

# baseline = get_baseline(keys)

