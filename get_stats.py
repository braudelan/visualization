import pandas

def get_stats(raw_data):

    # means
    groupby_soil_treatment = raw_data.groupby(level=[0, 1],axis=1)  # group 4 replicates from every soil-treatment pair
    means                  = groupby_soil_treatment.mean()          # means of 4 replicates
    means_stde             = groupby_soil_treatment.sem()           # stnd error of means

    # means of control
    control    = means.xs('c', axis=1, level=1)

    #treatment effect
    substract  = means.diff(periods=1, axis=1)       # substracting across columns, right to left
    difference = substract.xs("t", axis=1, level=1)  # treatment - control
    normalized = difference / control * 100          # difference normalized to control (percent)


    return means, normalized, means_stde


