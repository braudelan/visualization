import argparse

import pandas
from scipy.stats import ttest_ind
import matplotlib
from matplotlib import pyplot
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
# import seaborn

# from get_stats import get_stats
# from graphs import visualize
# from tables import make_tables
# from specifics import growth

# seaborn.set()

parser = argparse.ArgumentParser()
parser.add_argument("test",type=str)
parser.add_argument("figure_number", type=int)
parser.add_argument("table_number", type=int)

argv = parser.parse_args()

input_file = "all_tests.xlsx"

dataframe = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                              sheet_name=argv.test,
                              na_values=["-", " "]).rename_axis("days")
dataframe.columns.rename(["soil", "treatment", "replicate"],
                         level=None, inplace=True)
dataframe.columns.set_levels(["c", "t"], level=1, inplace=True)

# means
groupby_soil_treatment = dataframe.groupby(level=[0, 1], axis=1)  # group 4 replicates from every soil-treatment pair
means = groupby_soil_treatment.mean()  # means of 4 replicates
#    treatment_means = means.xs("t",axis=1,level=1)
# standard error of means
stde_means = groupby_soil_treatment.sem()  # stnd error of means

# treatment means normalized to control
diff_of_means = means.diff(periods=1, axis=1)  # substracting over columns index, from right to left
treatment_effect = diff_of_means.xs("t", axis=1,
                                    level=1)  # slicing out from diff_of_means the unwanted results of control minus treatment
# standard error of normalized means
control_stde_sqrd = (stde_means ** 2).xs("c", axis=1, level=1)  # control stnd error values squared
MRE_stde_sqrd = (stde_means ** 2).xs("t", axis=1, level=1)  # treatment stnd error values squared
stde_effect = ((control_stde_sqrd + MRE_stde_sqrd) ** 0.5).iloc[1:5, :]  # stnd error of treatment effect

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


majorLocator = MultipleLocator(7)
minorLocator = MultipleLocator(1)
# minorLocator = AutoMinorLocator()



stde_treatment_means = stde_means.xs("t", axis=1, level=1)

args = (argv.figure_number, argv.test)

matplotlib.rcParams['legend.facecolor'] = 'azure'
matplotlib.rcParams['legend.frameon'] = True

# grid_spec = GridSpec(2, 2)

title_text = r'$\bf{Figure %s.}$ means of %s across 28 days of incubation. (a)all soils, ' \
             r'(b)treated soils only (c)normalized to control' % args
ylabel_text = r'$Biomass-C\ \slash\ mg \ast kg\ soil^{-1}$'
xlabel_text = r'$Time\ \slash\ days$'
symbol_fontdic = {'weight': 'bold',
                  'size': 18,
                  }

figure = pyplot.figure(1, figsize=(15, 20))
figure.tight_layout()
figure.subplots_adjust(hspace=0.2)
figure.text(0.12, 0.01, title_text, fontsize=16)
figure.text(0, 0.5, ylabel_text, fontsize=16, rotation=90, va='center')
figure.text(0.5, 0.04, xlabel_text, fontsize=16, ha='center')

means_axes = figure.add_subplot(311)
means.plot(
    ax=means_axes,
    xlim=(0, 30),
    yerr=stde_means,
)
means_axes.text(0.07, 0.85, "a", transform=means_axes.transAxes, fontdict=symbol_fontdic)
means_axes.xaxis.set_major_locator(majorLocator)
means_axes.xaxis.set_minor_locator(minorLocator)

MRE_means_axes = figure.add_subplot(312)
MRE_means_axes.text(0.07, 0.85, "b", transform=MRE_means_axes.transAxes, fontdict=symbol_fontdic)

effect_axes = figure.add_subplot(313)
effect_axes.text(0.07, 0.85, "c", transform=effect_axes.transAxes, fontdict=symbol_fontdic)


means.xs("t", axis=1, level=1).plot(
                                    kind="bar",
                                    ax=MRE_means_axes,
                                    xticks=range(0, 30, 7),
                                    xlim=(0, 30),
                                    yerr=stde_treatment_means,
                                   )

treatment_effect.plot(
                      kind="bar",
                      ax=effect_axes,
                      xticks=list(means.index[1:]),
                      yerr=stde_effect,
                     )
