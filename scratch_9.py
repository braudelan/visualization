import pandas

from get_raw_data import get_keys
from get_raw_data import get_single_set
from get_stats    import get_stats
from get_Ttest    import get_daily_Ttest
from baseline     import get_baseline


# get tab names to import from file
keys          = get_keys()[0]
raw_data      = get_single_set(keys[0])
Ttest_mask    = get_daily_Ttest(raw_data)[0]
mask_day0     = Ttest_mask.loc[:,0]
mask_baseline = mask_day0

# # get raw data
# for key in [keys]:
#     data = get_single_set(key)

# # get basic statistics
# means, effect, means_stde = get_stats(raw_data)


# mask, Ttest_values = get_daily_Ttest(raw_data)

baseline_frame = get_baseline(keys)