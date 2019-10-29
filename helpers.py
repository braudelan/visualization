import os

import numpy
from pandas import DataFrame
import random
import imgkit


class Constants:

    groups = ['ORG', 'MIN', 'UNC']
    color_options = ('darkred', 'royalblue', 'dimgrey')
    colors =  dict(zip(groups, color_options))
    marker_options = ('*', 'o', 'd')
    markers =  dict(zip(groups, marker_options))
    line_style_labels = ('solid', 'broken', 'dotted')
    line_style_options = ('-', '-.', ':')
    line_styles = dict(zip(line_style_labels, line_style_options))
    treatment_labels = ['c', 't']
    level_labels = ["soil", "treatment", "replicate"]
    input_file_name = "all_tests.xlsx"
    output_folder = '/home/elan/Dropbox/research/figures'


def get_week_ends(dataframe):

    every_7th = dataframe.index.isin([0, 7, 14, 21, 28])

    return every_7th


def delay_factor(x, delay):
    ''' return a function alternating between 0 and 1 with delay.'''

    N_HARMONICS = 1000
    CYCLE = 28

    def bn(n):
        n = int(n)
        if (n % 2 != 0):
            return 2 / (pi * n)
        else:
            return 0

    # Wn
    def wn(n):
        wn = (2 * pi * n) / CYCLE
        return wn

    a0 = 0.5
    partialSums = a0
    for n in range(1, N_HARMONICS):
        partialSums = partialSums + bn(n) * sin(wn(n) * (x - delay))
    return partialSums


def replace_None(raw_data):

    TREATMENTS = Constants.treatment_labels
    SOILS = Constants.groups
    DAYS = raw_data.index

    for treatment in TREATMENTS:
        for soil in SOILS:
            for day in DAYS:
                daily_data = raw_data.loc[day, (treatment, soil)]
                daily_mean = daily_data.mean()
                daily_data.fillna(daily_mean, inplace=True)

    return raw_data

def propagate_stde(result, error_1, error_2):
    '''calculate the stnd error of a function of two variables.
    errors are relative errors if the function is a multiplication.
    if the function is addition(or subtraction, errors are absolute.
    '''

    relative_error = (error_1**2 + error_2**2)**0.5
    propagated_error = relative_error * result

    return propagated_error


def DataFrame_to_image(data, css, outputfile="out.png", format="png"):
    '''
    For rendering a Pandas DataFrame as an image.
    data: a pandas DataFrame
    css: a string containing rules for styling the output table. This must
         contain both the opening an closing <style> tags.
    *outputimage: filename for saving of generated image
    *format: output format, as supported by IMGKit. Default is "png"
    '''
    fn = str(random.random() * 100000000).split(".")[0] + ".html"

    try:
        os.remove(fn)
    except:
        None
    text_file = open(fn, "a")

    # write the CSS
    text_file.write(css)
    # write the HTML-ized Pandas DataFrame
    text_file.write(data.to_html())
    text_file.close()

    # See IMGKit options for full configuration,
    # e.g. cropping of final image
    imgkitoptions = {"format": format}
    imgkit.from_file(fn, outputfile, options=imgkitoptions)
    os.remove(fn)


# def get_round(dataframe):
#
#     number = dataframe.min().min()
#     bounds = h, m, l = (10, 0.1, 0.01)
#
#     if number >= h:
#         return 0
#
#     if number < h and number >= m:
#         return 2
#
#     elif number < m  and number >= l:
#         return 3
#
#     else:
#         return 4

