import pdb

import numpy
import pandas
from pandas import DataFrame, Series
import seaborn

from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from sklearn.linear_model import LinearRegression
from statsmodels.regression import linear_model
from statsmodels.regression.linear_model import RegressionResults
from statsmodels.tools.tools import add_constant

from raw_data import get_raw_data, get_setup_arguments, baseline_normalize
from helpers import Constants, DataFrame_to_image

FIGURES_DIRECTORY = Constants.figures_directory
OUTPUT_DIRECTORY = f'{FIGURES_DIRECTORY}/correlations/'

setup_arguments = get_setup_arguments()
DATA_SETS_NAMES = setup_arguments.sets
LEVEL_NAMES = Constants.level_names
UNITS = Constants.parameters_units


def get_all_parameters(data_sets_names,
                       normalize_by=None, treatment: str=None):
    '''organize data to fit regression functions'''

    def stack_data(data_set_name):

        # get raw data
        raw_data = get_raw_data(data_set_name)
        raw_data = (
            normalize_by(raw_data) if normalize_by else
            raw_data[treatment] if treatment else
            raw_data
        )

        # stack and rename the resulting Series
        columns_level_names = raw_data.columns.names
        stacked = raw_data.stack(columns_level_names)
        renamed = stacked.rename(data_set_name)
        stacked_data = renamed

        return stacked_data

    # get all the stacked data sets
    stacked_data_sets_list = []
    for data_set_name in data_sets_names:
        stacked_data = stack_data(data_set_name)
        stacked_data_sets_list.append(stacked_data)

    # concat the stacked data sets into a dataframe
    all_parameters = pandas.concat(
                    stacked_data_sets_list, axis=1)

    # drop unnecessary index levels
    levels_to_drop = 'days'
    all_parameters = all_parameters.droplevel(
                                    levels_to_drop)

    return all_parameters


def get_regression(x, y)-> RegressionResults:

    y = y.values
    x = x.values
    x = add_constant(x)

    # intialize the model
    model = linear_model.OLS(y, x, missing='drop')

    # fit the regression
    fit_result = model.fit()

    return fit_result

def scatter_and_regression_line(data, data_set_name,
                         x_name, y_name, fit_result=None):

    # initialize figure and axes
    figure = pyplot.figure()

    # plot
    regression_line_kws = {
        'color': 'k',
        'lw': 1,
    }
    axes: Axes = seaborn.scatterplot(
        x=x_name,
        y=y_name,
        hue='soil',
        style='days',
        data=data,
    )
    seaborn.regplot(
        x=x_name,
        y=y_name,
        data=data,
        robust=True,
        scatter=False,
        ax=axes,
        line_kws=regression_line_kws,
    )

    # labels and decorations
    axes.set_title(data_set_name, pad=5)
    x_label = f'{x_name}'
    y_label = f'{y_name}'
    axes.set_ylabel(y_label, labelpad=0.1)
    axes.set_xlabel(x_label, labelpad=0.1)

    # r_sqaure
    rsqaured_x, rsqaured_y = (0.95, 0.1)
    if fit_result:
        r_square = round(fit_result.rsquared,2)
        axes.text(
            x=rsqaured_x,
            y=rsqaured_y,
            s=f'r_square: {str(r_square)}',
            fontweight='bold',
            horizontalalignment='right',
            transform=axes.transAxes
        )
    pyplot.close()

    return axes



def visualize_regression(all_parameters, min_r_square, ):

    def save_regression_plot(figure):
        save_to = f'{OUTPUT_DIRECTORY}' \
                  f'{ind_var}_{dep_var}_test.png'
        figure.savefig(save_to, dpi=300,
                       format='png',bbox_inches='tight')
        pyplot.close()


    def add_regression_line(axes):

        lower_xlim, upper_xlim = axes.get_xlim()
        X_plot = numpy.linspace(lower_xlim, upper_xlim, 100)
        y = slope * X_plot + intercept

        axes.plot(X_plot, y, '-')


    def plot_regression(pairwise_data,
                        x_name, y_name, fit_result):

        # initialize figure and axes
        figure = pyplot.figure()

        # plot
        axes = seaborn.scatterplot(x=x_name,
                                   y=y_name,
                                   hue='treatment',
                                   style='soil',
                                   data=pairwise_data)

        # labels and decorations
        x_label = f'{x_name} ({UNITS[x_name]})'
        y_label = f'{y_name} ({UNITS[y_name]})'
        axes.set_ylabel(y_label, labelpad=0.1)
        axes.set_xlabel(x_label, labelpad=0.1)

        # r_sqaure
        axes.text(0.95, 0.1, f'r_square:{str(r_square)}',
                  fontweight='bold',
                  horizontalalignment='right',
                  transform=axes.transAxes)

        return figure


    def write_regression_params(file):

        data_pair = f'{ind_var} X {dep_var}'
        equation = f'y = {slope}x + {intercept}'
        interval = f'confidence interval for the slope:' \
                   f'{slope_confidence[0]}, {slope_confidence[1]}'
        rsquared = f'r_squared: {r_square}'

        output = f'\n\n{data_pair}:\n' \
                 f'\t{equation}\n' \
                 f'\t{interval}\n' \
                 f'\t{rsquared}\r'

        file.write(output)

    file = open(f'{OUTPUT_DIRECTORY}coefficients.txt', 'w+')

    parameters = all_parameters.columns
    for ind_var in parameters:
        for dep_var in parameters.drop(ind_var):

            # data
            paird_data_sets = [ind_var, dep_var]
            pairwise_data = all_parameters[paird_data_sets]
            pairwise_data = pairwise_data.dropna(how='any')
            pairwise_data = pairwise_data.reset_index()
            x = pairwise_data[ind_var]
            y = pairwise_data[dep_var]

            # compute regression
            fit_result = get_regression(x, y)

            # regression results
            round_to = 3
            alpha = 0.05
            r_square = round(fit_result.rsquared, round_to)
            intercept, slope = fit_result.params.round(round_to)
            conf_interval = fit_result.conf_int(alpha).round(round_to)
            slope_confidence =  conf_interval[1]


            if r_square > min_r_square:

                # plot
                figure = plot_regression(
                    pairwise_data, ind_var, dep_var, r_square)

                # add regression line
                axes = figure.axes[0]
                add_regression_line(axes)

                # save plot
                save_regression_plot(figure)

                # write regression parameters
                write_regression_params(file)


            else:
                continue

    return

