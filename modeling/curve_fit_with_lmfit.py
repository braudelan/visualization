# for 1st week MBC fit curve and plot together with measured dat

import matplotlib.pyplot as plt

from lmfit import Model

from data.raw_data import get_raw_data
from modeling.model_functions import *


def fit_curve(data, model_function):
    '''
    find best fit parameters.

    :param data: DataFrame
    raw data. index values are sampling events.
    :return:
    '''
    x = data.index.values
    y = data.values


    model = Model(model_function)
    params = model.make_params(a=2000, k_a=1, k_b=0.6)

    result = model.fit(y, params, t=x)

    return result

def plot_fit(data, fit_result):

    x = data.index.values
    y = data.values
    plt.plot(x, y, 'bo')
    plt.plot(x, fit_result.init_fit, 'k--', label='initial fit')
    plt.plot(x, fit_result.best_fit, 'r-', label='best fit')
    plt.legend(loc='best')
    plt.show()

# if __name__ == '__main__':
#
#     # data
#     get_raw_data('RESP')

