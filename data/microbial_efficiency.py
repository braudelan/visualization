''''''
import pdb

from data.raw_data import get_raw_data
from data.stats import get_stats
from data.growth import get_weekly_growth
from data.cumulative_respiration import get_weekly_respiration
from data.helpers import *

def get_carbon_efficiency(treatment):

    wknds = [0, 7, 14, 21]

    # raw data
    raw_mbc = get_raw_data('MBC')[treatment]
    raw_mbc = raw_mbc.loc[wknds]  # start-finish of first 3 weeks

    # get stats
    mbc_stats = get_stats(raw_mbc)
    mbc_means = mbc_stats.means
    mbc_errors = mbc_stats.stde

    # weekly change
    weekly_mbc_change = mbc_means.diff()
    weekly_mbc_change = weekly_mbc_change.shift(-1).drop(21)

    # associated errors for weekly change
    errors_squared = mbc_errors**2
    add_errors = errors_squared.add(errors_squared.shift(1))
    square_root = add_errors**0.5
    error_mbc_change = square_root.shift(-1).drop(21)

    # weekly respiration stats
    weekly_respiration_stats = get_weekly_respiration(treatment)
    weekly_respiration = weekly_respiration_stats.means
    repiration_error = weekly_respiration_stats.stde

    # impose same index for MBC and Respiration data
    index = weekly_respiration.index
    weekly_mbc_change.index = index
    error_mbc_change.index = index

    # assimilation-to-consumption ratio (CUE)
    CUE = weekly_mbc_change / (weekly_respiration + weekly_mbc_change)

    # error propogation
    growth_relative_err = error_mbc_change / weekly_mbc_change
    respiration_relative_err = repiration_error / weekly_respiration
    CUE_error = propagate_error(CUE, respiration_relative_err, growth_relative_err)

    return Stats(
        means=CUE,
        stde=CUE_error,
    )



