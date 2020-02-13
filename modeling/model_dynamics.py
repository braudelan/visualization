import pandas

from lmfit import Model, Parameters

from data.raw_data import get_raw_data, baseline_normalize
from modeling.model_functions import biomass_carbon


def fit_model(model_function, t, y, drop_days=None):

    ''' setup a model and calculate fit.'''

    # independent time variable
    if drop_days:
        days = list(set(t) - set(drop_days))
    else:
        days = t

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
        'k_a': 1,
        'k_b': 0.6,
        'k_g': 30,
        'k_d': 0.4,
    }
    for name in param_names:
        parameters.add(name, value=initial_values[name])


    # fit model to data
    fit_result = model.fit(y, parameters, t=t,  nan_policy='omit')

    # refit the model with fixed variable
    # FIXED_VAR = 'k_g'
    # parameters = fit_result.params
    # parameters[FIXED_VAR].set(vary=False)
    # fit_result.fit(data=y, t=t, params=parameters, weights=soil_stdv, nan_policy='omit')

    return fit_result


def drop_days(time_variable, days_to_drop=None):

    if type(days_to_drop) == list:
        time_variable = list(set(time_variable) - set(drop_days)) \
            if drop_days else time_variable

    else:
        mask = [days_to_drop(x) for x in time_variable]
        time_variable = time_variable[mask]

    return time_variable


def fit(data, model_function, days_to_drop=None):
    '''
    initialize model and fit data.

    parameter:
    data (DataFrame)
    must contain a 'mean' column with y values to fit and an 'error' column
    with weights.
    '''

    # independent variable
    t = data.index.values


    # drop irrelevant days
    t = drop_days(t, days_to_drop) if days_to_drop else t
    data = data.loc[t]

    # dependent variable abd weights
    y = data['mean'].values
    error = data['error'].values

    # intialize model and perform fit
    fit = model.fit(y, t=t, weights=error, nan_policy='omit')

    return fit


if __name__ == '__main__':

    data_set_name = 'MBC'
    soil = 'MIN'
    raw = get_raw_data(data_set_name)
    raw = baseline_normalize(raw)[soil]
    mean = raw.T.mean()
    sem = raw.T.sem()
    mean[0] = 0
    sem[0] = 0
    mean.name = 'mean'
    sem.name = 'error'
    data = pandas.concat([mean, sem], axis=1)

    data.dropna(how='any', inplace=True)
    fit = fit(data, biomass_carbon)
