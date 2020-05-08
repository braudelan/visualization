# constant parameters used in different modules in the project
from seaborn import color_palette


main_input_file = 'input_data.xlsx'
preliminary_input_file = 'preliminary_data.xlsx'
figures_directory = '/home/elan/Dropbox/research/thesis/latex_thesis/thesis_figures'
PRELIMINARY_PARAMS = [
    'MBC',
    'Resp',
    'WEOC',
    'HWEC',
    'HWES-C',
    'Erg',
]
MAIN_PARAMS = [
    'MBC',
    'MBN',
    'Resp',
    'HWES',
    'WEOC',
    'AS',
    'Erg',
    'TOC',
    'TON',
]
parameters = [
    'MBC',
    'HWEC',
    'HWES',
    'HWES-C',
    'WEOC',
    'AS',
    'Resp',
    'MBN',
    'Erg',
    'TOC',
    'TON',
    'Erg-to-MBC',
    'CUE',
]
generic_units = r'mg\ast kg\ soil^{-1}'
units = [
    r'mg\ C\ast kg\ soil^{-1}',
    r'mg\ C\ast kg\ soil^{-1}',
    r'mg\ Carbohydrate\ \ast\ kg\ soil^{-1}',
    r'mg\ Carbohydrate-C\ast kg\ soil^{-1}',
    r'mg\ C\ast kg\ soil^{-1}',
    '%WSA',
    r'mg\ CO_2-C * kg^{-1} * day^{-1}',
    r'mg C * kg soil^{-1}',
    r'mg Ergosterol * kg^{-1} * day^{-1}',
    r'% of soil weight',
    r'% of soil weight',
    r'% of MBC',
    r''
]
TITLES = [
    r'Microbial Biomass Carbon',
    r'Hot Water Extractable Carbon',
    r'Hot Water Extractable Carbohydrates',
    r'Hot Water Extractable Carbohydrates',
    r'Water Extractable Organic Carbon',
    r'Aggregate Stability',
    r'Microbial Respiration',
    r'Microbial Biomass Nitrogen',
    r'Soil Ergosterol',
    r'Total Organic Carbon',
    r'Total Organic Nitrogen',
    r'Soil Ergosterol',
    r'Carbon Use Efficiency',
]

PRELIMINARY_STTs = [
    'CON',
    'STR',
    'KWC',
]
titles_for_STTs = [
    'Control',
    'Straw amended',
    'Kitchen Waste Compost amended'
]

PRELIMINARY_STT_titles = dict(zip(PRELIMINARY_STTs, titles_for_STTs))
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