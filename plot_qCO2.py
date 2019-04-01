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
figure = pyplot.figure(4, figsize=(16,12))
figure.tight_layout()
figure.subplots_adjust(hspace=0.5)
figure.text(0.1, -0.1, title_text, fontsize=23)

# instantaneous qCO2
inst_axes = figure.add_subplot(211)

qCO2_inst.drop(8).plot(ax=inst_axes,
                      )
# average qCO2
average_axes = figure.add_subplot(212)


qCO2_average.plot(ax=average_axes,
                  kind='bar'
                  )

xtick_label_rotate = pyplot.xticks(rotation=45)

# save figure
figure.savefig("./figures/qCO2.png", bbox_inches='tight', pad_inches=2)
pyplot.clf()