''' compute basic statistics from raw data.'''
from collections import namedtuple

import pandas
from pandas import DataFrame

import data.significance as significance
import data.raw_data as raw_data
from data.helpers import Stats

def get_stats(raw_data: DataFrame, treatment: str=None) -> namedtuple:
    '''
    calculate basic statistics for a given data sets.

    :returns
    namedtuple: the different statistics calculated

    '''

    # means
    levels =['treatment', 'soil'] if treatment else 'soil'
    groupby_soil_treatment = raw_data.groupby(level=levels, axis=1)

    means = groupby_soil_treatment.mean()  # means of 4 replicates
    stde = groupby_soil_treatment.sem()  # std error

    # drop control or MRE if the treatment argument is passed
    if treatment:
        means = means[treatment]
        stde = stde[treatment]

    # means.treatment_label = treatment
    # control = means.xs('c', level=0, axis=1)
    # control_SE = means_SE.xs('c', level=0, axis=1)
    # control_SD = means_SD.xs('c', level=0, axis=1)
    # control.treatment_label = 'c'

    # treatment effect
    # difference = MRE - control   # treatment - control
    # normalized_diff = difference / control * 100  # difference normalized to control (percent)

    return Stats(
        means=means,
        stde=stde,
        # difference=difference,
        # normalized_diff=normalized_diffget
    )


def get_multiple_stats(raw_data_sets):
    '''

    :param raw_data_sets: dict
    keys are data sets names.
    values are DataFrame s with raw data

    :return: multiple_stats: dict
    keys are data sets names.
    values are a Stats instance with means and stnd erros
    '''


    multiple_stats = {}
    for name, raw_data in raw_data_sets.items():
        stats = get_stats(raw_data)
        multiple_stats[name] = stats

    return multiple_stats


def get_baseline_stats(keys):
    '''
    get raw baseline values of multiple parameters.

    :param keys: list
    parameters to be included.

    :return:
    '''

    # list of raw data sets (for inspection)
    raw_sets = []

    # lists to store statistics from every data_set
    data_sets_means = []
    data_sets_err = []
    significance_list = []
    for key in keys:

        # get the data
        raw = raw_data.get_raw_data(key)['c']

        # exclude week days
        week_ends = [day for day in raw.index if day in [0, 7, 14, 21, 28]]
        raw = raw.loc[week_ends]

        # transpose, stack, drop irrelevant levels
        transposed = raw.T
        stacked = transposed.stack()
        raw = stacked.droplevel(['replicate', 'days'])

        # rename resulting Series
        raw.name = key

        # append to raw_sets list
        raw_sets.append(raw)

        # compute statistics
        group_by_soil = raw.groupby(raw.index)
        means = group_by_soil.mean()
        std_err = group_by_soil.sem()

        # compute significance and rename
        booleans = significance.get_significance_booleans(raw)
        annotations = significance.annotate(booleans)
        annotations.name = key

        # append statistics to lists
        data_sets_means.append(means)
        data_sets_err.append(std_err)
        significance_list.append(annotations)

    # combine stats from all data sets into Dataframe
    baseline_means = pandas.concat(data_sets_means, axis=1)
    baseline_std_errors = pandas.concat(data_sets_err, axis=1)
    baseline_significance = pandas.concat(significance_list, axis=1)

    return Stats(means=baseline_means,stde=baseline_std_errors,),\
           baseline_significance,\
           raw_sets

if __name__ == '__main__':
    keys = ['TOC', 'WEOC', 'HWES', 'AS', 'MBC', 'Resp', 'Erg']
    means, errors, significance, raw_sets = get_baseline_stats(keys)

# def normalize_to_TOC(raw)-> dict:
#     '''normalize a given carbon fraction to TOC '''
#
#     # get baseline value for TOC
#     raw_TOC = get_raw_data('TOC')
#     raw_TOC_control = raw_TOC.loc[:, 'c']
#     exclude_day14 = raw_TOC_control.drop(index=14)
#     stacked = exclude_day14.stack() # unreliable results on day 14
#     TOC_means = stacked.mean() * 1000 # multiply by 1000 to1 switch from % of soil weight to mg/kg
#     TOC_stde = stacked.sem() * 1000
#     TOC_relative_stde = TOC_stde / TOC_means
#
#     # get carbon fraction statistics
#     treatment_stats = get_stats(raw, 't')
#     control_stats = get_stats(raw, 'c')
#     normalized_to_baseline = normalize_to_baseline(raw)
#
#     catrgories = {'treatment': treatment_stats,
#                   'control': control_stats,
#                   'normalized': normalized_to_baseline
#                   }
#     TOC_normalized_by_category = {}
#     for category in catrgories.keys():
#         category_stats = catrgories[category]
#         means = category_stats.means
#         stde = category_stats.stde
#         relative_stde = stde / means
#
#         divided_by_TOC = means.copy()
#         relative_stde_of_quotient = relative_stde.copy()
#         for soil in SOILS:
#             soil_means = means[soil]
#             TOC_soil_mean = TOC_means[soil]
#             divided_by_TOC[soil] = soil_means / TOC_soil_mean
#             soil_stde = relative_stde[soil]
#             TOC_soil_relative_stde = TOC_relative_stde[soil]
#             relative_stde_of_quotient[soil] = (soil_stde ** 2
#                                                + TOC_soil_relative_stde ** 2) ** 0.5
#
#         percent_of_TOC = divided_by_TOC * 100
#         percent_stde = relative_stde_of_quotient * 100
#
#         stats = Stats(means=percent_of_TOC,
#               stde=percent_stde,
#               stdv=None)
#         TOC_normalized_by_category[category] = stats
#
#     return TOC_normalized_by_category

