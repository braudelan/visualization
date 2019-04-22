import pandas

from get_raw_data import get_single_set,get_multi_sets, get_args
from  get_stats import get_stats
from get_Ttest import get_daily_Ttest


data_keys = get_args()[0][0]
raw_data = get_single_set(data_keys)

means, effect, means_stde = get_stats(raw_data)

mask, Ttest_values = get_daily_Ttest(raw_data)
