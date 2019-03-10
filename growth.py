import pandas
from pandas import DataFrame

def get_weekly_growth(means: DataFrame):
    days = [0, 7, 14, 21]
    week = 1
    weekly_growth = pandas.DataFrame(columns=['1st', '2nd', '3rd', '4th'], dtype=int)

    for day in days:
        growth = means.loc[day+7] - means.loc[day]

        weekly_growth[week] = growth
        week += 1

    weekly_growth = weekly_growth.round(0)

    return weekly_growth