#
#
#
# def normalize_to_control(raw_data):
#     '''normalize raw data of treatment samples to corresponding control samples.
#
#     each treatment replicate is normalized to the average of 4 (or less) corresponding
#      control replicates.
#
#     '''
#
#     raw_t = raw_data.loc[:, ('t', SOILS)] # MRE treatment
#     raw_c = raw_data.loc[:, ('c', SOILS)] # control
#
#     control_means = get_stats(raw_c, 'c').means # shape ->(10,3)
#
#     # empty dataframe with the same shape and indexes as raw_t
#     control_means_shaped = DataFrame().reindex_like(raw_t) # shape ->(10,12)
#
#     # fill above shaped empty dataframe with the mean value for every set of replicates
#     for row in control_means_shaped.index:
#         for column in control_means_shaped.columns:
#             soil = column[0]
#             control_means_shaped.loc[row, column] = control_means.loc[row, soil]
#
#     normalized = raw_t / control_means_shaped * 100
#     normalized = get_stats(normalized, 't')
#     replace_negative = lambda x: None if (x < 0) else x
#     normalized_means = normalized.means.applymap(replace_negative)
#     normalized_stde = normalized.stde.applymap(replace_negative)
#
#     return Stats(
#         means=normalized_means,
#         stde=normalized_stde,
#         stdv=None
#     )
#
#
# def normalize_to_baseline(raw_data):
#     '''represent the means of each soil as a percentage of corresponding baseline value '''
#
#     # get baseline stats
#     baseline_stats = get_baseline(raw_data)
#     baseline_means = baseline_stats.means
#     baseline_stde = baseline_stats.stde
#
#     # get treatment stats
#     treatment_stats = get_stats(raw_data, 't')
#     treatment_means: DataFrame = treatment_stats.means
#     treatment_stde = treatment_stats.stde
#
#     # setup empty dataframes for normalized stats
#     index = treatment_means.index
#     columns = treatment_means.columns
#     normalized = DataFrame(index=index, columns=columns)
#     normalized_stde = DataFrame(index=index, columns=columns)
#
#     for soil in SOILS:
#
#         treatment_data = treatment_means[soil]
#         treatment_error = treatment_stde[soil]
#         treatment_relative_error = treatment_error / treatment_data  #relative stnd error
#
#         baseline = baseline_means[soil]
#         baseline_error = baseline_stde[soil]
#         baseline_relative_error = baseline_error / baseline #relative stnd error
#
#         divided_by_baseline = treatment_data / baseline #data normalized to baseline
#         normalized_relative_error = (treatment_relative_error**2 +
#                                      baseline_relative_error**2)**0.5 # formula for stnd error of a quotient
#         normalized[soil] = divided_by_baseline * 100
#         normalized_stde[soil] = normalized_relative_error * divided_by_baseline * 100
#
#     return Stats(
#         means=normalized,
#         stde=normalized_stde,
#         stdv=None
#     )
#
#
# def normalize_to_initial(raw_data):
#     '''represent the means of each soil as a percentage of corresponding initial value '''
#
#     # get initial values
#     stats = get_stats(raw_data, 'c')
#     means = stats.means
#     stde = stats.stde
#     initial_values = means.loc[0] #means of day 0
#     initial_values_stde = stde.loc[0]
#
#     # get treatment stats
#     treatment_stats = get_stats(raw_data, 't')
#     treatment_means: DataFrame = treatment_stats.means
#     treatment_stde = treatment_stats.stde
#
#     # setup empty dataframes for normalized stats
#     index = treatment_means.index
#     columns = treatment_means.columns
#     normalized = DataFrame(index=index, columns=columns)
#     normalized_stde = DataFrame(index=index, columns=columns)
#
#     for soil in SOILS:
#
#         treatment_data = treatment_means[soil]
#         treatment_error = treatment_stde[soil]
#         treatment_relative_error = treatment_error / treatment_data #relative stnd error
#
#         initial = initial_values[soil]
#         initial_error = initial_values_stde[soil]
#         initial_relative_error = initial_error / initial
#
#         divided_by_initial = treatment_data / initial #data normalized to initial
#         normalized_relative_error = (treatment_relative_error**2 +
#                                      initial_relative_error**2)**0.5
#         normalized[soil] = divided_by_initial * 100
#         normalized_stde[soil] = normalized_relative_error * divided_by_initial * 100
#
#     return Stats(
#         means=normalized,
#         stde=normalized_stde,
#         stdv=None
#     )
#

