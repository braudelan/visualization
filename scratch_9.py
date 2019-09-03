from raw_data import get_setup_arguments, get_raw_data
from stats import get_stats, get_normalized
from growth import get_weekly_growth, tabulate_growth
from helpers import Constants

OUTPUT_FOLDER =Constants.output_folder

setup_args = get_setup_arguments()

data_sets_names = setup_args.sets
enumerated = enumerate(data_sets_names)

for name, number in zip(data_sets_names, enumerated):

    raw = get_raw_data(name)
    stats = get_stats(raw, 't')
    normelized_stats = get_normalized(raw)
    normalized_means = normelized_stats.means
    normalized_stde = normelized_stats.stde
    weekly_growth_norm = get_weekly_growth(normalized_means, normalized_stde)

    growth_table = tabulate_growth(weekly_growth_norm, name, number)
    growth_table.savefig('%s/%s_weekly_growth.png' %(OUTPUT_FOLDER, name))