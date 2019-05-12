import pandas
from matplotlib import pyplot
from matplotlib.ticker import MultipleLocator

from stats import get_stats

# variabels
input_file = "all_tests.xlsx"
TESTS = ['MBC', 'RESP']

#pyplot paramateres
majorLocator = MultipleLocator(7)
minorLocator = MultipleLocator(1)

pyplot.rc('legend', facecolor='inherit', frameon=False, markerscale=1.5)
pyplot.rc('font', size=18)
pyplot.rc('lines', linewidth=3)

symbol_text_params = {'weight': 'bold',
                      'size': 26,
                      }
labels_text_params = {'size': 19}

# text
title_text = 'metabolic quotient. (a) instantaneous $qCO_{2}$ across 3 weeks of incubation, normalized to a an\n'
'average value of all control samples from all three soils, throughout the incubation period,\n'
'excluding iregular results on days 0 and 7,(b) average $\_{q}CO_{2}$ at three time periods\n '
'corresponding to each pulse of MRE applied'

                                # get the data

stats = {}
for test in TESTS:
# input data into DataFrame
    raw_data = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                     sheet_name=test,
                                     na_values=["-", " "]).rename_axis("days")
    raw_data.columns.rename(["soil", "treatment", "replicate"],
                            level=None, inplace=True)
    raw_data.columns.set_levels(["c", "t"], level='treatment', inplace=True)

#get statistics and parameters
    means, means_stde, normalized = get_stats(raw_data)

    stats[test] = means

# instantaneous qCO2
MBC_means  = stats['MBC']
RESP_means = stats['RESP']
qCO2_inst  = RESP_means / MBC_means
qCO2_inst  = qCO2_inst.drop(8)

# baseline instantaneous qCO2
control  = qCO2_inst.xs('c', level='treatment', axis=1)
droped   = control.drop(labels=[0,7])
baseline = droped.mean().mean()

# instantaneous qCO2 normalized to baseline
normalized_qCO2 = qCO2_inst / baseline

# average qCO2
qCO2_average = pandas.read_excel(input_file, index_col=0, header=0, sheet_name='qCO2')

                                 # plotting

#create and adjut figure
figure_4 = pyplot.figure(1, figsize=(16, 18))
figure_4.tight_layout()
figure_4.subplots_adjust(hspace=0.3)
figure_4.text(0.1, 0.0, title_text, fontsize=23)

# plot instantaneous qCO2
inst_axes = figure_4.add_subplot(211)

normalized_qCO2.plot(ax=inst_axes,
                       xlim=(0, 22)
                      )
inst_axes.xaxis.set_major_locator(majorLocator)
inst_axes.xaxis.set_minor_locator(minorLocator)

# plot average qCO2
average_axes = figure_4.add_subplot(212)


qCO2_average.plot(ax=average_axes,
                  kind='bar'
                  )

xtick_label_rotate = pyplot.xticks(rotation=45)

                                 # save figure

figure_4.savefig("./misc_figures/qCO2.png", bbox_inches='tight', pad_inches=2)
pyplot.clf()

# todo work on title