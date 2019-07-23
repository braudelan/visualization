import numpy
from matplotlib import pyplot
from matplotlib.ticker import MultipleLocator, NullLocator
from matplotlib.axes import Axes
from lmfit import Model, Parameters
from lmfit.model import ModelResult

from raw_data import get_setup_arguments
from raw_data import get_raw_data
from stats import get_stats
from helpers import  Constants
from model_functions import respiration_rate, biomass_carbon


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
# data_set = data_set.loc[data_set.index != 8]

DAYS_TO_FIT = data_set.index.values

def delay_coefficient(t, delay):
    coefficient = numpy.zeros(len(t))
    coefficient[numpy.where(t > delay)] = 1

    return coefficient

def assign_property(label, choices):
    '''assign plotting parameter based on soil name and choices'''
    property = choices[label]
    return property

def refit_model(fit_result, soil, variable_name):

    parameters = fit_result.params
    initial_params = fit_result.init_params
    parameters[variable_name].set(vary=False)
    fit_result.fit(data=fit_result.data, params=parameters, nan_policy='omit')
    print(soil + ':\'' + fit_result.fit_report())


def plot_model(ax, fit_result, data_kws, fit_kws):

    model = fit_result.model
    parameters = fit_result.params

    # x values for measured and fitted points
    X = numpy.arange(DAYS_TO_FIT[0], DAYS_TO_FIT[-1], 1 / 24)  # 24 time points for each day in time_range
    y_fit = model.eval(t=X, params=parameters)

    fit_result.plot_fit(ax=ax, numpoints=480, data_kws=data_kws, fit_kws=fit_kws)

    # dely = fit_result.eval_uncertainty(sigma=1, t=X)
    # ax.fill_between(X, y_fit - dely, y_fit + dely, color="#ABABAB")

def fit_model(model_function, data):

    ''' setup a model and calculate fit.'''

    # independent time variable
    t = DAYS_TO_FIT
    # dependent variable (measured data)
    y = data.loc[DAYS_TO_FIT[0]:DAYS_TO_FIT[-1]].values

    # setup the model
    model = Model(model_function, independent_vars='t')

    # setup parameters
    parameters = Parameters()
    param_names = model.param_names
    initial_values = {
        'a_g': 400,
        'a_d': 2000,
        'k': 0.3,
        'k_g': 0.3,
        'k_d': 0.4,
    }
    for name in param_names:
        parameters.add(name, value=initial_values[name])

    # fit model to data
    result = model.fit(y, parameters, t=t, nan_policy='omit')

    return result

def make_figure(model_function, data, data_SD=None):

    # text for plot
    font_setup = {'size': 20,
                 }
    fit_function_text = r'$\mathit{model\/function:}$' + '\n' + r'$\mathit{a\ast[\exp^{-k\ast\left(time - 0.5\right)} - \exp^{-k\ast\left(time + 0.5\right)}]}$'
    x_label = r'$day\ of\ incubation$'
    y_label = r'$MRE\ -\ control\  \slash$' + '\n' + r'$mg\ CO_{2}-C\ \ast\ kg\ soil^{-1}\ \ast\ day^{-1}$'
    figure_title = 'respiration rate with fit curves'

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

    for soil in SOILS:

        # plotting parameters
        fit_color = assign_property(soil, COLORS)
        data_color = assign_property(soil, COLORS)
        data_marker = assign_property(soil, MARKERS)

        data_kws = {
            'color': data_color,
            'marker': data_marker,
            'markersize': 12,
        }

        fit_kws = {
            'color': fit_color,
            'linewidth': 3,
        }

        fit_result = fit_model(model_function, data[soil])
        plot_model(axes, fit_result, data_kws, fit_kws)


    legend = axes.legend(loc='best', prop={'size': 20})

    return figure


if __name__ == '__main__':

    function = respiration_rate if data_set_name == 'RESP' else biomass_carbon
    # figure = make_figure(function, data_set)
    # figure.savefig('./modeling/%s' % data_set_name)

    for soil in SOILS:
        data = data_set[soil]
        fit_result = fit_model(function, data)
        refit_model(fit_result,data, soil)