def correlations_matrix():
    data = get_all_parameters(DATA_SETS_NAMES)
    correlations = data.corr()

    css = """
        <style type=\"text/css\">
        table {
        color: #333;
        font-family: Helvetica, Arial, sans-serif;
        width: 640px;
        border-collapse:
        collapse;
        border-spacing: 0;
        }
        td, th {
        border: 1px solid transparent; /* No more visible border */
        height: 30px;
        }
        th {
        background: #DFDFDF; /* Darken header a bit */
        font-weight: bold;
        }
        td {
        background: #FAFAFA;
        text-align: center;
        }
        table tr:nth-child(odd) td{
        background-color: white;
        }
        </style>
        """  # html code specifying the appearence of significance table
    output_directory = '/home/elan/Dropbox/research/figures/correlations/'
    output_file = f'{output_directory}pairwise_pearson'
    DataFrame_to_image(correlations, css, output_file)


if __name__ == '__main__':
    data = get_all_parameters(DATA_SETS_NAMES)
    # correlations_matrix()
    visualize_regression(data, 0.6)

# # ------------------------------------- correlations matrix ------------------------------------------------------------
# # # DataFrame.corr() uses pearson pairwise correlation by default
#
# # treatments = ['t', 'c', None]
# # for treatment in treatments:
# #     make_correlations_matrix(DATA_SETS_NAMES, treatment)
# # ------------------------------------- plot --------------------------------------------------------------
# # plot_correlations(all_parameters)
#
#
#
# def linear_regression_statsmodels(x, y):
#
#     y = y.values
#     x = x.values
#     x = sm.add_constant(x)
#
#     model = sm.OLS(y, x, missing='drop')
#     fit_result = model.fit()
#
#     return fit_result
#
# def linaer_regression_sklearn(pairwise_data: DataFrame,
#                               x: Series, y: Series):
#
#     n_samples = pairwise_data.shape[0]
#     y = y.values.reshape(n_samples, 1)
#     x = x.values.reshape(n_samples, 1)
#
#     model = LinearRegression()
#     model.fit(x, y)
#     r_sq = model.score(x, y)
#     r_sq = round(r_sq, 2)
#
#     return r_sq
#
# def add_regression_line(axes, x, y):
#     slope, intercept = numpy.polyfit(x, y, 1)
#     X_plot = numpy.linspace(
#         axes.get_xlim()[0], axes.get_xlim()[1], 100)
#     x = X_plot
#     y = slope * X_plot + intercept
#     axes.plot(x, y, '-')
#
#     slope = round(slope, 4)
#     intercept = round(intercept, 4)
#
#     return slope, intercept
#
#
# def plot_regression(pairwise_data,
#                     x_name, y_name, fit_result):
#
#     # initialize figure and axes
#     figure = pyplot.figure()
#
#     # plot
#     axes = seaborn.scatterplot(x=x_name,
#                         y=y_name,
#                         hue='treatment',
#                         style='soil',
#                         data=pairwise_data)
#     #
#     # # regression line
#     # add_regression_line()
#
#     # labels and decorations
#     x_label = f'{x_name} ({UNITS[x_name]})'
#     y_label = f'{y_name} ({UNITS[y_name]})'
#     axes.set_ylabel(y_label, labelpad=0.1)
#     axes.set_xlabel(x_label, labelpad=0.1)
#
#     # r_sqaure
#     axes.text(0.95, 0.1, f'r_square:{str(r_square)}',
#                 fontweight='bold',
#                 horizontalalignment='right',
#                 transform=axes.transAxes)
#
#     return figure
