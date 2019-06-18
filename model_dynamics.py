import pandas
import numpy
from matplotlib import pyplot
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

from get_raw_data import get_setup_arguments
from get_raw_data import get_raw_data
from get_stats import get_stats
from helpers import get_week_ends


SOILS = ['ORG', 'MIN', 'UNC']

# which data sets to load
setup_arguments = get_setup_arguments()
data_set = setup_arguments.sets[0]

# get data
raw_data = get_raw_data(data_set)
week_ends = get_week_ends(raw_data)
data = raw_data.loc[week_ends, ('t', SOILS)].reset_index(col_level=1, col_fill='')
data.columns = data.columns.droplevel('treatment')

# define x data and names of data series
data_series_names = SOILS
X = data['days'].values

# fit function
def y_fit(x, c0, c1, c2, c3):
    return c0 + c1*x - c2*x**2 - c3*x**3

# instantiate a figure and axes
model_figure = pyplot.figure()
axes = model_figure.add_subplot(111)

text_indent = 0.06
i = 0

lines = {}
# fit curve for every soil and plot fit functions over measured values
for series_name in data_series_names:

    y_data = data[series_name].values
    minimum = numpy.nanmin(y_data)

    # initial guess for parameters
    p0 = [minimum, 0.01, minimum, 0.01 ]

    # fit curve
    coefficients, cov = curve_fit(y_fit, X, y_data, p0)

    # calculate y based on model coefficients
    y_predicted = y_fit(X, coefficients[0], coefficients[1], coefficients[2], coefficients[3])

    # calculate R_square
    r_square = r2_score(y_data, y_predicted)

    lines[series_name + 'measured'] = axes.plot(X, y_data, 'b', label='measured')
    lines[series_name + 'predicted'] = axes.plot(X, y_predicted, 'r:', label='predicted')

    axes.text(0.1, i - text_indent, series_name + str(r_square), transform=axes.transAxes)

    i += text_indent
