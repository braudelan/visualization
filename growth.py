import pandas

def growth(means):
    treatment_means= means.xs("t", axis=1, level=1)
    days = [0,7,14]
    week = 1
    weekly_growth = pandas.DataFrame(columns=[1, 2, 3], dtype=int)

    for day in days:
        growth = treatment_means.loc[day+7] - treatment_means.loc[day]

        weekly_growth[week] = growth
        week += 1

    return weekly_growth.round(0)
