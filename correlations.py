import pandas

from matplotlib import pyplot

from raw_data import get_raw_data, get_setup_arguments

setup_arguments = get_setup_arguments()
DATA_SETS_NAMES = setup_arguments.sets

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

# compute correlations
correlations = all_parameters.corr()

parameters = all_parameters.columns
x = 'HWS'
for parameter in parameters:
    all_parameters.plot(x=x, y=parameter)
    pyplot.show()
    pyplot.cla()


# ------------------------------------- example of how to get r_square -------------------------------------------------
# from sklearn.linear_model import LinearRegression
#
# data = all_parameters[['HWS', 'AS']]
# data = data.dropna()  # this will drop any row with any None value, in this case leaving only days 0, 14 and 28
# y = data['AS'].values
# x = data['HWS'].values
#
# model = LinearRegression()
# model.fit(x, y)
# r_sq = model.score(x, y)



