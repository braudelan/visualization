import pandas
import numpy

from matplotlib import pyplot
from sklearn.linear_model import LinearRegression
import statsmodels.api as statsmodels

from raw_data import get_raw_data, get_setup_arguments
from helpers import Constants, DataFrame_to_image


setup_arguments = get_setup_arguments()
DATA_SETS_NAMES = setup_arguments.sets
LEVEL_LABELS = Constants.level_labels

def get_r_squared(data, x: str, y: str):

    data = data[[x, y]]
    data = data.dropna()  # this will drop any row with any None value, in this case leaving only days 0, 14 and 28
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



def organize_data(data_sets_names, treatment: str=None):
    '''organize data to fit the corr method'''

    stacked_data_sets = []
    for data_set_name in data_sets_names:
        raw_data = get_raw_data(data_set_name)
        if treatment is not None:
            raw_data = raw_data[treatment]
            stacked = raw_data.stack(level=('soil', 'replicate'))
        else:
            stacked = raw_data.stack(LEVEL_LABELS)
        renamed = stacked.rename(data_set_name)

        stacked_data_sets.append(renamed)
    organized_data = pandas.concat(stacked_data_sets, axis=1)

    return organized_data


def plot_correlations(data):
    parameters = data.columns
    for ind_var in parameters:
        for dep_var in parameters.drop(ind_var):

            # compute regrresion and get r_square
            r_square = get_r_squared(data, ind_var, dep_var)
            r_square = round(r_square, 2)

            if r_square > 0.5:

                # data
                pairwise_data = data[[dep_var, ind_var]]
                pairwise_data = pairwise_data.dropna(how='all')
                x = pairwise_data[dep_var]
                y = pairwise_data[ind_var]

                # plot
                pyplot.scatter(x, y)
                axes = pyplot.gca()
                add_regrresion_line(x, y, axes)
                pyplot.xlabel(ind_var)
                pyplot.ylabel(dep_var)
                pyplot.xticks([])
                pyplot.yticks([])

                # add r_square
                pyplot.text(0.95, 0.1, f'r_square:{str(r_square)}',
                            fontweight='bold', horizontalalignment='right',
                            transform=axes.transAxes)

                save_to = '/home/elan/Dropbox/research' \
                          '/figures/correlations/linear_regrresion/' \
                          'test_%s_%s.png' % (ind_var, dep_var)
                pyplot.savefig(save_to, dpi=300, format='png',
                               bbox_inches='tight')
                pyplot.close()

            else:
                continue



# ------------------------------------- correlations matrix ------------------------------------------------------------
# DataFrame.corr() uses pearson pairwise correlation by default
def make_correlations_matrix(data_sets_names, treatment):
    data = organize_data(data_sets_names, treatment)
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
    output_file = f'{output_directory}correlations_{treatment}'
    DataFrame_to_image(correlations, css, output_file)

treatments = ['t', 'c', None]
for treatment in treatments:
    make_correlations_matrix(DATA_SETS_NAMES, treatment)
# ------------------------------------- plot --------------------------------------------------------------
# plot_correlations(all_parameters)



