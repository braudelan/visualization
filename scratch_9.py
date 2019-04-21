from get_raw_data import get_multi_sets, get_args
from  get_stats import get_stats

data_keys = get_args()[0]
dataframes = get_multi_sets(data_keys)

print(dataframes['MBC'], dataframes['TOC'])

