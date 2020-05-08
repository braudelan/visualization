from scipy.optimize import curve_fit
from matplotlib import pyplot

from data.raw_data import *
from data.stats import *
from modeling.model_functions import *



INITIAIL_PARAMS = [300, 1.5, 0.4]

# microbial growth and decay
def growth_decay(t, A, ka, kb):

    # 1st order reaction product
    def conc(time, max, rate_constant):
        return max * (1 - exp(-rate_constant * time))

    return conc(t, A, ka) - conc(t, A, kb)


def get_the_data(
        data_name,
        treatment,
        days_to_fit,
        soil,
        normalize
):

    raw_data = get_raw_data(data_name).loc[days_to_fit]
    raw_data = normalize(raw_data) if normalize else raw_data
    stats = get_stats(raw_data) if normalize else get_stats(raw_data, treatment)

    means = stats.means[soil].dropna()
    stnd_err = stats.stde[soil].dropna()

    return Stats(
        means=means,
        stde=stnd_err
    )

    # group by sampling event
    groupby_sampling = raw.groupby(raw.index)

    # means
    means = groupby_sampling.mean()
    stdev = groupby_sampling.std()

    return Stats(
        means=means,
        stde=stdev
    )


def get_best_fit_params(means, stdv, model_function):
    '''
    find best fit parameters for dynamics data.

    :param means: Series
    index is sampling events.

    :param stdv: Series

    :param model_function:
    the function to preform curve fit for.

    :return: fit_params
    list of best fit parameters.
    '''


    X = means.index.values
    y_observed = means.values
    stnd_dev = stdv.values

    fit_params, covarriance = curve_fit(model_function, X, y_observed,
                                        sigma=stnd_dev,
                                        p0=INITIAIL_PARAMS,
                                        absolute_sigma=True)

    return  fit_params, covarriance


def get_weekly_fit(means, stdev, model_function):
    '''
    fit weekly data to a given model function

    :param means: Series
    mean value for the entire time period.

    :param stdev:Series

    :param model_function:
    the function to be fitted.

    :return: fit_result: dict
    '''
    week_bounds = {
        '1': (0, 7),
        '2': (7, 14),
        '3': (14, 21),
    }

    weekly_means = {}
    for week, bounds in week_bounds.items():
        start = week_bounds[week][0]
        end = week_bounds[week][1]
        week_means = means.loc[start:end]
        weekly_means[week] = week_means

    for week, means in weekly_means.items():



def plot_fit(means, fit_params, title, model_function):
    '''
    plot fitted curve alongside the measured data points.

    :param means:
    :param fit_params: list
    len(list) = 2
    :param title:
    :param model_function:
    :return:
    '''
    x_measured = means.index.values
    y_measured = means.values

    first_measured_x = x_measured[0]
    last_measured_x = x_measured[-1]

    x_fit = numpy.arange(
        first_measured_x,
        last_measured_x,
        0.1
    )
    p0, p1, p2 = fit_params
    y_fit = model_function(x_fit, p0, p1, p2)

    pyplot.plot(x_measured, y_measured, 'bo',label='measured')
    pyplot.plot(x_fit, y_fit, 'r-', label='fitted curve')
    pyplot.xlabel(r'$days$')
    pyplot.ylabel(r'$mg\ \ast\ kg^{-1}$')
    pyplot.title(title)

#todo return an axes so that more data can be plotted on the same plot

if __name__ == '__main__':

    MODEL_FUNCTION = growth_decay
    normalize_by = control_normalize
    name = 'MBC'
    treatment = 't'
    soils = ['ORG', 'MIN', 'UNC']
    soil = 'ORG'
    days = [0, 1, 3, 7,]


    data = get_the_data(name, treatment, soil, days, normalize_by)
    fit_params = get_best_fit_params(data, MODEL_FUNCTION)

    plot_fit(data,fit_params, soil, MODEL_FUNCTION)

    # fit = get_best_fit_params(data, MODEL_FUNCTION)

# curve fitting
# growth_decay_model = Model(model_function)
# params = growth_decay_model.make_params(a=3000, k_a=20, k_b=0.01)
#
# result = growth_decay_model.fit(y_observed, params, t=X, )
