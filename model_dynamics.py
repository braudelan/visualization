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

fit_results = {}
def fit_model(data):

    # define main independent time variable
    t = DAYS_TO_FIT

    # define additional independent variables
    c1 = delay_coefficient(t, 7)
    c2 = delay_coefficient(t, 14)

    # helper function
    def first_order_rate(z, a, k):
        return a * (exp(-k * (z - 0.5)) - exp(-k * (z + 0.5)))

    # model function
    def respiration_rate(x, a, k, c1, c2):
        return first_order_rate(x, a, k) + c1 * first_order_rate(x-7, a, k) + c2 * first_order_rate(x-14, a, k)

    # setup the model
    rate_model = Model(respiration_rate, independent_vars=('x', 'c1', 'c2'))

    # setup parameters
    parameters = rate_model.make_params()
    parameters.add(name='a', value=185)
    parameters.add(name='k', value=0.2)

    for soil in SOILS:

        y = data[soil].loc[DAYS_TO_FIT[0]:DAYS_TO_FIT[-1]].values

        # fit model to data
        result = rate_model.fit(y, parameters, x=t, c1=c1, c2=c2)

        fit_results[soil] = result

    return respiration_rate, fit_results


def plot_model(data, data_SD=None):

    # model results
    fit_function = fit_model(data)[0]
    model_results = fit_model(data)[1]

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

    # setup figure and axes
    figure = pyplot.figure(figsize=(25,15))
    figure.suptitle(figure_title, fontsize=28)
    axes = figure.add_subplot(111)
    axes.xaxis.set_major_locator(major_locator)
    axes.xaxis.set_minor_locator(minor_locator)
    axes.text(0.7, 0.6, fit_function_text, transform=axes.transAxes, fontdict=font_setup)
    axes.set_xlabel(x_label, labelpad=30, fontsize=20)
    axes.set_ylabel(y_label, labelpad=150, va='center', rotation=60, fontsize=20)

    indent = 0
    # plot measured and fitted points for each soil
    for soil in SOILS:

        y_measured = data[soil].loc[data.index.isin(DAYS_TO_FIT)]
        fit_result = model_results[soil]
        a = fit_result.best_values['a']
        k = fit_result.best_values['k']

        # text for best fit values and fit statistics
        chi_square = fit_result.chisqr
        chi_square_text = r'$\chi ^2:$' + str(chi_square)
        fit_report = fit_result.fit_report()
        parameters_best_fit = re.findall(re.compile('(?:\s+)\d+\.\d+\s+\+/\-\s+\d+\.\d+'), fit_report)
        a_value = parameters_best_fit[0]
        k_value = parameters_best_fit[1]

        parameters_text = soil + '\n' + chi_square_text + '\n a: ' + a_value + '\n k: ' + k_value

        fit_curve_color = color = (
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

        axes.plot(x_measured, y_measured, 's',color=measured_color, marker=measured_marker, markersize=12, label=soil+' measured')
        axes.plot(x_fit_curve , fit_function(x_fit_curve, a, k, c1, c2), color=fit_curve_color, linewidth=3,
                                                                linestyle=(1,(3,2,3,2)), label=soil+' fit curve')
        axes.text(-0.45, 0.9 - indent, parameters_text, transform=axes.transAxes, fontsize=18)

        indent += 0.13

    legend = axes.legend(loc='best', prop={'size': 20})

    return figure


if __name__ == '__main__':
    results = fit_model(data_set)
    fit_figure = plot_model(data_set)
    fit_figure.savefig('/home/elan/Desktop/test_model_dynamics.png', bbox_inches='tight')
    pyplot.clf()