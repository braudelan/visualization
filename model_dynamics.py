import re
from pdb import set_trace
from typing import Dict, Any, Tuple

import pandas
import numpy
from numpy import exp
from matplotlib import pyplot
from lmfit import Model, Parameters
from lmfit.model import ModelResult
from matplotlib.ticker import MultipleLocator, NullLocator

from raw_data import get_setup_arguments
from raw_data import get_raw_data
from stats import get_stats
from helpers import  Constants
from model_functions import respiration_rate, microbial_carbon


# constants
SOILS = Constants.soils
COLORS = Constants.colors
MARKERS = Constants.markers

# plotting parameters
ORG_color, MIN_color, UNC_color = COLORS
ORG_marker, MIN_marker, UNC_marker = MARKERS
major_locator = MultipleLocator(7)  # major ticks locations
minor_locator = MultipleLocator(1)  # minor ticks locations

# which data sets to load
setup_arguments = get_setup_arguments()
data_set_name = setup_arguments.sets[0]

# get data set
raw_data = get_raw_data(data_set_name)
stats = get_stats(raw_data)
data_set = stats.MRE - stats.control # subtract control values

DAYS_TO_FIT = data_set.index.values[1:]

def delay_coefficient(t, delay):
    coefficient = numpy.zeros(len(t))
    coefficient[numpy.where(t > delay)] = 1

    return coefficient

def fit_model(model_function, data):

    ''' setup a model and calculate fit.'''

    # define main independent time variable
    t = DAYS_TO_FIT

    # define additional independent variables
    # c1 = delay_coefficient(t, 7)
    # c2 = delay_coefficient(t, 14)

    # setup the model
    model = Model(model_function, independent_vars=('t', ))

    # setup parameters
    parameters = Parameters()
    param_names = model.param_names
    initial_values = {
                      'a': 400,
                      'b': 2000,
                      'k': 0.3,
                      'k_a': 0.3,
                      'k_b': 0.4,
                      }
    for name in param_names:
        parameters.add(name, value=initial_values[name])

    results = {}
    for soil in SOILS:
        # dependent variable
        y = data[soil].loc[DAYS_TO_FIT[0]:DAYS_TO_FIT[-1]].values

        # fit model to data
        result = model.fit(y, parameters, t=t, nan_policy='omit')

        results[soil] = result

    return results


def plot_model(model_function, data, data_SD=None):

    # dictionary of fit results for the 3 soils (soil names as keys)
    fit_results = fit_model(model_function,data)

    # x values for measured and fitted points
    x_measured = DAYS_TO_FIT
    x_fit_curve = numpy.arange(DAYS_TO_FIT[0], DAYS_TO_FIT[-1], 1 / 24) # 24 time points for each day in time_range

    # delay coefficients for model function
    c1 = delay_coefficient(x_fit_curve, 7)
    c2 = delay_coefficient(x_fit_curve, 14)

    # text for plot
    font_setup = {'size': 20,
                 }
    fit_function_text = r'$\mathit{model\/function:}$' + '\n' + r'$\mathit{a\ast[\exp^{-k\ast\left(time - 0.5\right)} - \exp^{-k\ast\left(time + 0.5\right)}]}$'
    x_label = r'$day\ of\ incubation$'
    y_label = r'$MRE\ -\ control\  \slash$' + '\n' + r'$mg\ CO_{2}-C\ \ast\ kg\ soil^{-1}\ \ast\ day^{-1}$'
    figure_title ='respiration rate with fit curves'

    # figure
    figure = pyplot.figure(figsize=(25,15))
    figure.suptitle(figure_title, fontsize=28)
    figure.set_tight_layout(tight={'pad': 10})

    # axes setup
    axes = figure.add_subplot(111)
    # ticks
    axes.xaxis.set_major_locator(major_locator)
    axes.xaxis.set_minor_locator(minor_locator)
    axes.tick_params(which='major', length=5, width=1.5, labelsize='large')
    axes.tick_params(which='minor', length=4, width=1)
    # model function text
    axes.text(0.7, 0.6, fit_function_text, transform=axes.transAxes, fontdict=font_setup)
    # labels
    axes.set_xlabel(x_label, labelpad=30, fontsize=20)
    axes.set_ylabel(y_label, labelpad=150, va='center', rotation=60, fontsize=20)

    indent = 0
    # plot measured and fitted points for each soil
    for soil in SOILS:

        # text
        # parameters_text = soil + '\n a: ' + str(a) + '\n k: ' + str(k)

        fit_color = (
                                   ORG_color if (soil == 'ORG') else
                                   MIN_color if (soil == 'MIN') else
                                   UNC_color
                                  )

        measured_color = (
                          ORG_color if (soil == 'ORG') else
                          MIN_color if (soil == 'MIN') else
                          UNC_color
                         )


        measured_marker = (
                          ORG_marker if (soil == 'ORG') else
                          MIN_marker if (soil == 'MIN') else
                          UNC_marker
                         )


        data_kws = {
                    'color': measured_color,
                    'marker': measured_marker,
                    'markersize': 12,
                   }

        fit_kws = {
                   'color': fit_color,
                   'linewidth': 3,
                  }

        fit_result = fit_results[soil]
        model = fit_result.model
        params = fit_result.params

        y_fit = model.eval(t = x_fit_curve, params=params)
        # a = fit_result.best_values['a']
        # k = fit_result.best_values['k']
        #
        fit_result.plot_fit(ax=axes, numpoints=480, data_kws=data_kws, fit_kws=fit_kws)
        dely = fit_result.eval_uncertainty(sigma=1, t=x_fit_curve)
        axes.fill_between(x_fit_curve, y_fit - dely, y_fit + dely, color="#ABABAB")
        # axes.plot(x_measured, y_measured, 's',color=measured_color, marker=measured_marker, markersize=12, label=soil+' measured')
        # axes.plot(x_fit_curve , y_fit, color=fit_color, linewidth=3,
        #                                                         linestyle=(1,(3,2,3,2)), label=soil+' fit curve')
        # # fit result text
        # axes.text(0.06, 0.8 - indent, parameters_text, transform=axes.transAxes, fontsize=15)

        indent += 0.13

    legend = axes.legend(loc='best', prop={'size': 20})

    return figure


if __name__ == '__main__':
    function = respiration_rate if data_set_name == 'RESP' else microbial_carbon
    results = fit_model(function, data_set)
    fit_figure = plot_model(function, data_set)
    fit_figure.savefig('./modeling/%s.png' %data_set_name)
    pyplot.clf()