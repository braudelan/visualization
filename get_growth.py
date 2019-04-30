import pandas
from pandas import DataFrame

def get_weekly_growth(means):

    week_ends = [x for x in means.index if x % 7 == 0 or x == 0 ]  # list day 0 and end of every week

    if len(week_ends) == 5:
        weeks = ['1st', '2nd', '3rd', '4th']
    else:
        weeks = ['1st', '2nd', '3rd']

    weekly_growth = pandas.DataFrame(columns=weeks, dtype=int)

    for day, week in zip(week_ends[:-1], weeks):

        growth = means.loc[day + 7] - means.loc[day]
        weekly_growth[week] = growth

    weekly_growth['total'] = weekly_growth.sum(axis=1)
    weekly_growth = weekly_growth.round(0)

    return weekly_growth