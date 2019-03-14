from matplotlib import pyplot


def make_growth_table(weekly_growth, argv):

    args = (argv.table_number, argv.test)

    pyplot.rc('font', size=18)
    titles_params = { 'fontsize': 20}

    row_labels = []
    for soil in ('COM', 'MIN', 'UNC'):
        label_c = soil + r'$_c$'
        label_t = soil + r'$_t$'
        row_labels.append(label_c)
        row_labels.append(label_t)

    title_text = r'$\bf{Table %s.}$  weekly change in %s across 4 weeks of incubation' %args

    table_figure = pyplot.figure(1)
    table_figure.tight_layout()
    table_figure.subplots_adjust(top=0.3)

    growth = table_figure.add_subplot(111)
    growth.axis('off')
    growth.axis('tight')
    growth.set_title(title_text, pad=0.2, fontsize=20, position=(0.42, 1.1))

    growth_columns = ['1st week', '2nd week', '3rd week', '4th week']

    growth_table = pyplot.table(cellText=weekly_growth.values,
                                loc='center',
                                colLabels=growth_columns,
                                rowLabels=row_labels,
                                cellLoc='center',
                                colWidths=[0.07, 0.1, 0.1, 0.1, 0.1],
                                )

    for cell in growth_table._cells:
        if cell[0] == 0 or cell[1] == -1:
            growth_table._cells[cell].set_text_props(weight='bold')

    growth_table.scale(2, 3)


    return table_figure

