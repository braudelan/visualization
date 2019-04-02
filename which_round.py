import pandas

def get_round(dataframe):

    number = dataframe.min().min()
    bounds = h, m, l = (10, 0.1, 0.01)

    if number >= h:
        return 0

    if number < h and number >= m:
        return 2

    elif number < m  and number >= l:
        return 3

    else:
        return 4