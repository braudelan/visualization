import pdb
from pandas import DataFrame
from statsmodels.stats.multicomp import MultiComparison, pairwise_tukeyhsd
from scipy.stats import ttest_ind

from raw_data import get_setup_arguments, get_raw_data
from stats import get_stats, normalize_to_control
from growth import get_weekly_growth, tabulate_growth
from helpers import Constants, replace_nan


MBC_raw_data = get_raw_data('MBC')

def replace_None(raw_data):

    TREATMENTS = Constants.treatment_labels
    SOILS = Constants.groups
    DAYS = raw_data.index

    for treatment in TREATMENTS:
        for soil in SOILS:
            for day in DAYS:
                daily_data = raw_data.loc[day, (treatment, soil)]
                daily_mean = daily_data.mean()
                daily_data.fillna(daily_mean, inplace=True)

    return raw_data

if __name__ == '__main__':
    None_handled_raw_data = replace_None(MBC_raw_data)