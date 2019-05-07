import pandas
from matplotlib import pyplot

from raw_data import get_keys
from raw_data import get_raw_data
from stats    import get_stats
from Ttest    import get_daily_Ttest
# from baseline     import get_baseline


# get tab names to import from file
INPUT_FILE = "all_tests.xlsx"

keys = get_keys().specific[0]
raw_data = get_raw_data(keys)
#
means, normalized, means_stde, diff = get_stats(raw_data)
#
Ttest = get_daily_Ttest(raw_data)
mask  = Ttest < 0.05

