import pdb
import numpy
from numpy import ma
from matplotlib import pyplot
from matplotlib.ticker import MultipleLocator, NullLocator
from matplotlib.axes import Axes
from lmfit import Model, Parameters
from lmfit.model import ModelResult

from raw_data import get_setup_arguments
from raw_data import get_raw_data
from stats import get_stats, normalize_to_control
from helpers import  Constants
from model_functions import respiration_rate, biomass_carbon


# constants
SOILS = Constants.groups
COLORS = Constants.colors
MARKERS = Constants.markers
OUTPUT_FOLDER = Constants.output_folder

# plotting parameters
major_locator = MultipleLocator(7)  # major ticks locations
minor_locator = MultipleLocator(1)  # minor ticks locations

# which data set to load
setup_arguments = get_setup_arguments()
data_set_name = setup_arguments.sets[0]

# get data set
raw_data = get_raw_data(data_set_name)
norm_raw = normalize_to_control(raw_data)
stats = get_stats(norm_raw, 't')
data_set = stats.means
data_stdv = stats.stdv

DAYS_TO_FIT = data_set.index.values[1:]


def get_chi_square(fit_result):

    def exclude_nans(array):
        where_nan = numpy.isnan(array)  # boolean array, True where NAN
        has_nan = numpy.any(where_nan)

        if has_nan:
            excluded = ma.masked_array(array, where_nan)

            return excluded

        else:
            return array

    def no_zeros(array):
        for i in array:
            if i == 0:
                i += 1 * 10 ** -6

    y_fit = exclude_nans(fit_result.best_fit)
    y_measured = exclude_nans(fit_result.data)
    no_zeros(y_fit)
    no_zeros(y_measured)

    residuals = y_measured - y_fit
    sqaured = residuals ** 2
    normalized = sqaured / y_fit
    normalized_chi_sqaure = normalized.sum()

    return normalized_chi_sqaure


def fit_model(model_function, soil_data, soil_stdv):

    ''' setup a model and calculate fit.'''

    # independent time variable
    t = DAYS_TO_FIT
    # dependent variable (measured data)
    y = soil_data.loc[DAYS_TO_FIT].values

    # setup the model
    model = Model(model_function, independent_vars='t')
    # model.set_param_hint('a_g', max=3000)

    # setup parameters
    parameters = Parameters()
    param_names = model.param_names
    initial_values = {
        'a': 120,
        'a_g': 3000,
        'a_d': 3000,
        'k': 0.3,
        'k_g': 30,
        'k_d': 0.4,
    }
    for name in param_names:
        parameters.add(name, value=initial_values[name])


    # fit model to data
    fit_result = model.fit(y, parameters, t=t, weights=soil_stdv.loc[DAYS_TO_FIT], nan_policy='omit')

    # refit the model with fixed variable
    # FIXED_VAR = 'k_g'
    # parameters = fit_result.params
    # parameters[FIXED_VAR].set(vary=False)
    # fit_result.fit(data=y, t=t, params=parameters, weights=soil_stdv, nan_policy='omit')

    return fit_result


def plot_model(axes: Axes, soil, fit_result: ModelResult):

    # position chi square text
    text_height = 0.02
    x_location = 0.7
    y_ORG = 0.7
    y_MIN = y_ORG - text_height
    y_UNC = y_MIN - text_height
    locations = ((x_location, y_ORG), (x_location, y_MIN), (x_location, y_UNC))
    CHI_SQUARE_LOCATION = dict(zip(SOILS, locations))

    data_kws = {
        'color': COLORS[soil],
        'marker': MARKERS[soil],
        'markersize': 12,
    }

    fit_kws = {
        'color': COLORS[soil],
        'linewidth': 3,
    }

    model = fit_result.model
    parameters = fit_result.params

    X = numpy.arange(DAYS_TO_FIT[0], DAYS_TO_FIT[-1], 1 / 24)  # 24 time points for each day in time_range
    y_fit = model.eval(t=X, params=parameters)

    lines = fit_result.plot_fit(ax=axes, numpoints=480, data_kws=data_kws, fit_kws=fit_kws)

    dely = fit_result.eval_uncertainty(sigma=1, t=X)
    axes.fill_between(X, y_fit - dely, y_fit + dely, color="#ABABAB")

    reduced_chi_square = get_chi_square(fit_result)
    x = CHI_SQUARE_LOCATION[soil][0]
    y = CHI_SQUARE_LOCATION[soil][1]
    axes.text(x, y, str(reduced_chi_square), transform=axes.transAxes)


def make_figure_and_axes():
    # text for plot
    font_setup = {'size': 20,
                 }
    # fit_function_text = r'$\mathit{model\/function:}$' + '\n' + r'$\mathit{a\ast[\exp^{-k\ast\left(time - 0.5\right)} - \exp^{-k\ast\left(time + 0.5\right)}]}$'
    x_label = r'$day\ of\ incubation$'
    y_label = r'$MRE\ -\ control\  \slash$' + '\n' + r'$mg\ CO_{2}-C\ \ast\ kg\ soil^{-1}\ \ast\ day^{-1}$'
    figure_title = 'respiration rate with fit curves'

    # figure
    figure = pyplot.figure(figsize=(25,15))
    figure.set_tight_layout(tight={'pad': 10})
    # figure.suptitle(figure_title, fontsize=28)

    # axes setup
    axes: Axes = figure.add_subplot(111)

    axes.xaxis.set_major_locator(major_locator)
    axes.xaxis.set_minor_locator(minor_locator)
    axes.tick_params(which='major', length=5, width=1.5, labelsize='large')
    axes.tick_params(which='minor', length=4, width=1)

    # labels
    axes.set_xlabel(x_label, labelpad=30, fontsize=40)
    axes.set_ylabel(y_label, labelpad=150, va='center', rotation=60, fontsize=20)

    # legend = axes.legend(loc='best', prop={'size': 20})

    return figure, axes


if __name__ == '__main__':
    function = respiration_rate if data_set_name == 'RESP' else biomass_carbon
    figure, axes = make_figure_and_axes()
    for soil in SOILS:
        data = data_set[soil]
        stdv = data_stdv[soil]
        fit_result = fit_model(function, data, stdv)
        plot_model(axes, soil, fit_result)

    handles = axes.get_lines()

    labels = SOILS + SOILS
    legend = axes.legend(handles=handles, labels=labels, loc='best', prop={'size': 20})
    figure.savefig('%s/%s_model_weighted' %(OUTPUT_FOLDER, data_set_name))

    # for soil in SOILS:
    #     result = fit_model(function, data_set[soil], data_SD[soil])
    #     chi_square = get_chi_square(result)
    #
    #     print(soil + ':' + str(chi_square
