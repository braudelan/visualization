from collections import namedtuple

from data.raw_data import get_raw_data, baseline_normalize
from data.significance import get_significance_booleans
from data.helpers import get_week_ends, Constants

Stats = namedtuple('Stats', ['means', 'stde'])
SOILS = Constants.groups


def get_raw_interval_growth(raw_data):

    sampling_days = raw_data.index

    first_day = sampling_days[0]
    second_day = sampling_days[1]
    second_to_last_day = sampling_days[-2]
    last_day = sampling_days[-1]

    interval_limits = [day for day in sampling_days if day in [0, 7, 14, 21, 28]]
    number_of_intervals = len(interval_limits) - 1

    def rename_columns(dataframe):

        def get_renaming_map(dataframe):
            old = dataframe.columns
            new = list(range(1, number_of_intervals + 1))
            zipped = zip(old, new)
            return dict(zipped)

        rename_by = get_renaming_map(dataframe)
        dataframe.rename(mapper=rename_by,
                         axis='columns', inplace=True)

    data = raw_data.loc[interval_limits]
    data = data.T

    interval_beginings = data.loc[:, first_day:second_to_last_day]
    interval_endings =  data.loc[:, second_day:last_day]

    # rename column labels from interval limits to intervals (days to weeks)
    endings_beginings = [
        interval_endings,
        interval_beginings
    ]
    for dataframe in endings_beginings:
        rename_columns(dataframe)

    # get growth
    interval_growth = interval_endings - interval_beginings

    # change irregular values to none
    # weekly_growth.loc[('ORG', 2), 4] = None
    interval_growth = interval_growth.droplevel(
                                    'replicate')
    interval_growth = interval_growth.rename_axis(
                                    columns='interval')



    return interval_growth


def get_weekly_growth(raw_data, treatment):
    '''
    retrun means of weekly growth for every soil.

    :parameter treatment: str
     't' for treated samples, 'c' for control samples.

    '''

    weekly_growth = get_raw_interval_growth(raw_data)


    stacked = weekly_growth.stack()
    grouped_soil_week = stacked.groupby(['soil', 'interval'])
    means = grouped_soil_week.mean()
    means = means.unstack().T
    stde = grouped_soil_week.sem()
    stde = stde.unstack().T

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
    weekly_growth = get_raw_interval_growth(raw_data)
    for soil in SOILS:
        soil_weekly_growth = weekly_growth.loc[soil]
        booleans = significance_between_weeks(soil_weekly_growth)
        print(f'{soil}:\n{booleans}')


