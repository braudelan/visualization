import argparse

import pandas
from matplotlib import pyplot

from stats import get_stats
from growth import get_weekly_growth
from daily_ttest import get_daily_ttest
from graphs import make_graphs
from growth_table import make_growth_table

parser = argparse.ArgumentParser()
parser.add_argument("test",type=str)
parser.add_argument("figure_number", type=int)
parser.add_argument("table_number", type=int)

argv = parser.parse_args()

input_file = "all_tests.xlsx"

# input data into DataFrame
raw_data = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                 sheet_name=argv.test,
                                 na_values=["-", " "]).rename_axis("days")
raw_data.columns.rename(["soil", "treatment", "replicate"],
                        level=None, inplace=True)
raw_data.columns.set_levels(["c", "t"], level=1, inplace=True)

#get statistics and parameters
means, means_stde, treatment_effect = get_stats(raw_data, argv)
daily_ttest = get_daily_ttest(raw_data)
weekly_growth = get_weekly_growth(means)

#visualize
figures = make_graphs(means, treatment_effect, means_stde, argv)
figures.savefig("%s_figuers.png" %argv.test, bbox_inches='tight', pad_inches=2)
pyplot.clf()

tables = make_growth_table(weekly_growth, argv)
tables.savefig("%s_tables.png" %argv.test, bbox_inches='tight')


