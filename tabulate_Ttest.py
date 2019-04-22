from matplotlib import pyplot


def tabulate_Ttest(daily_ttest, test):

    title_text = r'%s daily Ttest' %test

    figure_5 = pyplot.figure(3)
    figure_5.tight_layout()

    axes = figure_5.add_subplot(111)
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

    return figure_5