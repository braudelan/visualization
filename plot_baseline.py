from matplotlib import

from get_raw_data import get_multi_sets


dataframes = get_multi_sets(args)

title_text = r'baseline values of important parameters for each soil'

figure = pyplot.figure(5)

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

figure.savefig("./figures/baseline_table.png", bbox_inches='tight')
pyplot.cla()