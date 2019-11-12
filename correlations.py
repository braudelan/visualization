import pandas

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


stacked_data_sets = organize_data(DATA_SETS_NAMES)
all_parameters = pandas.concat(stacked_data_sets, axis=1)

# ------------------------------------- correlations matrix ------------------------------------------------------------
correlations = all_parameters.corr()

# ------------------------------------- linear regression --------------------------------------------------------------
parameters = all_parameters.columns
for ind_var in parameters:
    for dep_var in parameters.drop(ind_var):
        r_square = get_r_square(ind_var, dep_var)
        if r_square > 0.5:
            all_parameters.plot(x=ind_var, y=dep_var, kind='scatter')
            pyplot.text(0.8, 0.8, str(r_square))

            save_to = '/home/elan/Dropbox/research' \
                  '/figures/correlations/linear_regrresion/'\
                  '%s_%s.png' %(ind_var,dep_var)
            pyplot.savefig(save_to, dpi=300, format='png', bbox_inches='tight')
            pyplot.close()
        else:
            continue



