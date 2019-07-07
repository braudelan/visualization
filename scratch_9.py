
from numpy import exp
from lmfit import Model

from raw_data import get_setup_arguments
from raw_data import get_raw_data
from stats import get_stats
from switch_on_off import delay_factor


# setup
setup_arguments = get_setup_arguments()
data_set_name = setup_arguments.sets[0]
raw_data = get_raw_data(data_set_name)
stats = get_stats(raw_data)

# data
data = stats.difference['ORG']

# # model function
# def rate(x, a, k):
#
#     def rate_unit(x):
#         return a * ( exp(-k*(x-0.5)) - exp(-k*(x+0.5)))
#
#     return rate_unit(x) + delay_factor(x,7) * rate_unit(x - 7) + delay_factor(x,14) * rate_unit(x - 14)
#
# # setup the model
# rate_model = Model(rate)
#
# # setup parameters
# parameters = rate_model.make_params()
# parameters.add('a', value=200)
# parameters.add('k', value=0.5)
# # parameters.add('c1', expr='0 if t < 7 else 1')
# # parameters.add('c2', expr='0 if t < 14 else 1')
#
# # independent variable and measuerd data points to fit
# x = data.index.values
# y = data.values
#
# # fit model to data
# result = rate_model.fit(y, parameters, x=x)
#
#
