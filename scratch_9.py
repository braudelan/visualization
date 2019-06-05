from pandas import DataFrame
from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import MultipleLocator, NullLocator

from get_raw_data import get_setup_arguments
from get_raw_data import get_raw_data, get_multi_sets
from get_stats import get_stats, get_carbon_stats, get_baseline
from plot import plot_baseline
from Ttest import get_daily_Ttest

# arguments to specify which data sets to load from INPUT_FILE
setup_arguments = get_setup_arguments()

set_name = setup_arguments.sets[0]
number = setup_arguments.numbers[0]

raw_data = get_raw_data(set_name)
# figure = plot_baseline(raw_data)
#
stats = get_stats(raw_data)
means = stats.means
means_SE = stats.means_SE
MRE = stats.MRE
MRE_SE = stats.MRE_SE
normalized = stats.normalized_diff
control = stats.control

baseline = get_baseline(raw_data)
# c_to_n = get_carbon_stats()

def get_week_ends(dataframe):

    every_7th = dataframe.index.isin([0, 7, 14, 21, 28])

    return every_7th
#
# fig = pyplot.figure()
#
# ax_ratio = 0.2
# ax = fig.add_subplot(111)
#
# line_ORG = MRE['ORG'].plot()
# line_MIN = MRE['MIN'].plot()
#
# ax.set_aspect(1.0/ax.get_data_ratio()*ax_ratio)
#
# fig.savefig('./test_pyplot')

# def get_carbon_stats():
#     sets_names = ['MBC', 'MBN', 'RESP', 'DOC', 'HWE-S','TOC']
#     dataframes = get_multi_sets(sets_names)
#     stats_frames = {}
#     for set in sets_names:
#         raw = dataframes[set]
#         stats = get_stats(raw)
#         means = stats.means
#         means_SE = stats.means_SE
#         set_stats = {'means': means, 'means_SE': means_SE}
#         stats_frames[set] = set_stats
#
#     MBC = stats_frames['MBC']['means']
#     MBN = stats_frames['MBN']['means']
#     RESP = stats_frames['RESP']['means']
#     DOC = stats_frames['DOC']['means']
#     HWES = stats_frames['HWE-S']['means']
#     HWES_C = HWES / 4  # 40% C in glucose
#     C_to_N_ratio = MBC / MBN
#     soil_available_C = MBC + HWES_C + DOC
#     available_C_control = available_C.xs(key='c', level=0, axis=1)
#     available_C_MRE = available_C.xs(key='t', level=0, axis=1)
#     available_C_difference = available_C_MRE- available_C_control # todo plot available_c and available_C_difference
#
#     return soil_available_C, available_C_difference, C_to_N_ratio
#
#
#
# # MBC_raw = dataframes['MBC']
# MBN_raw = dataframes['MBN']
# MBC_stats = get_stats(MBC_raw)
# MBN_stats = get_stats(MBN_raw)

