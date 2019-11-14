import pandas
import numpy

from matplotlib import pyplot
from sklearn.linear_model import LinearRegression

from raw_data import get_raw_data, get_setup_arguments

setup_arguments = get_setup_arguments()
DATA_SETS_NAMES = setup_arguments.sets

def get_r_square(x: str, y: str):

    data = all_parameters[[x, y]]
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



def organize_data(data_sets_names):
    '''organize data to fit the corr method'''

    stacked_data_sets = []
    for data_set_name in data_sets_names:
        raw_data = get_raw_data(data_set_name)
        grouped = raw_data.groupby(level=('soil', 'treatment')
                                                , axis='columns')
        means = grouped.mean()
        stacked_twice = means.stack().stack()
        renamed = stacked_twice.rename(data_set_name)

        stacked_data_sets.append(renamed)

    return stacked_data_sets


def plot_correlations(arranged_data):
    parameters = arranged_data.columns
    for ind_var in parameters:
        for dep_var in parameters.drop(ind_var):

            # compute regrresion and get r_square
            r_square = get_r_square(ind_var, dep_var)
            r_square = round(r_square, 2)

            if r_square > 0.5:

                # data
                data = all_parameters[[dep_var, ind_var]]
                data = data.dropna(how='any')
                x = data[dep_var]
                y = data[ind_var]

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


stacked_data_sets = organize_data(DATA_SETS_NAMES)
all_parameters = pandas.concat(stacked_data_sets, axis=1)

# ------------------------------------- correlations matrix ------------------------------------------------------------
# correlations = all_parameters.corr()


# ------------------------------------- plot --------------------------------------------------------------
# plot_correlations(all_parameters)



