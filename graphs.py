from matplotlib import pyplot
from matplotlib.ticker import MultipleLocator


def make_graphs(means, treatment_effect, means_stde, argv):
    stde_treatment_means = means_stde.xs("t", axis=1, level=1)
    
    args = (argv.figure_number, argv.test)

    majorLocator = MultipleLocator(7)
    minorLocator = MultipleLocator(1)

    pyplot.rc('legend', facecolor='inherit', frameon=False, markerscale=1.5)
    pyplot.rc('font', size=18)
    pyplot.rc('lines', linewidth=3)

    title_text = r'$\bf{Figure %s.}$ means of %s across 28 days of incubation. (a) all soils, ' \
                 r'(b) normalized to control' % args
    xlabel_text = r'$incubation\ time\ \slash\ days$'

    means_ylabel_text = r'$%s\ \slash\ mg \ast kg\ soil^{-1}$' %args[1]
    effect_ylabel_text = r'$%s\ normalized\ \slash\ percent\ of\ control$' %args[1]

    symbol_text_params = {'weight': 'bold',
                         'size': 26,
                         }
    labels_text_params = {'size': 19
                          }


    # means.columns = []
    # for soil in ('COM', 'MIN', 'UNC'):
    #     label_c = soil + r'$_c$'
    #     label_t = soil + r'$_t$'
    #     means.columns.append(label_c)
    #     means.columns.append(label_t)


    figure = pyplot.figure(1, figsize=(15,20))
    figure.tight_layout()
    figure.subplots_adjust(hspace=0.3)
    figure.text(0.05, 0.01, title_text, fontsize=20)


    # means of all expr. units
    means_axes = figure.add_subplot(211)
    if len(means.index) > 5:
        means.plot(ax=means_axes,
                   xlim=(0,30),
                   yerr=means_stde,
                   )
        means_axes.xaxis.set_major_locator(majorLocator)
        means_axes.xaxis.set_minor_locator(minorLocator)
        means_axes.legend(means_axes.get_lines(), (means.columns))

    else:
        means.plot(ax=means_axes,
                   kind='bar',
                   xlim=(0, 30),
                   yerr=means_stde,
                   )

    means_axes.tick_params(axis='x', which='minor', width=1, length=3)
    means_axes.text(0.03, 1.05, "a", transform=means_axes.transAxes, fontdict=symbol_text_params)  # symbol
    means_ylabel = means_axes.set_ylabel(means_ylabel_text, labelpad=30, fontdict=labels_text_params)
    means_axes.set_xlabel('')

    # treatment effect as percent of control
    effect_axes = figure.add_subplot(212)
    if len(means.index) > 5 :
            treatment_effect.plot(ax=effect_axes,
                                  xlim=(0,30),
                                 )
            effect_axes.xaxis.set_major_locator(majorLocator)
            effect_axes.xaxis.set_minor_locator(minorLocator)
            effect_axes.legend((effect_axes.get_lines()), (treatment_effect.columns))
    else:
        treatment_effect.plot(ax=effect_axes,
                              kind='bar',
                              xlim=(0, 30),
                              )
        # effect_axes.legend(effect_axes.containers, (treatment_effect.columns))

    effect_ylabel = effect_axes.set_ylabel(effect_ylabel_text, labelpad=30, fontdict=labels_text_params)
    effect_axes.set_xlabel(xlabel_text, labelpad=30, fontdict=labels_text_params)
    effect_axes.tick_params(axis='x', which='minor', width=1,length=3)
    effect_axes.text(0.03, 1.05, "b", transform=effect_axes.transAxes, fontdict=symbol_text_params)

    return figure
    
