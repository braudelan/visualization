from matplotlib import pyplot
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator


def plot_week_ends(means, normalized, means_stde, number, set_name):

    # pyplot parameters

    pyplot.style.use('seaborn-darkgrid')

    pyplot.rc('legend',
              facecolor='inherit',
              framealpha=0,
              markerscale=1.5)
    pyplot.rc('font', size=19) # control text size when not defined locally
    pyplot.rc('lines', linewidth=3)

    symbol_text_params = {'weight': 'bold',
                          'size': 26,
                          }


    line_styles = densly_dashed, solid = ((0, (2, 1)), (0, ()))

    major_locator = MultipleLocator(7)  # major ticks locations
    minor_locator = MultipleLocator(1)  # minor ticks locations


    # local parameters
    normalized_stde = None
    num_data_points = len(means.index)    # number of sampling days
    excluded = normalized.iloc[1:, :]  # treatment effect without day 0
    for frame in [means, means_stde]:
        frame.columns = frame.columns.map('_'.join)
        frame.reset_index(inplace=True)
    normalized.reset_index(inplace=True)
    last_day = means['days'].iloc[-1]     # last sampling day
    every_seven = [0,7,14,21,28]


    # figure text
    title_text = r'$\bf{Figure %s.}$ means of %s across %s days of incubation. (a) all soils, ' \
                 r'(b) normalized to control' % (number, set_name, last_day)

    xlabel_text = r'$incubation\ time\ \slash\ days$'

    if set_name == 'RESP':
        means_ylabel_text = r'$%s\ \slash\ mg\ CO_{2}-C\ \ast\ kg\ soil^{-1}\ \ast\ h^{-1} $' % set_name
    else:
        means_ylabel_text = r'$%s\ \slash\ mg \ast kg\ soil^{-1}$' % set_name

    normalized_ylabel_text = r'$%s\ normalized\ \slash\ percent\ of\ control$' % set_name


    # create and adjut figure
    week_ends_figure = pyplot.figure(number, figsize=(25,15))
    week_ends_figure.tight_layout()
    week_ends_figure.subplots_adjust(hspace=0.3)



    # create all means axes and set parameters
    means_axes = week_ends_figure.add_subplot(211)

    means_axes.set_xlim((0,last_day))
    means_axes.xaxis.set_minor_locator(minor_locator)
    means_axes.xaxis.set_major_locator(major_locator)
    means_axes.tick_params(axis='x', which='minor', width=1, length=3)
    means_axes.text(0.03, 1.05, "a", transform=means_axes.transAxes, fontdict=symbol_text_params)  # symbol
    means_axes.set_ylabel(means_ylabel_text, labelpad=30)
    means_axes.set_xlabel('')


    # plot all means
    means_lines = plot_axes_lines(means.loc[every_seven], means_stde.loc[every_seven], means_axes) # todo take out specific data points (MBC)
                                                                 #      insert markings for time points where
                                                                 #      MRE was applied

    # costumize all means legend
    list_lines = list(means_lines.items())
    lables = []
    handles = []
    for line in list_lines[3:]:
        label = line[0][2:]
        handel = line[1]
        lables.append(label)
        handles.append(handel)
    treatment_labels = ['MRE apllied', 'c']
    lables.extend(treatment_labels)
    treatment_handles = [Line2D([0], [0], linewidth=5, linestyle=solid, color='k'),
                         Line2D([0], [0], linewidth=5, linestyle=densly_dashed, color='k')]
    handles.extend(treatment_handles)
    means_legend = means_axes.legend(handles, lables) # todo remove error bars from legend objects.


    # create normalized axes and set parameters
    normalized_axes = week_ends_figure.add_subplot(212)

    normalized_axes.set_xlim((0, last_day))
    normalized_axes.xaxis.set_major_locator(major_locator)
    normalized_axes.xaxis.set_minor_locator(minor_locator)
    normalized_axes.set_ylabel(normalized_ylabel_text, labelpad=30)
    normalized_axes.set_xlabel(xlabel_text, labelpad=30)
    normalized_axes.tick_params(axis='x', which='minor', width=1,length=3)
    normalized_axes.text(0.03, 1.05, "b", transform=normalized_axes.transAxes, fontdict=symbol_text_params)


    # plot normalized
    normalized_lines = plot_axes_lines(normalized.loc[every_seven], normalized_stde.loc[every_seven], normalized_axes)

    normalized_axes.legend()

    week_ends_figure.text(0, -0.4, title_text, fontsize=22, transform=normalized_axes.transAxes)

    return week_ends_figure
