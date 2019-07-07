from matplotlib import pyplot             # todo solve: running visualize.py with all data sets raises an error

from raw_data import get_setup_arguments, get_raw_data, get_multi_sets
from stats import get_stats, get_carbon_stats
from plot import plot_dynamics, plot_all_parameters, plot_c_to_n
# from model_dynamics import plot_model
from helpers import get_week_ends
# from Ttest import get_daily_Ttest
# from growth import get_weekly_growth, tabulate_growth


# set pyplot parameters
pyplot.rc('savefig', bbox='tight', pad_inches=1.5)

# input & output locations
INPUT_FILE = "all_tests.xlsx"
OUTPUT_DIRECTORY = "incubation_figures"

# setup
setup_arguments = get_setup_arguments()
DATA_SETS_NAMES = setup_arguments.sets
NUMBERS = setup_arguments.numbers

# SOILS = ['ORG', 'MIN', 'UNC']

# plot dynamics of each soil parameter as a seperate graph
for set_name, number in zip(DATA_SETS_NAMES, NUMBERS):

    # input data into DataFrame
    raw_data = get_raw_data(set_name)

    week_ends = get_week_ends(raw_data)

    # get statistics
    BasicStats = get_stats(raw_data)

    # data to plot
    difference = BasicStats.difference
    # means = BasicStats.means
    # means_SE = BasicStats.means_SE
    # MRE = BasicStats.MRE
    # MRE_SD = BasicStats.MRE_SD
    # MRE_SE = BasicStats.MRE_SE
    # control = BasicStats.control
    # control_SE = BasicStats.control_SE
    # normalized = BasicStats.normalized_diff

    microbial_c_to_n = get_carbon_stats()

    # plot dynamics
    treatment_figure = plot_dynamics(MRE, MRE_SE, MRE_SD, number, set_name, normalized=difference)
    treatment_figure.savefig("./%s/%s_model.png" % (OUTPUT_DIRECTORY, set_name))
    pyplot.cla()

    # if set_name == 'RESP':
    #     model_figure = plot_model(difference)
    #     model_figure.savefig('./%s/RESP_model_3_weeks.png' % OUTPUT_DIRECTORY)

    # # plot weekedns dynamics
    # treatment_figure = plot_dynamics(MRE.loc[week_ends, :], MRE_SE.loc[week_ends, :],
    #                                  MRE_SD.loc[week_ends, :], number, set_name,
    #                                  normalized=normalized.loc[week_ends, :])
    #
    # treatment_figure.savefig("./%s/%s_model.png" % (OUTPUT_DIRECTORY, set_name))
    # pyplot.cla()

# # plot baseline
# raw_data_sets = get_multi_sets(SETS_NAMES)
# soil_properties_figure = plot_all_parameters(raw_data_sets)
# soil_properties_figure.savefig('./%s/baseline.png' % OUTPUT_DIRECTORY)

# # plot C to N ratio
# c_to_n = get_carbon_stats()
# carbon_figure = plot_c_to_n(c_to_n)
# carbon_figure.savefig('./%s/C_to_N.png' %OUTPUT_DIRECTORY)







# MRE = MRE.loc[get_week_ends(MRE)] if set_name == 'RESP' else MRE
# MRE_SE = MRE_SE.loc[get_week_ends(MRE_SE)] if set_name == 'RESP' else MRE_SE
# normalized = normalized.loc[get_week_ends(normalized)] if set_name == 'RESP' else normalized

# # plot control
#     control_means_fig = plot_control(means, means_SE, set_name, number)
#     control_means_fig.savefig('./%s/control_%s.png' %(OUTPUT_DIRECTORY,set_name))
#     pyplot.cla()

# # plot ttest table
#     daily_ttest = get_daily_Ttest(raw_data)
#     ttest_table = tabulate_daily_Ttest(daily_ttest, set_name)
#     ttest_table.savefig("./%s/%s_Ttest.png" %(OUTPUT_DIRECTORY,set_name), bbox_inches='tight')
#     pyplot.cla()

# # plot weekly growth table
#     if test != 'RESP':
#         weekly_growth = get_weekly_growth(means)
#         growth_table = tabulate_growth(weekly_growth, number, set_name)
#         growth_table.savefig("./%s/%s_growth.png" %(OUTPUT_DIRECTORY,set_name) bbox_inches='tight')
#         pyplot.clf()
