import pandas

def get_stats(input_file, argv):
    """

    :rtype: DataFrame
    """
    dataframe = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                  sheet_name=argv.test,
                                  na_values=["-", " "]).rename_axis("days")
    dataframe.columns.rename(["soil", "treatment", "replicate"],
                             level=None, inplace=True)
    dataframe.columns.set_levels(["c", "t"], level=1, inplace=True)

    # means
    groupby_soil_treatment = dataframe.groupby(level=[0, 1],
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
    Ttest_dic = {}
    for day in list(dataframe.index):
        data_MRE = dataframe.T.xs("t", level=1)

        COM_MIN = list(ttest_ind(data_MRE.xs("COM", level=0).loc[:, day],
                                 data_MRE.xs("MIN", level=0).loc[:, day],
                                 equal_var=False, nan_policy='omit')
                       )
        COM_UND = list(ttest_ind(data_MRE.xs("COM", level=0).loc[:, day],
                                 data_MRE.xs("UND", level=0).loc[:, day],
                                 equal_var=False, nan_policy='omit')
                       )
        MIN_UND = list(ttest_ind(data_MRE.xs("MIN", level=0).loc[:, day],
                                 data_MRE.xs("UND", level=0).loc[:, day],
                                 equal_var=False, nan_policy='omit')
                       )

        all_pairs = {"COM-MIN": COM_MIN[1],
                     "COM-UND": COM_UND[1],
                     "MIN-UND": MIN_UND[1]
                     }
        Ttest_dic[day] = all_pairs

    daily_ttest = pandas.DataFrame.from_dict(Ttest_dic).T
    daily_ttest.rename_axis("days", inplace=True)

    return means, means_stde, treatment_effect, daily_ttest