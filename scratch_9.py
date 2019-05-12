import pandas
from matplotlib import pyplot

from raw_data import get_keys
from raw_data import get_raw_data
from stats    import get_stats
from Ttest    import get_daily_Ttest
# from baseline     import get_baseline


# get tab names to import from file
INPUT_FILE = "all_tests.xlsx"

keys = get_keys().specific[0]
raw_data = get_raw_data(keys)
#
means, normalized, means_stde, diff = get_stats(raw_data)
#
def color_map_generator(dataframe):
    colors = ['r', 'b', 'g']
    soils = ['COM', 'MIN', 'UNC']
    soils_colors = dict(zip(soils, colors))
    color_map = [soils_colors.get(x[1]) for x in dataframe.columns]

    return color_map

def line_styler(dataframe):
    MRE_line_style     = '-'
    control_line_style = '--'
    line_style_dict    = {'t': MRE_line_style, 'c': control_line_style}
    line_style_map     = [line_style_dict.get(x[0]) for x in dataframe.columns]

    return line_style_map

style= line_styler(means)
color = color_map_generator(means)