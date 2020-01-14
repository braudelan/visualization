from data_handling.raw_data import get_raw_data
from growth import get_mean_weekly_growth
from cumulative_respiration import get_weekly_respiration
from helpers import *


treatment = 't'
raw_mbc = get_raw_data('MBC')[treatment]

# means and stnd errors
weekly_growth_stats = get_mean_weekly_growth(raw_mbc)
weekly_respiration_stats = get_weekly_respiration(treatment)

weekly_growth = weekly_growth_stats.means
weekly_respiration = weekly_respiration_stats.means
new_columns = weekly_respiration.columns
weekly_growth = weekly_growth.reindex(columns=new_columns)
weekly_growth = weekly_growth.drop(4)

# weekly respiration-to-grwoth ratio
respiration_to_growth = weekly_respiration / weekly_growth

# error propogation
growth_error = weekly_growth_stats.stde
growth_error = growth_error.reindex(columns=new_columns)
growth_error = growth_error.drop(4)
growth_relative_err = growth_error / weekly_growth
repiration_error = weekly_respiration_stats.stde
respiration_relative_err = repiration_error / weekly_respiration

error_of_ratio = propagate_error(respiration_to_growth, respiration_relative_err, growth_relative_err)

# plot
ratio = respiration_to_growth
ratio.loc[2, 'UNC'] = None
errors = error_of_ratio
errors.loc[2, 'UNC'] = None

labels = [r'$1^{st}$', r'$2^{nd}$', r'$3^{rd}$', r'$4^{th}$']
x_location = numpy.arange(1,5)



