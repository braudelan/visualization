''''''
from data.raw_data import get_raw_data
from data.growth import get_weekly_growth
from data.cumulative_respiration import get_weekly_respiration
from data.helpers import *

def get_carbon_efficiency(treatment):

    # raw data
    raw_mbc = get_raw_data('MBC')[treatment]
    weekly_growth_stats = get_weekly_growth(raw_mbc)
    weekly_respiration_stats = get_weekly_respiration(treatment)

    # means and stnd errors
    weekly_growth = weekly_growth_stats.means
    weekly_growth = weekly_growth.drop(4)
    growth_error = weekly_growth_stats.stde
    growth_error = growth_error.drop(4)
    weekly_respiration = weekly_respiration_stats.means
    repiration_error = weekly_respiration_stats.stde

    # assimilation-to-consumption ratio (CUE)
    CUE = weekly_growth / (weekly_respiration + weekly_growth)

    # error propogation
    growth_relative_err = growth_error / weekly_growth
    respiration_relative_err = repiration_error / weekly_respiration
    CUE_error = propagate_error(CUE, respiration_relative_err, growth_relative_err)

    return Stats(
        means=CUE,
        stde=CUE_error,
    )



