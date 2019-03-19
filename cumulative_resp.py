import pandas


input_file = "all_tests.xlsx"

# input data into DataFrame
raw_data = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                 sheet_name='RESP',
                                 na_values=["-", " "]).rename_axis("days")
raw_data.columns.rename(["soil", "treatment", "replicate"],
                        level=None, inplace=True)
raw_data.columns.set_levels(["c", "t"], level=1, inplace=True)

groupby_soil_treatment = raw_data.groupby(level=[0, 1], axis=1)

means = groupby_soil_treatment.mean()  # means of 4 replicates

