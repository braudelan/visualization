import pandas
from pandas import DataFrame, Series
import seaborn

from matplotlib import pyplot
from matplotlib.axes import Axes
from statsmodels.regression import linear_model
from statsmodels.regression.linear_model import RegressionResults
from statsmodels.tools.tools import add_constant

from data.raw_data import get_raw_data, get_setup_arguments
from data.helpers import Constants

FIGURES_DIRECTORY = Constants.figures_directory
OUTPUT_DIRECTORY = f'{FIGURES_DIRECTORY}/correlations/'

setup_arguments = get_setup_arguments()
DATA_SETS_NAMES = setup_arguments.sets
LEVEL_NAMES = Constants.level_names
UNITS = Constants.parameters_units

# plotting parameters
MARKERS = Constants.markers
MARKER_COLORS = Constants.colors


def write_regression_params(file, ind_var, dep_var, fit_result):

    percision = '.2f'

    data_pair = f'{ind_var} X {dep_var}'
    fit_params = fit_result.params
    intercept = fit_params[0]
    slope = fit_params[1]
    # equation = f'y = {slope}x + {intercept}'
    slope_f_value = fit_result.fvalue
    slope_f_pvalue = fit_result.f_pvalue
    slope_interval = fit_result.conf_int()[1]
    slope_low = slope_interval[0]
    slope_high = slope_interval[1]
    interval = f'{slope_low:{percision}}, {slope_high:{percision}}'
    r_square = fit_result.rsquared_adj

    output = f'\n\n{data_pair}:\n\n\n' \
             f'\t regression parameters: slope-{slope:{percision}},' \
             f' intercept-{intercept:{percision}}\n' \
             f'\t slope statistics: f value = {slope_f_value:{percision}},' \
             f' f pvalue = {slope_f_pvalue:{percision}}\n'\
             f'\t slope confidence interval: {interval}\n' \
             f'\t r squared adj: {r_square:{percision}}\r'

    file.write(output)
    file.close()


def stack_data(raw_data,
               normalize_by=None, treatment: str=None):
    '''
    stack the raw data .

    parameters
    ----------

    raw_data: str or DataFrame
        if a string is given it will be used as an argument for get_raw_data()..

    normalize_by: function, optional
        how to normalize the data.

    treatment: str, optional
        can be either "t" (use data from treated samples) or "c" (use data from control samples)

    returns
    -------
    stacked_data_set: Series
        Series.index are the group id's for regression
        and Series.values are the results being regressed.
        Series.name is the name of the data set.
        '''

    # data
    data = get_raw_data(raw_data) if type(raw_data) == str else raw_data
    data = (
        normalize_by(data) if normalize_by else
        data[treatment] if treatment else
        data
    )

    # stack and rename the resulting Series
    columns_level_names = data.columns.names
    stacked_data_set = data.stack(columns_level_names)
    # stacked_data_set = stacked.rename(data_set_name)

    return stacked_data_set
#
# def get_stacked_data(data_set_names):
#
#     stacked_data_sets_list = []
#     for data_set_name in data_sets_names:
#         stacked_data = stack_data(data_set_name)
#         stacked_data_sets_list.append(stacked_data)
#
#     return stacked_data_sets_list

def combine_data_sets(raw_data_sets: dict):
    '''
    combine data sets into one DataFrame.

    parameter
    ---------
    raw_data_sets: dict
        keys are the data sets names,
        values are DataFrames with raw data.
        
    returns
    -------
    concatenated: DataFrame
        columns are the names of the data sets.
    '''


    # stacked and name the data sets
    for key, value in raw_data_sets.items():
        new_value = stack_data(value)
        new_value.name = key
        raw_data_sets[key] = new_value

    # concat the stacked data sets
    concatenated = pandas.concat(raw_data_sets.values(), axis=1)

    # drop unnecessary index levels
    levels_to_drop = ['days', 'replicate']
    concatenated = concatenated.droplevel(levels_to_drop).reset_index()

    return concatenated


def get_regression(x, y)-> RegressionResults:

    y = y.values
    x = x.values
    x = add_constant(x)

    # intialize the model
    model = linear_model.OLS(y, x, missing='drop')

    # fit the regression
    fit_result = model.fit()

    return fit_result


