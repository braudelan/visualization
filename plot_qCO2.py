import pandas
from matplotlib import pyplot

from stats import get_stats

input_file = "all_tests.xlsx"

title_text = r' metabolic quotient. (a) instantaneous, (b) average '

pyplot.rc('legend', facecolor='inherit', frameon=False, markerscale=1.5)
pyplot.rc('font', size=18)
pyplot.rc('lines', linewidth=3)

symbol_text_params = {'weight': 'bold',
                      'size': 26,
                      }
labels_text_params = {'size': 19}

# get statistics
TESTS = ['MBC', 'RESP']
stats = {}

for test in TESTS:

    # input data into DataFrame
    raw_data = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                     sheet_name=test,
                                     na_values=["-", " "]).rename_axis("days")
    raw_data.columns.rename(["soil", "treatment", "replicate"],
                            level=None, inplace=True)
    raw_data.columns.set_levels(["c", "t"], level=1, inplace=True)

    #get statistics and parameters
    means, means_stde, treatment_effect = get_stats(raw_data)

    stats[test] = means


# instantaneous qCO2
MBC_means = stats['MBC']
RESP_means = stats['RESP']
qCO2_inst = RESP_means / MBC_means

# average qCO2
qCO2_average = pandas.read_excel(input_file, index_col=0, header=0, sheet_name='qCO2')

# plotting
figure = pyplot.figure(4, figsize=(10,10))
figure.tight_layout()
figure.subplots_adjust(wspace=0.5)
figure.text(0.05, 0.01, title_text, fontsize=20)

inst_axes = figure.add_subplot(121)

qCO2_inst.plot(ax=inst_axes,
               kind='bar'
               )
average_axes = figure.add_subplot(122)

qCO2_average.plot(ax=average_axes,
                  kind='bar'
                  )
# save figure
figure.savefig("./figures/qCO2.png", bbox_inches='tight', pad_inches=2)
pyplot.clf()