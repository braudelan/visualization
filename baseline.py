import pandas
from pandas     import DataFrame
from matplotlib import pyplot

from raw_data import get_raw_data
from get_stats    import get_stats
from Ttest    import get_daily_Ttest
from which_round  import get_round

def get_baseline(keys):

    """
    get baseline values of specified data sets and appends them into a single dataframe.
    """

    # dataframe containing basline values of each parameter for every soil
    baseline_dataframe = DataFrame()

    # get the data and append into *basline_frame*
    for key in keys:

        raw_data           = get_raw_data(key)
        means              = get_stats(raw_data)[0]  # get_stats returns 4 variabels, we want only the *means* variable
        control_means      = means.xs('c', level='treatment', axis=1)
        baseline           = control_means.loc[0].round(get_round(means))
        baseline_dataframe = pandas.concat([baseline_dataframe, baseline], axis=1)
        baseline_dataframe = baseline_dataframe.rename(index=str, columns={0:key})

    return baseline_dataframe


def plot_baseline(baseline_dataframe):

    """
    plot baseline_dataframe into a table
    :param baseline_dataframe:
    """


    title_text = r'baseline values of important parameters for each soil'

    baseline_figure = pyplot.figure()

    axes = baseline_figure.add_subplot(111)
    axes.axis('off')
    axes.axis('tight')
    ttest_title = axes.set_title(title_text, pad=0.2, fontsize=20, position=(0, 1.1))


    baseline_table = pyplot.table(cellText=baseline_dataframe.values,
                               loc='center',
                               colLabels=baseline_dataframe.columns,
                               rowLabels=baseline_dataframe.index,
                               cellLoc='center',
                              # colWidths=[0.1 for x in baseline_dataframe.columns],
                               # bbox = [0.0, -1.3, 1.0, 1.0]
                               )

    for cell in baseline_table._cells:
        if cell[0] == 0 or cell[1] == -1:
            baseline_table._cells[cell].set_text_props(weight='bold')

    baseline_table.scale(2, 3)

    baseline_figure.savefig("./misc_figures/baseline_table.png", bbox_inches='tight')
    pyplot.cla()