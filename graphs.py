import matplotlib
from matplotlib import pyplot
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)


def visualize(means, treatment_effect, stde_means, stde_effect, argv):
    stde_treatment_means = stde_means.xs("t", axis=1, level=1)
    
    args = (argv.figure_number, argv.test)

    majorLocator = MultipleLocator(7)
    minorLocator = MultipleLocator(1)

    pyplot.rc('legend', facecolor='inherit', frameon=False, markerscale=1.2)
    pyplot.rc('font', size=16)
    pyplot.rc('lines', linewidth=2,)

    title_text = r'$\bf{Figure %s.}$ means of %s across 28 days of incubation. (a) all soils, ' \
                 r'(b) treated soils only (c) normalized to control' % args
    ylabel_text = r'$biomass-C\ \slash\ mg \ast kg\ soil^{-1}$'
    xlabel_text = r'$incubation\ time\ \slash\ days$'
    symbol_fontdic ={'weight': 'bold',
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
    # title and axis labels
    figure.text(0, 0.01, title_text, fontsize=19)
    figure.text(0, 0.5, ylabel_text, fontsize=19, rotation=90, va='center')
    figure.text(0.5, 0.06, xlabel_text, fontsize=19, ha='center')

    means_axes = figure.add_subplot(311)
    # plot data
    means.plot(ax=means_axes, xlim=(0,30), yerr=stde_means)
    means_axes.text(0.07, 0.85, "a", transform=means_axes.transAxes, fontdict=symbol_fontdic)
    means_axes.xaxis.set_major_locator(majorLocator)
    means_axes.xaxis.set_minor_locator(minorLocator)
    means_axes.legend((means_axes.get_lines()),(all_means_legend))
    means_axes.set_xlabel('')

    MRE_means_axes = figure.add_subplot(312)
    #plot data
    means.xs("t", axis=1, level=1).plot(
                                        kind="bar",
                                        ax=MRE_means_axes,
                                        xticks=range(0, 30, 7),
                                        xlim=(0, 30),
                                        yerr=stde_treatment_means,
                                        )
    MRE_means_axes.text(0.07, 0.85, "b", transform=MRE_means_axes.transAxes, fontdict=symbol_fontdic)
    MRE_means_axes.legend()
    MRE_means_axes.set_xlabel(MRE_means_axes.get_legend_handels_labels())

    effect_axes = figure.add_subplot(313)
    # plot data
    treatment_effect.plot(kind="bar", ax=effect_axes,
                          xticks=list(means.index[1:]), yerr=stde_effect)
    effect_axes.text(0.07, 0.85, "c", transform=effect_axes.transAxes, fontdict=symbol_fontdic)
    effect_axes.set_xlabel('')

    return figure
    
