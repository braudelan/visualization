import os
from collections import namedtuple
import random

import imgkit
import numpy
from pandas.io.formats.style import Styler
from seaborn import color_palette


class Stats:
    def __init__(self, means, stde):
        self.means = means
        self.stde = stde


class Constants:
    input_file_path = 'input_data.xlsx'
    figures_directory = '/home/elan/Dropbox/research/figures'
    parameters = [
        'MBC',
        'HWES',
        'WEOC',
        'AS',
        'Resp',
        'MBN',
        'Erg',
        'TOC',
        'TON',
    ]
    generic_units = r'mg\ast kg\ soil^{-1}'
    units = [
        r'mg\ast kg\ soil^{-1}',
        r'mg\ast kg\ soil^{-1}',
        r'mg\ast kg\ soil^{-1}',
        r'\%WSA',
        r'mg CO_2-C \ast kg^{-1}\ast day^{-1}',
        r'mg\ast kg\ soil^{-1}',
        r'\%MBC',
        r'\%soil weight',
        r'\%soil weight'
    ]
    parameters_units = dict(zip(parameters, units))
    LTTs = [
        'ORG',
        'MIN',
        'UNC'
    ]
    line_style_options = (
        '--',
        '-.',
        ':',
    )
    color_options = color_palette('Set1', n_colors=3).as_hex()

    marker_options = (
        's',
        'o',
        'v',
    )
    colors =  dict(zip(LTTs, color_options))
    markers =  dict(zip(LTTs, marker_options))
    line_styles = dict(zip(LTTs, line_style_options))
    treatment_labels = ['c', 't']
    level_names = [
        "treatment",
        "soil",
        "replicate",
    ]
    table_css = """
                    <style type=\"text/css\">
                    table {
                    color: #333;
                    font-family: Helvetica, Arial, sans-serif;
                    width: 640px;
                    border-collapse:
                    collapse; 
                    border-spacing: 0;
                    }
                    td, th {
                    border: 1px solid transparent; /* No more visible border */
                    height: 30px;
                    }
                    th {
                    background: #DFDFDF; /* Darken header a bit */
                    font-weight: bold;
                    }
                    td {
                    background: #FAFAFA;
                    text-align: center;
                    }
                    table tr:nth-child(odd) td{
                    background-color: white;
                    }
                    </style>
                    """


def get_week_ends(dataframe):

    every_7th = dataframe.index.isin([0, 7, 14, 21, 28])

    return every_7th


def replace_nan_with_mean(raw_data):
    '''
     replace nan values with the average of remaining replicates.

     :parameter
     raw_data: dataframe
     either treated, control or normalized results.
     treatment level has to be dropped from columns.
     '''

    TREATMENTS = Constants.treatment_labels
    SOILS = Constants.LTTs
    DAYS = raw_data.index

    for soil in SOILS:
        for day in DAYS:
            daily_data = raw_data.loc[day, soil]
            daily_mean = daily_data.mean()
            daily_data.fillna(daily_mean, inplace=True)

    return raw_data


def propagate_error(result, error_1, error_2):
    '''compute the stnd error of a multiplication of two variables.
    error_1 and error_2 are relative errors
     (i.e divided by the mean).
    '''

    relative_error = (error_1**2 + error_2**2)**0.5
    propagated_error = relative_error * result

    return propagated_error


def style_to_image(styler: Styler, output_file='output/output.png'):
    renderd = styler.render()
    imgkit.from_string(renderd, output_file)


def DataFrame_to_image(data, css, outputfile="weekly_mbc_growth.png", format="png"):
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


def get_round(data):

    minimum = data.min().min()
    large, medium, small = (10, 0.1, 0.01)

    significant_digits = (
        0 if minimum >= large else
        2 if minimum < large and minimum >= medium else
        3 if minimum < medium and minimum >= small else
        4
    )

    return significant_digits


def round_column_data(series):
    significant_digits = get_round(series)
    rounded_series = series.round(significant_digits)

    return rounded_series


def get_cumulative_sum(array: numpy.ndarray):
    array_length = len(array)
    cum_sum = numpy.zeros(array_length)

    for i in range(array_length):
        if i == 0:
            cum_sum[i] = array[i]
        else:
            cum_sum[i] = cum_sum[i-1] + array[i]

    return cum_sum


def get_cumulative_error(array: numpy.ndarray):
    array_length = len(array)
    cum_sum = numpy.zeros(array_length)

    for i in range(array_length):
        if i == 0:
            cum_sum[i] = array[i]
        else:
            cum_sum[i] = ((cum_sum[i-1])**2 + (array[i])**2)**0.5

    return cum_sum


MATPLOTLIB_STYLES = [u'seaborn-darkgrid', u'seaborn-notebook', u'classic', u'seaborn-ticks', u'grayscale', u'bmh',
                     u'seaborn-talk', u'dark_background', u'ggplot', u'fivethirtyeight', u'_classic_test',
                     u'seaborn-colorblind', u'seaborn-deep', u'seaborn-whitegrid', u'seaborn-bright', u'seaborn-poster',
                     u'seaborn-muted', u'seaborn-paper', u'seaborn-white', u'seaborn-pastel', u'seaborn-dark',
                     u'seaborn', u'seaborn-dark-palette']
