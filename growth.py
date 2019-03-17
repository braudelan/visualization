import pandas
from pandas import DataFrame

def get_weekly_growth(means: DataFrame):

    days = [0, 7, 14, 21]
    weeks = ['1st', '2nd', '3rd', '4th',]
    weekly_growth = pandas.DataFrame(columns=weeks, dtype=int)

    for day, week in zip(days, weeks):
        growth = means.loc[day + 7] - means.loc[day]

        weekly_growth[week] = growth

    weekly_growth['total'] = weekly_growth.groupby(weekly_growth.index).cumsum()
    weekly_growth = weekly_growth.round(0)

    return weekly_growth
