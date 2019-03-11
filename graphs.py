import matplotlib
from matplotlib import pyplot
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)


def make_graphs(means, treatment_effect, stde_means, argv):
    stde_treatment_means = stde_means.xs("t", axis=1, level=1)
    
    args = (argv.figure_number, argv.test)

    majorLocator = MultipleLocator(7)
    minorLocator = MultipleLocator(1)

    pyplot.rc('legend', facecolor='inherit', frameon=False, markerscale=1.2)
    pyplot.rc('font', size=16)
    pyplot.rc('lines', linewidth=2,)

    title_text = r'$\bf{Figure %s.}$ means of %s across 28 days of incubation. (a) all soils, ' \
                 r'(b) normalized to control' % args
    xlabel_text = r'$incubation\ time\ \slash\ days$'
    means_ylabel_text = r'$biomass-C\ \slash\ mg \ast kg\ soil^{-1}$'

    font_properties ={'weight': 'bold',
                     'size': 22
                    }

    all_means_legend = []
    for soil in ('COM', 'MIN', 'UNC'):
        label_c = soil + r'$_c$'
        label_t = soil + r'$_t$'
        all_means_legend.append(label_c)
        all_means_legend.append(label_t)


    figure = pyplot.figure(1, figsize=(15,20))
    figure.tight_layout()
    figure.subplots_adjust(hspace=0.2)
    figure.text(0.12, 0.01, title_text, fontsize=16)
    figure.text(0.5, 0.04, xlabel_text, fontsize=16, ha='center')


    # means of all expr. units
    means_axes = figure.add_subplot(211)
    means.plot(ax=means_axes,
               xlim=(0,30),
               yerr=stde_means,
               )
    means_axes.set_ylabel('means_ylabel_text', fontdict=font_properties )
    means_axes.text(0.07, 0.85, "a", transform=means_axes.transAxes, fontdict=font_properties)
    means_axes.xaxis.set_major_locator(majorLocator)
    means_axes.xaxis.set_minor_locator(minorLocator)
    means_axes.legend((means_axes.get_lines()),(all_means_legend))
    means_axes.set_xlabel('')

    # treatment effect as percent of control
    effect_axes = figure.add_subplot(313)
    treatment_effect.plot(ax=effect_axes,
                          xticks=list(means.index[1:]),
                          )
    effect_axes.text(0.07, 0.85, "b", transform=effect_axes.transAxes, fontdict=font_properties)
    effect_axes.set_xlabel('')

    return figure
    
