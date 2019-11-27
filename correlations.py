import pdb

import numpy
import pandas
from pandas import DataFrame, Series
import seaborn

from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from sklearn.linear_model import LinearRegression
import statsmodels.api as statsmodels

from raw_data import get_raw_data, get_setup_arguments, baseline_normalize
from helpers import Constants, DataFrame_to_image

FIGURES_DIRECTORY = Constants.figures_directory
OUTPUT_DIRECTORY = f'{FIGURES_DIRECTORY}/correlations/'

setup_arguments = get_setup_arguments()
DATA_SETS_NAMES = setup_arguments.sets
LEVEL_NAMES = Constants.level_names
UNITS = Constants.parameters_units

def get_r_squared(pairwise_data: DataFrame,
                        x: Series, y: Series):

    n_samples = pairwise_data.shape[0]
    y = y.values.reshape(n_samples, 1)
    x = x.values.reshape(n_samples, 1)

    model = LinearRegression()
    model.fit(x, y)
    r_sq = model.score(x, y)
    r_sq = round(r_sq, 2)

    return r_sq


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


def plot_regression(pairwise_data,
                    x_name, y_name, r_square):

    def add_regression_line():
        x = pairwise_data[x_name]
        y = pairwise_data[y_name]
        slope, intercept = numpy.polyfit(x, y, 1)
        X_plot = numpy.linspace(
            axes.get_xlim()[0], axes.get_xlim()[1], 100)
        x = X_plot
        y = slope * X_plot + intercept
        axes.plot(x, y, '-')

    # initialize figure and axes
    figure = pyplot.figure()

    # plot
    axes = seaborn.scatterplot(x=x_name,
                        y=y_name,
                        hue='treatment',
                        style='soil',
                        data=pairwise_data)

    # regression line
    add_regression_line()

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

def visualize_regression(all_parameters, min_r_square):

    def save_regression_plot(figure):
        save_to = f'{OUTPUT_DIRECTORY}' \
                  f'{ind_var}_{dep_var}_test.png'
        figure.savefig(save_to, dpi=300,
                       format='png',bbox_inches='tight')
        pyplot.close()

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

            # compute regression and get r_square
            r_square = get_r_squared(pairwise_data, x, y)

            if r_square > min_r_square:
                # plot
                figure = plot_regression(
                    pairwise_data, ind_var, dep_var, r_square)

                # save plot
                save_regression_plot(figure)
            else:
                continue


if __name__ == '__main__':
    data = get_all_parameters(DATA_SETS_NAMES)
    visualize_regression(data, 0.6)

# ------------------------------------- correlations matrix ------------------------------------------------------------
# # DataFrame.corr() uses pearson pairwise correlation by default
# def make_correlations_matrix(data_sets_names, treatment):
#     data = organize_data(data_sets_names, treatment)
#     correlations = data.corr()
#
#     css = """
#         <style type=\"text/css\">
#         table {
#         color: #333;
#         font-family: Helvetica, Arial, sans-serif;
#         width: 640px;
#         border-collapse:
#         collapse;
#         border-spacing: 0;
#         }
#         td, th {
#         border: 1px solid transparent; /* No more visible border */
#         height: 30px;
#         }
#         th {
#         background: #DFDFDF; /* Darken header a bit */
#         font-weight: bold;
#         }
#         td {
#         background: #FAFAFA;
#         text-align: center;
#         }
#         table tr:nth-child(odd) td{
#         background-color: white;
#         }
#         </style>
#         """  # html code specifying the appearence of significance table
#     output_directory = '/home/elan/Dropbox/research/figures/correlations/'
#     output_file = f'{output_directory}correlations_{treatment}'
#     DataFrame_to_image(correlations, css, output_file)
#
# treatments = ['t', 'c', None]
# for treatment in treatments:
#     make_correlations_matrix(DATA_SETS_NAMES, treatment)
# ------------------------------------- plot --------------------------------------------------------------
# plot_correlations(all_parameters)

