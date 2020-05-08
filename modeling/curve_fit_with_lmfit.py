import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model
from lmfit.model import ModelResult

from data.raw_data import get_raw_data
import constants as constants


LTTs = constants.LONG_TERM_TREATMENTS

# constant parameters for respiration data
WEEKS = ['1', '2', '3']
BOUNDS = [(0, 7), (7, 14), (14, 21)]
WEEKLY_BOUNDS = dict(zip(WEEKS, BOUNDS))
DROP = [[0.17], [7, 7.17], []]
INDICES_TO_DROP = dict(zip(WEEKS, DROP))

# initial guess for parameters
INIT_PARAMS = {'A': 1000, 'k': 1}


# ----------------------------------------------- getting the data and some data wrangling---------------------------------------------------------
def get_raw_ltt(
        data_set_name,
        ltt,
    ):

    '''
    get treated samples raw data, for a given LTT.

    :param data_set_name:
    :param ltt:
    :return:
    '''


    raw_data = get_raw_data(data_set_name)['t'] # treated samples
    raw_ltt = raw_data[ltt]

    # stack and drop 'replicate' level
    stacked = raw_ltt.stack()
    droped_n_stacked = stacked.droplevel('replicate')
    raw_ltt = droped_n_stacked

    raw_ltt.name = data_set_name

    return raw_ltt


def combine_raw_data(
        data_set_name,
):
    '''
    combine raw_data from all LTTs.

    :param data_set_name: str
    which data set to use.

    :param treatment: str
    't' for treated samples, 'c' for control samples

    :return: combined_raw_data: Series
    index is sampling event.
    '''

    def drop_outliers(data, drop_index):
        is_respiration_data = data.name == 'Resp'


        if is_respiration_data:
            data.drop(drop_index, inplace=True)

    # get raw data
    combined_raw = get_raw_data(data_set_name)['t']

    # stack and drop 'soil' and 'replicate' levels
    columns_levels = combined_raw.columns.names
    combined_raw = combined_raw.stack(columns_levels).droplevel(columns_levels)

    # name raw data
    combined_raw.name = data_set_name

    # # drop outlying data
    # indices_to_drop = [0.17, 7, 7.17]
    # drop_outliers(combined_raw, indices_to_drop)

    # # insert initial control values for respiration data of treated samples
    # if data_set_name == 'Resp' and treatment == 't':
    #     # get data
    #     control_raw = get_raw_data(data_set_name)['c']
    #     # first sampling raw data
    #     first_row = control_raw.iloc[0]
    #     # drop all index levels
    #     first_row.reset_index(drop=True)
    #     # set all index labels to 0
    #     new_index = [0 for i in first_row.index]
    #     first_row.index = new_index
    #     # insert control first sampling data as the first value of treated samples data
    #     raw = first_row.append(raw)

    return combined_raw


def get_weekly_data(
        raw_data,
        weekly_bounds,
        drop=None,
):
    '''
    getting raw data for a given week.

    :param raw_data: Series
    raw data for the entire experiment period.

    :param weekly_bounds: dict
    keys are week numbers and values are tuples with the first
        and last sampling time of each week.

    :return: weekly_data: dict
    keys are week numbers. values are slices of raw data of each week.
        for any week number other than 1, original index is conformed to a
        standalone week index (i.e same as 1st week index).

    '''


    weekly_data = {}
    for week in weekly_bounds.keys():

        # slice weekly data
        start = weekly_bounds[week][0]
        end = weekly_bounds[week][1]
        week_data = raw_data.loc[start:end]

        # exclude data points that are not modeled
        if drop:
            week_data.drop(drop[week], inplace=True)

        # pdb.set_trace()
        # conform index to start from zero
        if week != '1':
            subtract_start = lambda x: x - start
            week_data = week_data.rename(index=subtract_start)
            # # old_index = week_data.index
            # new_index = [i - start for i in week_data.index]
            # week_data.index = new_index

        weekly_data[week] = week_data

    return weekly_data


# ----------------------------------------------- fitting the data  --------------------------------------------------------
def get_fit_result(
        data,
        init_params,
        model_function,
):
    '''
    find best fit parameters.

    :param data: DataFrame
    raw data. index values are sampling events.

    :param init_params: dict

    :param model_function
    function to fit data with.

    :return: result: ModelResult

    '''

    x = data.index.values
    y = data.values


    model = Model(model_function)
    for param, init_value in init_params.items():
        model.set_param_hint(param, value=init_value)
    params = model.make_params()

    result = model.fit(y, params, t=x)

    return result


