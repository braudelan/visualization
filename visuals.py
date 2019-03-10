import argparse

from matplotlib import pyplot

from get_stats import get_stats
from graphs import visualize
from specifics import growth
from tables import make_tables

parser = argparse.ArgumentParser()
parser.add_argument("test",type=str)
parser.add_argument("figure_number", type=int)
parser.add_argument("table_number", type=int)

argv = parser.parse_args()

input_file = "all_tests.xlsx"

means, treatment_effect, stde_means, stde_effect, daily_ttest = get_stats(input_file, argv)
weekly_growth = growth(means)

figures = visualize(means, treatment_effect, stde_means, stde_effect, argv)
figures.savefig("%s_figuers.png" %argv.test, bbox_inches='tight', pad_inches=2)
pyplot.clf()

tables = make_tables(weekly_growth, argv)
tables.savefig("%s_tables.png" %argv.test, bbox_inches='tight')


