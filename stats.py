
import argparse

import pandas


parser = argparse.ArgumentParser()
parser.add_argument("input",type=str)
argv = parser.parse_args()

file = "all_tests.xlsx"

dataframe = pandas.read_excel(file, index_col=0, header=[0,1,2],
                              sheet_name=argv.input,
                              na_values=["-", " "]).rename_axis("days")
dataframe.columns.rename(["soil","treatment","replicate"],
                         level=None, inplace=True)
dataframe.columns.set_levels(["control","MRE"],level=1, inplace=True)


groupby_soil_treatment = dataframe.groupby(level=[0,1], axis=1) # group 4 replicates from every soil-treatment pair
means = groupby_soil_treatment.mean() # means of 4 replicates
stde_means = groupby_soil_treatment.sem() # stnd error of means
diff_of_means = means.diff(periods=1,axis=1) # substracting over columns index, from right to left
treatment_effect =  diff_of_means.xs("MRE",axis=1,level=1)# slicing out from diff_of_means the unwanted results of control minus treatment
control_stde_sqrd = (stde_means**2).xs("control",axis=1,level=1) # control stnd error values squared
MRE_stde_sqrd = (stde_means**2).xs("MRE", axis=1,level=1) # treatment stnd error values squared
stde_effect = (control_stde_sqrd + MRE_stde_sqrd)**0.5 # stnd error of treatment effect