def scatter_and_regression_line(data, title,
                                x_name, y_name, fit_result=None):

    with pyplot.style.context(u'incubation-dynamics'):
        # initialize figure and axes
        figure = pyplot.figure()

        # plot
        axes: Axes = seaborn.scatterplot(
            x=x_name,
            y=y_name,
            hue='soil',
            # style='days',
            data=data,
            palette=MARKER_COLORS,
        )
        regression_line_kws = {
            'color': 'k',
            'lw': 1,
        }
        seaborn.regplot(
            x=x_name,
            y=y_name,
            data=data,
            robust=True,
            scatter=False,
            ax=axes,
            line_kws=regression_line_kws,
        )

        # legend
        handles, labels = axes.get_legend_handles_labels()
        handles.pop(0)
        labels.pop(0)
        axes.legend(handles, labels)

        # labels and decorations
        axes.set_title(title, pad=5)
        x_label = f'{x_name}'
        y_label = f'{y_name}'

        # r_sqaure
        rsqaured_x, rsqaured_y = (0.95, 0.1)
        if fit_result:
            r_square = round(fit_result.rsquared,2)
            axes.text(
                x=rsqaured_x,
                y=rsqaured_y,
                s=fr'$r_square: {str(r_square)}$',
                fontweight='bold',
                horizontalalignment='right',
                transform=axes.transAxes
            )

    return axes
#
#
#
# def visualize_regression(all_parameters, min_r_square, ):
#
#     def save_regression_plot(figure):
#         save_to = f'{OUTPUT_DIRECTORY}' \
#                   f'{ind_var}_{dep_var}_test.png'
#         figure.savefig(save_to, dpi=300,
#                        format='png',bbox_inches='tight')
#         pyplot.close()
#
#
#     def add_regression_line(axes):
#
#         lower_xlim, upper_xlim = axes.get_xlim()
#         X_plot = numpy.linspace(lower_xlim, upper_xlim, 100)
#         y = slope * X_plot + intercept
#
#         axes.plot(X_plot, y, '-')
#
#
#     def plot_regression(pairwise_data,
#                         x_name, y_name, fit_result):
#
#         # initialize figure and axes
#         figure = pyplot.figure()
#
#         # plot
#         axes = seaborn.scatterplot(x=x_name,
#                                    y=y_name,
#                                    hue='treatment',
#                                    style='soil',
#                                    data=pairwise_data)
#
#         # labels and decorations
#         x_label = f'{x_name} ({UNITS[x_name]})'
#         y_label = f'{y_name} ({UNITS[y_name]})'
#         axes.set_ylabel(y_label, labelpad=0.1)
#         axes.set_xlabel(x_label, labelpad=0.1)
#
#         # r_sqaure
#         axes.text(0.95, 0.1, f'r_square:{str(r_square)}',
#                   fontweight='bold',
#                   horizontalalignment='right',
#                   transform=axes.transAxes)
#
#         return figure
#
#
#     def write_regression_params(file):
#
#         data_pair = f'{ind_var} X {dep_var}'
#         equation = f'y = {slope}x + {intercept}'
#         interval = f'confidence interval for the slope:' \
#                    f'{slope_confidence[0]}, {slope_confidence[1]}'
#         rsquared = f'r_squared: {r_square}'
#
#         output = f'\n\n{data_pair}:\n' \
#                  f'\t{equation}\n' \
#                  f'\t{interval}\n' \
#                  f'\t{rsquared}\r'
#
#         file.write(output)
#
#     file = open(f'{OUTPUT_DIRECTORY}coefficients.txt', 'w+')
#
#     parameters = all_parameters.columns
#     for ind_var in parameters:
#         for dep_var in parameters.drop(ind_var):
#
#             # data
#             paird_data_sets = [ind_var, dep_var]
#             pairwise_data = all_parameters[paird_data_sets]
#             pairwise_data = pairwise_data.dropna(how='any')
#             pairwise_data = pairwise_data.reset_index()
#             x = pairwise_data[ind_var]
#             y = pairwise_data[dep_var]
#
#             # compute regression
#             fit_result = get_regression(x, y)
#
#             # regression results
#             round_to = 3
#             alpha = 0.05
#             r_square = round(fit_result.rsquared, round_to)
#             intercept, slope = fit_result.params.round(round_to)
#             conf_interval = fit_result.conf_int(alpha).round(round_to)
#             slope_confidence =  conf_interval[1]
#
#
#             if r_square > min_r_square:
#
#                 # plot
#                 figure = plot_regression(
#                     pairwise_data, ind_var, dep_var, r_square)
#
#                 # add regression line
#                 axes = figure.axes[0]
#                 add_regression_line(axes)
#
#                 # save plot
#                 save_regression_plot(figure)
#
#                 # write regression parameters
#                 write_regression_params(file)
#
#
#             else:
#                 continue
#
#     return
#
# def correlations_matrix():
#     data = get_all_parameters(DATA_SETS_NAMES)
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
#     output_file = f'{output_directory}pairwise_pearson'
#     DataFrame_to_image(correlations, css, output_file)
#
#
# if __name__ == '__main__':
#     data = get_all_parameters(DATA_SETS_NAMES)
#     # correlations_matrix()

# def set_marker_parameters(axes, handles, labels, colors=MARKER_COLORS):
#
#     handles_and_labels = dict(zip(handles, labels))
#
#     for handle, soil_label in handles_and_labels.items():
#         handle.set_color(colors[soil_label])

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
