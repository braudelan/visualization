import matplotlib
from matplotlib import pyplot
from matplotlib.lines import Line2D # import patches or fancybox instead

figure = pyplot.figure(figsize=(8.27 × 11.69))
current_figure = pyplot.gcf()
size = current_figure.get_size_inches() * current_figure.dpi
