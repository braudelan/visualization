from matplotlib import pyplot

def make_tables(weekly_growth, daily_ttest, argv):
    args = (argv.table_number, argv.test)

    title_text = r'$\bf{Table %s.}$  weekly increase in %s for treated soils' %args
    
    table_figure = pyplot.figure(1)
    table_figure.tight_layout()
    table_figure.subplots_adjust(top=0.3,)    
    
    
    
    growth = table_figure.add_subplot(211)
    growth.axis('off')
    growth.axis('tight')
    growth.set_title(title_text, loc='center', fontsize=16)
    
    growth_columns = ['1st week', '2nd week', '3rd week']
    
    growth_table = pyplot.table(cellText=weekly_growth.values,
                 loc='center',
                 colLabels=growth_columns,
                 rowLabels=['COM', 'MIN', 'UNC'],
                 cellLoc='center',
                 colWidths=[0.07,0.1, 0.1, 0.1],
                 )
    
    for cell in growth_table._cells:
        if cell[0] == 0 or cell[1] == -1:
            growth_table._cells[cell].set_text_props(weight='bold')
            
    growth_table.scale(2,3)

    ttest = table_figure.add_subplot(212)
    ttest.axis('off')
    ttest.axis('tight')
    ttest.set_title(title_text, loc='center', fontsize=16)

    ttest_columns = daily_ttest.columns
    ttest_table = pyplot.table(cellText=daily_ttest.values,
                         loc='center',
                         colLabels=ttest_columns,
                         rowLabels=['COM', 'MIN', 'UNC'],
                         cellLoc='center',
                         colWidths=[0.07, 0.1, 0.1, 0.1],

                         )

    for cell in ttest_table._cells:
        if cell[0] == 0 or cell[1] == -1:
            ttest_table._cells[cell].set_text_props(weight='bold')

    ttest_table.scale(2, 3)

    return table_figure

    