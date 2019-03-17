import pandas
from matplotlib import pyplot

from stats import get_stats
from growth import get_weekly_growth
from daily_ttest import get_daily_ttest
from graphs import make_graphs
from growth_table import make_growth_table



input_file = "all_tests.xlsx"

TESTS = ['MBC', 'MBN', 'DOC', 'HWE-S', 'ERG', 'AS']
NUMBERS = range(1, len(TESTS)+1)
for test, number in zip(TESTS, NUMBERS):
    # input data into DataFrame
    raw_data = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                     sheet_name=test,
                                     na_values=["-", " "]).rename_axis("days")
    raw_data.columns.rename(["soil", "treatment", "replicate"],
                            level=None, inplace=True)
    raw_data.columns.set_levels(["c", "t"], level=1, inplace=True)

    #get statistics and parameters
    means, means_stde, treatment_effect = get_stats(raw_data)
    daily_ttest = get_daily_ttest(raw_data)

    #visualize
    figures = make_graphs(means, treatment_effect, means_stde, number, test)
    figures.savefig("%s_figuers.png" %test, bbox_inches='tight', pad_inches=2)
    pyplot.clf()

    if len(means.index) > 3:
        weekly_growth = get_weekly_growth(means)
        tables = make_growth_table(weekly_growth, number, test)
        tables.savefig("%s_tables.png" %test, bbox_inches='tight')

    if len
