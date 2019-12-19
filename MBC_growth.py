from collections import namedtuple

from raw_data import get_raw_data, baseline_normalize
from significance import get_significance_booleans
from helpers import get_week_ends, Constants

Stats = namedtuple('Stats', ['means', 'stde'])
SOILS = Constants.groups


def growth(raw_data):


def get_weekly_growth(raw_data):

    def rename_columns(dataframe):

        def get_renaming_map(dataframe):
            old = dataframe.columns
            new = list(range(1, 5))
            zipped = zip(old, new)
            return dict(zipped)

        rename_by = get_renaming_map(dataframe)
        dataframe.rename(mapper=rename_by,
                         axis='columns', inplace=True)

    intervals_limits = get_week_ends(raw_data)
    data = raw_data.loc[intervals_limits]
    data = data.T

    t_start = data.loc[:, 0:21]
    t_end =  data.loc[:, 7:28]

    # rename column labels from interval limits to intervals (days to weeks)
    endings_beginings = [
        t_end,
        t_start
    ]
    for dataframe in endings_beginings:
        rename_columns(dataframe)

    # get weekly growth
    weekly_growth = t_end - t_start

    # change irregular values to none
    weekly_growth.loc[('ORG', 2), 4] = None
    weekly_growth = weekly_growth.droplevel(
                                    'replicate')
    weekly_growth = weekly_growth.rename_axis(
                                    columns='week')



    return weekly_growth

def get_weekly_growth_means(weekly_growth):
    '''retrun means of weekly growth for every soil.'''
    stacked = weekly_growth.stack()
    grouped_soil_week = stacked.groupby(['soil', 'week'])
    means = grouped_soil_week.mean()
    stde = grouped_soil_week.sem()

    return Stats(
        means=means,
        stde=stde
    )

def significance_between_weeks(soil_weekly_growth):
    '''compute significance between weekly growth for specific soil.'''

    data = soil_weekly_growth
    data = data.stack().droplevel(0)

    booleans = get_significance_booleans(data)

    return booleans

if __name__ == '__main__':

    raw_data = get_raw_data('MBC')
    raw_data = baseline_normalize(raw_data)
    weekly_growth = get_weekly_growth(raw_data)
    for soil in SOILS:
        soil_weekly_growth = weekly_growth.loc[soil]
        booleans = significance_between_weeks(soil_weekly_growth)
        print(f'{soil}:\n{booleans}')