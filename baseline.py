import pandas

from raw_data import get_raw_data,\
    get_ergosterol_to_biomass,\
    get_raw_MBC_to_MBN,\
    get_raw_TOC_TN,\
    get_setup_arguments
from significance import get_significance_booleans, annotate
from helpers import get_week_ends, round_column_data, DataFrame_to_image, Constants

TOP_OUTPUT_DIRECTORY = Constants.output_directory
OUTPUT_DIRECTORY = TOP_OUTPUT_DIRECTORY + '/baseline/'

DATA_SETS_NAMES: list = get_setup_arguments().sets
DATA_SETS_NAMES.extend(['TOC_TN', 'MBC_MBN'])
TABLE_RENDERING_STRING = Constants.table_css

def get_raw_baseline(raw_data): # todo find a better name for this function
    '''take raw data and rearrange it for baseline computations '''

    week_ends = get_week_ends(raw_data) # get the index of week ends sampling days
    if 'treatment' in raw_data.columns.names:
        raw_data = raw_data['c'] # slice out treatment data
    raw_control_week_ends = raw_data.loc[week_ends] # slice out any rows that are not week ends
    raw_baseline = raw_control_week_ends.stack().reset_index(drop=True) # stack and revert to default index

    return raw_baseline

def get_baseline_stats(data_sets_names):

    data_sets_means = []
    data_sets_significances = []
    for data_set_name in data_sets_names:

        raw_data = (
            get_ergosterol_to_biomass() if data_set_name == 'ERG' else
            get_raw_MBC_to_MBN() if data_set_name == 'MBC_MBN' else
            get_raw_TOC_TN() if data_set_name == 'TOC_TN' else
            get_raw_data(data_set_name)
        )

        raw_baseline = get_raw_baseline(raw_data)

        # means
        data_set_means = raw_baseline.mean()
        data_set_means.name = data_set_name
        
        # significance between means
        raw_baseline_stacked = raw_baseline.stack().droplevel(0)
        booleans = get_significance_booleans(raw_baseline_stacked)
        significance_letters = annotate(booleans)
        significance_letters.name = data_set_name

        # append
        data_sets_means.append(data_set_means)
        data_sets_significances.append(significance_letters)

    significance_of_means = pandas.concat(data_sets_significances, axis='columns')
    means = pandas.concat(data_sets_means, axis='columns')


    means = means.apply(round_column_data)

    return means, significance_of_means

if __name__ == '__main__':

    baseline_stats = get_baseline_stats(DATA_SETS_NAMES)
    # means = baseline_stats[0]
    # significance = baseline_stats[1]
    #
    # MEANS_OUTPUT_FILE = f'{OUTPUT_DIRECTORY}means'
    # SIGNIFICANCE_OUTPUT_FILE = f'{OUTPUT_DIRECTORY}significance'
    # DataFrame_to_image(means, TABLE_RENDERING_STRING,
    #                                     MEANS_OUTPUT_FILE)
    # DataFrame_to_image(significance, TABLE_RENDERING_STRING,
    #                                     SIGNIFICANCE_OUTPUT_FILE)