def get_weekly_fit(
        weekly_data,
        init_params,
        model_function,
    ):
    '''
    fit weekly data to a given model function.

    :param raw_data:
    :param model_function:
    :return:
    '''

    weekly_fit = {}
    for week, data in weekly_data.items():

        fit_result = get_fit_result(data, init_params, model_function)
        weekly_fit[week] = fit_result

    return  weekly_fit


# ----------------------------------------------- plotting the measured data and the fitted function ----------------------------------------
def plot_one_week_fit(
        data,
        fit_result: ModelResult,
        figure_number=None,
):

    # model function
    model = fit_result.model

    # time points
    X = data.index.values

    # measured y data
    y = data.values

    # best fit y data
    from_zero = [x - X[0] for x in X]
    X_from_zero = np.linspace(from_zero[0], from_zero[-1], 100)
    best_fit_params = fit_result.params
    best_fit_y = model.eval(params=best_fit_params, t=X_from_zero)
    # pdb.set_trace()

    # new figure
    if figure_number:
        plt.figure(figure_number)

    # plot measured data
    plt.plot(X, y, 'bo')

    # plot best fit curve
    best_fit_X = np.linspace(X[0], X[-1], 100)
    plt.plot(best_fit_X, best_fit_y, 'r-', label='best fit')

    # uncertainty band
    best_fit = fit_result.best_fit
    n_sigma = 1
    error = fit_result.eval_uncertainty(sigma=n_sigma, t=X_from_zero)
    plt.fill_between(
        best_fit_X,
        best_fit_y - error,
        best_fit_y + error,
        color="#ABABAB",
        label=f'{n_sigma}$\sigma$ uncertainty band',
    )

    # plt.legend(loc='best')


def plot_weekly_fit(
        fit,
        data,
        weeks,
):
    '''
    plot data and fitted curve for each week separately.

    :param weekly_fit:
    :param bounds:
    :return:
    '''
    i = 1
    for week in weeks:

        fit_result = fit[week]
        week_data = data[week]
        plot_one_week_fit(week_data, fit_result, figure_number=i)
        i +=1



def plot_all_weeks(
        weekly_fit,
        weekly_data,
        weekly_bounds,
):
    '''
    plot data and model for the entire period.

    :param weekly_fit:
    :param weekly_data:
    :param weekly_bounds:
    :return:
    '''
    for week, bounds in weekly_bounds.items():
        # pdb.set_trace()
        start = bounds[0]

        # data
        week_data = weekly_data[week]

        # conform index back to all period values
        if week != '1':
            add_start = lambda x: x + start
            week_data = week_data.rename(index=add_start)

        # fit result
        fit_result = weekly_fit[week]

        # plot
        plot_one_week_fit(week_data, fit_result)

    figure = plt.gcf()

    return figure

# this should plot for each week the data and fiited curve of each LTT
def jointly_plot_ltts(
        data_set_name,
        init_params,
        model_function,
):
    ltts_data = {}
    for week in WEEKS:
        for ltt in LTTs:

            raw_data = get_raw_ltt(data_set_name, ltt)
            weekly_data = get_weekly_data(
                raw_data,WEEKLY_BOUNDS, INDICES_TO_DROP)
            weekly_fit = get_weekly_fit(
                weekly_data, init_params, model_function)


            ltts_data[ltt] = (weekly_data, weekly_fit)


    return ltts_data



# ----------------------------------------------- visualize the whole thing --------------------------------------------

def visualize_model(
        data_set_name: str,
        init_params: dict,
        model_function,
        ltt: str=None,
):
    '''
    plot measured data and fitted model for the entire incubation period.

    :param data_set_name:
    :param weekly_bounds:
    :param init_params:
    :param model_function:
    :param ltt:
    :return:
    '''

    # data
    raw_data = get_raw_ltt(data_set_name, ltt) if ltt else combine_raw_data(data_set_name)
    weekly_raw_data = get_weekly_data(raw_data, WEEKLY_BOUNDS)

    # fitting the data
    weekly_fit = get_weekly_fit(weekly_raw_data, init_params, model_function)

    # plotting
    figure = plot_all_weeks(weekly_fit, weekly_raw_data, WEEKLY_BOUNDS)

    return figure

