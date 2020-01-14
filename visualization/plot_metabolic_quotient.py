from matplotlib import pyplot
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap as listed_cmp

from data_handling.respiration_to_biomass import ratio, errors, labels
from helpers import *


colors = Constants.color_options
CMP = listed_cmp(colors)

# ticks and labels
TITLE_FONT_SIZE = 16
TITLE_PAD = 15
X_LABEL_PAD = 20
Y_LABEL_PAD = X_LABEL_PAD
AXIS_LABEL_FONTSIZE = 14
TICK_LABEL_FONTSIZE = 14

# error bars
CAP_LENGTH = 2.5
ERROR_LINEWIDTH = 1
CAP_THICKNESS=1
ERROR_KEY_WORDS = {
    'elinewidth': ERROR_LINEWIDTH,
    'capthick': CAP_THICKNESS
}

# labels
TITLE = r'$Ratio\ of\ Cumulative\ CO_2\ to\ Microbial\ growth$'

pyplot.style.use('seaborn-ticks')
axes: Axes = ratio.plot(
    kind='bar',
    yerr=errors,
    colormap=CMP,
    capsize=CAP_LENGTH,
    error_kw=ERROR_KEY_WORDS,
    legend=False
)

axes.set_xticklabels(labels)
# axes.set_ylabel(
#     r'$\%$',
#     labelpad=5,
#     fontsize=AXIS_LABEL_FONTSIZE
# )
axes.set_title(TITLE, pad=TITLE_PAD, fontsize=AXIS_LABEL_FONTSIZE)

axes.set_xlabel(
    r'$week\ of\ incubation$',
    labelpad=30,
    fontsize=AXIS_LABEL_FONTSIZE
)

axes.xaxis.set_tick_params(
    length=0,
    pad=15,
)

axes.yaxis.set_tick_params(
    labelsize=AXIS_LABEL_FONTSIZE
)
x_majortick_labels = axes.get_xmajorticklabels()
axes.set_xticklabels(
    x_majortick_labels,
    ha='center',
    fontsize=TICK_LABEL_FONTSIZE,
    rotation=0
)

handles, labels = axes.get_legend_handles_labels()
labels = [r'$ORG$', r'$MIN$', r'$UNC$']
axes.legend(handles, labels, loc='upper left', bbox_to_anchor=(0.05, 0.9), fontsize=AXIS_LABEL_FONTSIZE)

FIGSIZE = (8, 4)
figure: Figure = axes.figure
figure.set_size_inches(8, 4)

DPI = 144

dir = '/home/elan/Dropbox/research/student_conference/figures/'
file = f'metabolic_quotient.png'
file_path = f'{dir}{file}'
figure.savefig(file_path, format='png', bbox_inches='tight', dpi=DPI)