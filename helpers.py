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


def replace_nan_with_mean(raw_data):
    '''
     replace nan values with the average of remaining replicates.

     :parameter
     raw_data: dataframe
     either treated, control or normalized results.
     treatment level has to be dropped from columns.
     '''

    TREATMENTS = Constants.treatment_labels
    SOILS = Constants.groups
    DAYS = raw_data.index

    for soil in SOILS:
        for day in DAYS:
            daily_data = raw_data.loc[day, soil]
            daily_mean = daily_data.mean()
            daily_data.fillna(daily_mean, inplace=True)

    return raw_data

def propagate_stde(result, error_1, error_2):
    '''compute the stnd error of a multiplication of two variables.
    error_1 and error_2 are relative errors meaning the errors
    divided by the mean itself.
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


def get_round(dataframe):

    minimum = dataframe.min().min()
    large, medium, small = (10, 0.1, 0.01)

    round_to = (
        0 if minimum >= large else
        2 if minimum < large and minimum >= medium else
        3 if minimum < medium and minimum >= small else
        4
    )

    return round_to