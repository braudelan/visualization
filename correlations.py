import pandas
import numpy

from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from sklearn.linear_model import LinearRegression
import statsmodels.api as statsmodels

from raw_data import get_raw_data, get_setup_arguments, baseline_normalize
from helpers import Constants, DataFrame_to_image


setup_arguments = get_setup_arguments()
DATA_SETS_NAMES = setup_arguments.sets
LEVEL_NAMES = Constants.level_names

def get_r_squared(data, x: str, y: str):

    data = data[[x, y]]
    data = data.dropna()  # drop any row that has any None values
    n_samples = data.shape[0]
    y = data[y].values.reshape(n_samples, 1)
    x = data[x].values.reshape(n_samples, 1)

    model = LinearRegression()
    model.fit(x, y)
    r_sq = model.score(x, y)

    return r_sq


def add_regrresion_line(x, y, axes):
    m, b = numpy.polyfit(x, y, 1)
    X_plot = numpy.linspace(axes.get_xlim()[0], axes.get_xlim()[1], 100)
    pyplot.plot(X_plot, m * X_plot + b, '-')


def organize_data_sets(data_sets_names,
                       normalize_by=None, treatment: str=None):
    '''organize data to fit regrresion functions'''

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
    stacked_data_sets = []
    for data_set_name in data_sets_names:
        stacked_data = stack_data(data_set_name)
        stacked_data_sets.append(stacked_data)

    # concat the stacked data sets into a dataframe
    organized_data_sets = pandas.concat(
                            stacked_data_sets, axis=1)

    # drop unnecessary index levels
    levels_to_drop = ['days', 'replicate']
    organized_data_sets = organized_data_sets.\
                            droplevel(levels_to_drop)

    return organized_data_sets




def visualize_correlations(data, data_type):

    def plot_regrresion(data, ind_var, dep_var):

        # get the data and assign x and y
        pairwise_data = data[[dep_var, ind_var]]
        pairwise_data = pairwise_data.dropna(how='all')
        x = pairwise_data[dep_var]
        y = pairwise_data[ind_var]

        # initialize figure and axes
        figure = pyplot.figure()
        axes: Axes = figure.add_subplot(111)

        # plot
        axes.scatter(x, y)
        add_regrresion_line(x, y, axes)

        # labels etc.
        x_label = ind_var
        y_label = dep_var
        axes.set_ylabel(y_label)
        axes.set_xlabel(x_label)


    parameters = data.columns
    for ind_var in parameters:
        for dep_var in parameters.drop(ind_var):

            # compute regrresion and get r_square
            r_square = get_r_squared(data, ind_var, dep_var)
            r_square = round(r_square, 2)

            if r_square > 0.5:

                # data


                # plot
                plot_regrresion(data, ind_var, dep_var)
                # add r_square
                pyplot.text(0.95, 0.1, f'r_square:{str(r_square)}',
                            fontweight='bold', horizontalalignment='right',
                            transform=axes.transAxes)

                save_to = f'/home/elan/Dropbox/research' \
                          f'/figures/correlations/linear_regrresion/' \
                          f'{data_type}_{ind_var}_{dep_var}.png'
                pyplot.savefig(save_to, dpi=300, format='png',
                               bbox_inches='tight')
                pyplot.close()

            else:
                continue

if __name__ == '__main__':
    organized_data = organize_data_sets(DATA_SETS_NAMES)


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

