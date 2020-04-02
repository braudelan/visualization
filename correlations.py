import pdb

import pandas
from pandas import DataFrame, Series
import seaborn

from matplotlib import pyplot
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from statsmodels.regression import linear_model
from statsmodels.regression.linear_model import RegressionResults
from statsmodels.tools.tools import add_constant

from data.raw_data import get_raw_data, get_multi_sets
from data.stats import get_multiple_stats
from data.helpers import Constants, Stats


# output directories
FIGURES_DIRECTORY = Constants.figures_directory
OUTPUT_DIRECTORY = f'{FIGURES_DIRECTORY}/correlations'

# Constants
LEVEL_NAMES = Constants.level_names
UNITS = Constants.parameters_units

# plotting parameters
MARKERS = Constants.markers
MARKER_COLORS = Constants.colors

# regression parameters
TRESHOLD_R = 0


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
    stack raw data .

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

    # stack
    columns_level_names = data.columns.names
    stacked_data_set = data.stack(columns_level_names)

    return stacked_data_set


def combine_data_sets(data_sets: dict):
    '''

    :param data_sets: dict
    either a raw_data_sets or stats_data_sets object.
    keys are data sets names.
    values are either raw or mean DataFrams.

    :return: combined
    columns are names of data sets
    '''

    first_dict_value = list(data_sets.values())[0]
    mean_data = True if type(first_dict_value) == Stats else False

    # stacked and name the data sets
    for key, value in data_sets.items():
        value = value.means if mean_data else value
        new_value = stack_data(value)
        new_value.name = key
        data_sets[key] = new_value

    # concat the stacked data sets
    combined = pandas.concat(data_sets.values(), axis=1)

    # drop unnecessary index levels
    if not mean_data:
        levels_to_drop = ['replicate']
        combined = combined.droplevel(levels_to_drop).reset_index()

    return combined


def get_regression(x, y)-> RegressionResults:

    y = y.values
    x = x.values
    x = add_constant(x)

    # intialize the model
    model = linear_model.OLS(y, x, missing='drop')

    # fit the regression
    fit_result = model.fit()

    return fit_result


def plot_regression(data, title,
                    x_name, y_name, fit_result=None):

    with pyplot.style.context(u'incubation-dynamics'):
        # initialize figure and axes
        figure: Figure = pyplot.figure()

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

    return figure


def visualize_regression(combined_data, note: str=None):
    #todo probably remove the note param,
    #   add a dir param to direct specific correlations into seperate dir
    #   change param name combined_data
    '''

    :param combined_data:
    :param note: str
    will be added into the file name before
     regressor and regressand names.
    :return:
    '''

    def print_info():
        """print regression parameters"""
        n_data_points = len(combined_data)

    note = note if note + '_' else None

    id_columns = ['days', 'treatment', 'soil']
    parameters = combined_data.drop(id_columns, axis=1).columns
    for ind_var in parameters:
        for dep_var in parameters.drop(ind_var):

            pairwise_data = combined_data[[dep_var, ind_var]]
            pairwise_data = pairwise_data.dropna(how='all')
            x = pairwise_data[dep_var]
            y = pairwise_data[ind_var]
            # pdb.set_trace()
            regression_params = get_regression(x, y)

            title = f'{ind_var} X {dep_var}'

            if regression_params.rsquared > TRESHOLD_R:

                figure = plot_regression(combined_data, title,
                                 ind_var, dep_var, regression_params)

                save_to = f'{OUTPUT_DIRECTORY}/' \
                          f'{note}_' \
                          f'{title}.png'
                figure.savefig(fname=save_to, bbox_inches='tight')

    print(len(combined_data))

if __name__ == '__main__':

    data_set_names = get_setup_arguments()
    raw_data_sets = get_multi_sets(data_set_names, treatment='c')
    data_sets = get_multiple_stats(raw_data_sets)
    combined_data = combine_data_sets(data_sets)

    # visualize_regression(combined_data)

# todo write a func that computes the correlation
#   between the 'first differences' of time series
#   of two parameters (e.g DOC and RESP) doing this
#   comparison for every LTT (i.e soil)
#   the code below is a general direction

























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
