from matplotlib import pyplot


def make_ttest_table(daily_ttest, test):

    title_text = r'%s daily Ttest' %test

    figure = pyplot.figure(3)

    axes = figure.add_subplot(111)
    axes.axis('off')
    axes.axis('tight')
    ttest_title = axes.set_title(title_text, pad=0.2, fontsize=20, position=(0, 1.1))

    # ttest_columns = daily_ttest.columns

    ttest_table = pyplot.table(cellText=daily_ttest.values,
                               loc='center',
                               colLabels=daily_ttest.columns,
                               rowLabels=daily_ttest.index,
                               cellLoc='center',
                               colWidths=[0.1 for x in daily_ttest.columns],
                               # bbox = [0.0, -1.3, 1.0, 1.0]
                               )

    for cell in ttest_table._cells:
        if cell[0] == 0 or cell[1] == -1:
            ttest_table._cells[cell].set_text_props(weight='bold')

    ttest_table.scale(2, 3)

    return figure