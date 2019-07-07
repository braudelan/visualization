import re

import pandas
import numpy
from numpy import exp
from matplotlib import pyplot
from lmfit import Model, Parameters
from matplotlib.ticker import MultipleLocator, NullLocator

from raw_data import get_setup_arguments
from raw_data import get_raw_data
from stats import get_stats
from helpers import  Constants


# SOILS = Constants.soils
# COLORS = Constants.colors
# MARKERS = Constants.markers
#
# # plotting parameters
# ORG_color, MIN_color, UNC_color = COLORS
# ORG_marker, MIN_marker, UNC_marker = MARKERS
# major_locator = MultipleLocator(1)  # major ticks locations
# minor_locator = MultipleLocator(24)  # minor ticks locations

# which data sets to load
setup_arguments = get_setup_arguments()
data_set_name = setup_arguments.sets[0]

# get data set
raw_data = get_raw_data(data_set_name)
stats = get_stats(raw_data)
data = stats.MRE - stats.control # subtract control values

# DAYS_TO_FIT = data.index

# define main independent time variable and dependent variable
t = data.index[0:7].values
y = data['ORG'].loc[0:14].values

# define additional independent variables
c1 = numpy.zeros(len(t))
c2 = numpy.zeros(len(t))
c1[numpy.where(t>7)] = 1
c2[numpy.where(t>14)] = 1

# helper function
def rate_unit(z, a, k):
    return a * (exp(-k * (z - 0.5)) - exp(-k * (z + 0.5)))

# model function
def rate(x, a, k, c1, c2):
    return rate_unit(x, a, k) + c1 * rate_unit(x-7, a, k) + c2 * rate_unit(x-14, a, k)

# setup the model
rate_model = Model(rate, independent_vars=('x', 'c1', 'c2'))

# setup parameters
parameters = rate_model.make_params(a=200, k=0.5)

# fit model to data
fit_result = rate_model.fit(y, parameters, x=t, c1=c1, c2=c2)
#
# # model function
# def rate(x, a, k, c1, c2):
#     def rate_unit(x):
#         return a * ( exp(-k*(x-0.5)) - exp(-k*(x+0.5)))
#     return rate_unit(x) + c1 * rate_unit(x - 7) + c2 * rate_unit(x - 14)
#
#
# # define independent and dependent variables
# t = data.index.values
# y = data['ORG'].values
#
# # setup the model
# rate_model = Model(rate)
#
# # setup parameters
# parameters = rate_model.make_params()
# parameters._asteval.symtable['t'] = t
# parameters.add('a', value=200)
# parameters.add('k', value=0.5)
# parameters.add('c1', expr='1*(t>=7)')
# parameters.add('c2', expr='1*(t>=14)')
#
# # fit model to data
# result = rate_model.fit(y, parameters, x=t)
#
# # fit model to data
# def fit_model(data):
#
#     data = data.loc[data.index.isin(DAYS_TO_FIT)]
#
#     model_results = {}
#     for soil in SOILS:
#
#         soil_data = data[soil]
#
#         t = DAYS_TO_FIT.values
#         y = soil_data.values
#
#         result = rate_model.fit(y, parameters, x=t)
#
#         model_results[soil] = result
#
#     return rate, model_results
#
#
# def plot_model(data, data_SD=None):
#
#     # model results
#     fit_function = fit_model(data)[0]
#     model_results = fit_model(data)[1]
#
#     # x values for measured and fitted points
#     x_measured = [x-1 for x in DAYS_TO_FIT]
#     x_fit_curve = numpy.arange(x_measured[0], x_measured[-1], 1 / 24) # 24 time points for each day in time_range
#
#     # text for plot
#     font_setup = {'size': 27,
#                  }
#     fit_function_text = r'$ a\ast\exp\ ^{-kt}$'
#     x_label = r'$day\ of\ incubation$'
#     y_label = r'$MRE\ -\ control\  \slash$' + '\n' + r'$mg\ CO_{2}-C\ \ast\ kg\ soil^{-1}\ \ast\ day^{-1}$'
#     figure_title ='respiration rate model, 1st week'
#
#     # setup figure and axes
#     figure = pyplot.figure(figsize=(25,15))
#     figure.suptitle(figure_title, fontsize=28)
#     axes = figure.add_subplot(111)
#     axes.xaxis.set_major_locator(major_locator)
#     axes.xaxis.set_minor_locator(minor_locator)
#     axes.text(0.5, 0.6, fit_function_text, transform=axes.transAxes, fontdict=font_setup)
#     axes.set_xlabel(x_label, labelpad=30, fontsize=23)
#     axes.set_ylabel(y_label, labelpad=150, va='center', rotation=60, fontsize=23)
#
#     indent = 0
#     # plot measured and fitted points for each soil
#     for soil in SOILS:
#
#         y_measured = data[soil].loc[data.index.isin(DAYS_TO_FIT)]
#         fit_result = model_results[soil]
#         a = fit_result.best_values['a']
#         k = fit_result.best_values['k']
#
#         # text for best fit values and fit statistics
#         chi_square = fit_result.chisqr
#         chi_square_text = r'$\chi ^2:$' + str(chi_square)
#         fit_report = fit_result.fit_report()
#         parameters_best_fit = re.findall(re.compile('(?:\s+)\d+\.\d+\s+\+/\-\s+\d+\.\d+'), fit_report)
#         a_value = parameters_best_fit[0]
#         k_value = parameters_best_fit[1]
#
#         parameters_text = soil + '\n' + chi_square_text + '\n a: ' + a_value + '\n k: ' + k_value
#
#         fit_curve_color = color = (
#                                    '0.4' if (soil == 'ORG') else
#                                    '0.6' if (soil == 'MIN') else
#                                    '0.8'
#                                   )
#
#         measured_color = (
#                           ORG_color if (soil == 'ORG') else
#                           MIN_color if (soil == 'MIN') else
#                           UNC_color
#                          )
#
#         measured_marker = (
#                           ORG_marker if (soil == 'ORG') else
#                           MIN_marker if (soil == 'MIN') else
#                           UNC_marker
#                          )
#
#         axes.plot(x_measured, y_measured, 's', marker=measured_marker, markersize=12, label=soil+' measured')
#         axes.plot(x_fit_curve , fit_function(x_fit_curve, a, k), color=fit_curve_color, linewidth=3,
#                                                                 linestyle=(1,(3,2,3,2)), label=soil+' fit curve')
#         axes.text(-0.45, 0.9 - indent, parameters_text, transform=axes.transAxes, fontsize=18)
#
#         indent += 0.13
#
#     axes.legend()
#
#     return figure
#
#
# if __name__ == '__main__':
#     results = fit_model(data_set)