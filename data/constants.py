# constant parameters used in different modules in the project
from seaborn import color_palette


input_file_path = '../input_data.xlsx'
figures_directory = '/home/elan/Dropbox/research/figures'
parameters = [
    'MBC',
    'HWS',
    'DOC',
    'AS',
    'RESP',
    'MBN',
    'ERG',
    'TOC',
    'TON',
]
generic_units = r'mg\ast kg\ soil^{-1}'
units = [
    r'mg\ C\ast kg\ soil^{-1}',
    r'mg\ C\ast kg\ soil^{-1}',
    r'mg\ C\ast kg\ soil^{-1}',
    r'\%WSA',
    r'mg CO_2-C \ast kg^{-1}\ast day^{-1}',
    r'mg\ C\ast kg\ soil^{-1}',
    r'\%MBC',
    r'\%soil weight',
    r'\%soil weight'
]
TITLES = [
    r'Microbial\ Biomass\ Carbon',
    r'Hot\ Water\ Extractable\ Sugars',
    r'Water\ Extractable\ Organic\ Carbon',
    r'Aggregate\ Stability',
    r'Microbial\ Respiration',
    r'Microbial\ Biomass\ Nitrogen',
    r'Soil\ Ergosterol',
    r'Total Organic Carbon',
    r'Total Organic Nitrogen'
]

parameters_units = dict(zip(parameters, units))
PARAMETERS_TITLES = dict(zip(parameters, TITLES))

LONG_TERM_TREATMENTS = [
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
colors =  dict(zip(LONG_TERM_TREATMENTS, color_options))
markers =  dict(zip(LONG_TERM_TREATMENTS, marker_options))
line_styles = dict(zip(LONG_TERM_TREATMENTS, line_style_options))
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

# todo
#  change variable names to capital letters and
#  then use them as they are by importing * from the module