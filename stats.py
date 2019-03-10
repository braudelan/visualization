import pandas

def get_stats(raw_data, argv):

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

    # standard error of normalized means
    # control_stde_sqrd = (means_stde ** 2).xs("c", axis=1, level=1)  # control stnd error values squared
    # MRE_stde_sqrd = (means_stde ** 2).xs("t", axis=1, level=1)  # treatment stnd error values squared
    # stde_effect = ((control_stde_sqrd + MRE_stde_sqrd) ** 0.5).iloc[1:5, :]  # stnd error of treatment effect

    # test sgnificance between soils for every sampling day

    return means, means_stde, treatment_effect