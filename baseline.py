import pandas
from pandas     import DataFrame
from matplotlib import pyplot

from get_raw_data import get_single_set
from get_stats    import get_stats
from which_round  import get_round

def get_baseline(keys):

    """
    get baseline values of specified data sets and appends them into a single dataframe.
    """


    # dataframe containing basline values of each parameter for every soil
    baseline_frame = DataFrame()

    # get the data and append into *basline_frame*
    for key in keys:

        data           = get_single_set(key)
        means          = get_stats(data)[0]  # get_stats returns 3 variabels, we want only the *means * variable
        control_means  = means.xs('c', level=1, axis=1)
        baseline       = control_means.loc[0].round(get_round(means))
        baseline_frame = pandas.concat([baseline_frame, baseline], axis=1)
        baseline_frame = baseline_frame.rename(index=str, columns={0:key})

    return baseline_frame

pandas.DataFrame.rename
def plot_baseline(baseline_frame):
    # plot baseline_frame into a table
    title_text = r'baseline values of important parameters for each soil'

    baseline_figure = pyplot.figure(4)

    axes = figure.add_subplot(111)
    axes.axis('off')
    axes.axis('tight')
    ttest_title = axes.set_title(title_text, pad=0.2, fontsize=20, position=(0, 1.1))

    baseline_columns = baseline_data.columns

    baseline_table = pyplot.table(cellText=baseline_data.values,
                               loc='center',
                               colLabels=baseline_data.columns,
                               rowLabels=baseline_data.index,
                               cellLoc='center',
                              # colWidths=[0.1 for x in baseline_data.columns],
                               # bbox = [0.0, -1.3, 1.0, 1.0]
                               )

    for cell in baseline_table._cells:
        if cell[0] == 0 or cell[1] == -1:
            baseline_table._cells[cell].set_text_props(weight='bold')

    baseline_table.scale(2, 3)

    figure.savefig("./misc_figures/baseline_table.png", bbox_inches='tight')
    pyplot.cla()