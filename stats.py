import pandas

def get_stats(raw_data):

    # means
    groupby_soil_treatment = raw_data.groupby(level=[0, 1],
                                              axis=1)  # group 4 replicates from every soil-treatment pair
    means = groupby_soil_treatment.mean()  # means of 4 replicates

    # standard error of means
    means_stde = groupby_soil_treatment.sem()  # stnd error of means

    #treatment effect
    diff = means.diff(periods=1, axis=1)  # substracting over columns index, from right to left
    treatment_diff = diff.xs("t", axis=1, level=1)  # slicing out from diff the unwanted results of control minus treatment
    treatment_effect = treatment_diff / means.xs('c', axis=1, level=1) * 100

    return means, means_stde, treatment_effect