# means = stats_output.means
# means_SE = stats_output.means_SE
# normalized = stats_output.normalized_diff
# normalized_SE = stats_output.normal
# # raw_data.res
# # group raw_data by day
# # groupby_day   = raw_data.groupby('days')
# # by_day_groups = dict(list(groupby_day))
#
# by_day_Ttest = {}
#
# # pyplot parameters
#
# pyplot.style.use('seaborn-darkgrid')
#
# pyplot.rc('legend',
#           facecolor='inherit',
#           framealpha=0,
#           markerscale=1.5)
# pyplot.rc('font', size=19) # control text size when not defined locally
# pyplot.rc('lines', linewidth=3)
#
# symbol_text_params = {'weight': 'bold',
#                       'size': 26,
#                       }
#
#
# line_styles = densly_dashed, solid = ((0, (2, 1)), (0, ()))
#
# major_locator = MultipleLocator(7)  # major ticks locations
# minor_locator = MultipleLocator(1)  # minor ticks locations
#
#
# # local parameters
# normalized_SE = None
# num_data_points = len(means.index)    # number of sampling days
# excluded = normalized.iloc[1:, :]  # treatment effect without day 0
# for frame in [means, means_SE]:
#     frame.columns = frame.columns.map('_'.join)
#     frame.reset_index(inplace=True)
# normalized.reset_index(inplace=True)
# last_day = means['days'].iloc[-1]     # last sampling day
# every_seven = [0,7,14,21,28]
#
#
# # figure text
# title_text = r'$\bf{Figure %s.}$ means of %s across %s days of incubation. (a) all soils, ' \
#              r'(b) normalized to control' % (number, set_name, last_day)
#
# xlabel_text = r'$incubation\ time\ \slash\ days$'
#
# if set_name == 'RESP':
#     means_ylabel_text = r'$%s\ \slash\ mg\ CO_{2}-C\ \ast\ kg\ soil^{-1}\ \ast\ h^{-1} $' % set_name
# else:
#     means_ylabel_text = r'$%s\ \slash\ mg \ast kg\ soil^{-1}$' % set_name
#
# normalized_ylabel_text = r'$%s\ normalized\ \slash\ percent\ of\ control$' % set_name
#
#
# # create and adjut figure
# week_ends_figure = pyplot.figure(number, figsize=(25,15))
# week_ends_figure.tight_layout()
# week_ends_figure.subplots_adjust(hspace=0.3)
#
#
#
# # create all means axes and set parameters
# means_axes = week_ends_figure.add_subplot(211)
#
# means_axes.set_xlim((0,last_day))
# means_axes.xaxis.set_minor_locator(minor_locator)
# means_axes.xaxis.set_major_locator(major_locator)
# means_axes.tick_params(axis='x', which='minor', width=1, length=3)
# means_axes.text(0.03, 1.05, "a", transform=means_axes.transAxes, fontdict=symbol_text_params)  # symbol
# means_axes.set_ylabel(means_ylabel_text, labelpad=30)
# means_axes.set_xlabel('')
#
#
# # plot all means
# means_lines = plot_all_lines(means.loc[every_seven], means_SE.loc[every_seven], means_axes) # todo take out specific data points (MBC)
#                                                              #      insert markings for time points where
#                                                              #      MRE was applied
#
# # costumize all means legend
# list_lines = list(means_lines.items())
# lables = []
# handles = []
# for line in list_lines[3:]:
#     label = line[0][2:]
#     handel = line[1]
#     lables.append(label)
#     handles.append(handel)
# treatment_labels = ['MRE apllied', 'c']
# lables.extend(treatment_labels)
# treatment_handles = [Line2D([0], [0], linewidth=5, linestyle=solid, color='k'),
#                      Line2D([0], [0], linewidth=5, linestyle=densly_dashed, color='k')]
# handles.extend(treatment_handles)
# means_legend = means_axes.legend(handles, lables) # todo remove error bars from legend objects.


# create normalized axes and set parameters
# normalized_axes = week_ends_figure.add_subplot(212)
#
# normalized_axes.set_xlim((0, last_day))
# normalized_axes.xaxis.set_major_locator(major_locator)
# normalized_axes.xaxis.set_minor_locator(minor_locator)
# normalized_axes.set_ylabel(normalized_ylabel_text, labelpad=30)
# normalized_axes.set_xlabel(xlabel_text, labelpad=30)
# normalized_axes.tick_params(axis='x', which='minor', width=1,length=3)
# normalized_axes.text(0.03, 1.05, "b", transform=normalized_axes.transAxes, fontdict=symbol_text_params)
#
#
# # plot normalized
# normalized_lines = plot_all_lines(normalized.loc[every_seven], normalized_SE.loc[every_seven], normalized_axes)
#
# normalized_axes.legend()
#
# week_ends_figure.text(0, -0.4, title_text, fontsize=22, transform=normalized_axes.transAxes)












#
# # group by treatment (MRE\control)
# for daily_data in list(by_day_groups.items()):
#
#     day  = daily_data[0]
#     data = daily_data[1].T
#
#     groupby_treatment = data.groupby(level=[1])
#     treatment_groups  = dict(list(groupby_treatment))
#
#     Ttest_dict = {}
#
#     # group by soil and run Ttest
#     for group in treatment_groups.items():
#
#         treatment = group[0]
#         data      = group[1]
#
#         # groupby
#         groupby_soil = data.groupby(level=[0])
#         list_soils   = list(groupby_soil)
#
#         soil_a = list_soils[0]
#         soil_b = list_soils[1]
#         soil_c = list_soils[2]
#
#         label_ab = (treatment, (soil_a[0], soil_b[0]))
#         label_bc = (treatment, (soil_b[0], soil_c[0]))
#         label_ac = (treatment, (soil_a[0], soil_c[0]))
#
#         data_a = soil_a[1]
#         data_b = soil_b[1]
#         data_c = soil_c[1]
#
#         # Ttest
#         Ttest_ab = ttest_ind(data_a, data_b, equal_var='False', nan_policy='omit')
#         Ttest_bc = ttest_ind(data_b, data_c, equal_var='False', nan_policy='omit')
#         Ttest_ac = ttest_ind(data_a, data_c, equal_var='False', nan_policy='omit')
#
#         Ttest_dict[label_ab] = Ttest_ab[1]  # index [1] = p-value
#         Ttest_dict[label_bc] = Ttest_bc[1]
#         Ttest_dict[label_ac] = Ttest_ac[1]
#
#     by_day_Ttest[day] = Ttest_dict
#
# daily_Ttest = DataFrame.from_dict(by_day_Ttest)  # DataFrame
# daily_Ttest = daily_Ttest.round(get_round(daily_Ttest))
#
