from matplotlib import pyplot


def make_ttest_table(daily_ttest, agrv):


    ttest = table_figure.add_subplot(212)
    ttest.axis('off')
    ttest.axis('tight')
    ttest_title = ttest.set_title(title_text, pad=0.2, fontsize=20, position=(-0.2, 1.1))

    ttest_columns = daily_ttest.columns

    ttest_table = pyplot.table(cellText=daily_ttest.values,
                               loc='center',
                               colLabels=daily_ttest.columns,
                               rowLabels=daily_ttest.index,
                               cellLoc='center',
                               colWidths=[0.1 for x in ttest_columns],
                               # bbox = [0.0, -1.3, 1.0, 1.0]
                               )

    for cell in ttest_table._cells:
        if cell[0] == 0 or cell[1] == -1:
            ttest_table._cells[cell].set_text_props(weight='bold')

    ttest_table.scale(2, 3)
