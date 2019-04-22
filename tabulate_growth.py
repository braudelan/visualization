from matplotlib import pyplot


def make_growth_table(weekly_growth, test, number):

# variabels
    args = (number, test)

    row_labels = []
    for soil in ('COM', 'MIN', 'UNC'):
        control_label   = soil + r'$_{c}$'
        treatment_label = soil + r'$_{t}$'
        row_labels.append(control_label)
        row_labels.append(treatment_label)

    growth_columns = ['1st week', '2nd week', '3rd week', '4th week']


# pyplot parameters
    pyplot.rc('font', size=18)
    title_params = { 'fontsize': 20}

# text
    title_text = r'$\bf{Table %s.}$  weekly change in %s across 4 weeks of incubation' %args

# create and adjust figure
    table_figure = pyplot.figure(number)
    table_figure.tight_layout()
    table_figure.subplots_adjust(top=0.3)

# add and adjust subplot
    axes = table_figure.add_subplot(111)
    axes.axis('off')
    axes.axis('tight')
    axes.set_title(title_text, pad=0.2, fontsize=20, position=(0.42, 1.1))

# plot table
    growth_table = pyplot.table(cellText=weekly_growth.values,
                                loc='center',
                                colLabels=growth_columns,
                                rowLabels=row_labels,
                                # cellLoc='center',
                                # colWidths=[0.07, 0.1, 0.1, 0.1, 0.1],
                                )

    for cell in growth_table._cells:
        if cell[0] == 0 or cell[1] == -1:
            growth_table._cells[cell].set_text_props(weight='bold')

    growth_table.scale(2, 3)


    return table_figure

