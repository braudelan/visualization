# for 1st week MBC fit curve and plot together with measured dat

import matplotlib.pyplot as plt

from lmfit import Model

from data.raw_data import get_raw_data
from modeling.model_functions import *

# data
first_week = [0, 1, 3, 7]
data = get_raw_data('MBC')['t']['MIN'] # treatment raw data for 'MIN' soil
data = data.stack().droplevel('replicate').loc[first_week]

x = data.index.values
y = data.values


growth_decay_model = Model(growth_decay)
params = growth_decay_model.make_params(a=2000, k_a=1, k_b=0.6)

result = growth_decay_model.fit(y, params, t=x)

print(result.fit_report())

plt.plot(x, y, 'bo')
plt.plot(x, result.init_fit, 'k--', label='initial fit')
plt.plot(x, result.best_fit, 'r-', label='best fit')
plt.legend(loc='best')
plt.show()