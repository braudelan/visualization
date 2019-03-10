from matplotlib import pyplot

def make_tables(weekly_growth, argv):
    args = (argv.table_number, argv.test)

#    nrows = len(weekly_growth.index)
#    ncols = len(weekly_growth.columns)
#    wcell = 0.7
#    hcell = 0.2
#    wpad, hpad = 0, 0
#    
    title_text = r'$\bf{Table %s.}$  weekly increase in %s for treated soils' %args
    
    table_figure = pyplot.figure(1)
    table_figure.tight_layout()
    table_figure.subplots_adjust(top=0.3,)    
    
    
    
    growth = table_figure.add_subplot(111)
    growth.axis('off')
    growth.axis('tight')
    growth.set_title(title_text, loc='center', fontsize=16)
    
    column_names = ['1st week', '2nd week', '3rd week']
    
    table = pyplot.table(cellText=weekly_growth.values,
                 loc='center',
                 colLabels=column_names,
                 rowLabels=['COM', 'MIN', 'UNC'],
                 cellLoc='center',
                 colWidths=[0.07,0.1, 0.1, 0.1],
                 )
    
    for cell in table._cells:
        if cell[0] == 0 or cell[1] == -1:
            table._cells[cell].set_text_props(weight='bold')
            
    table.scale(2,3)
    
    

    return table_figure
#    pyplot.savefig("%s_tables.pdf" %argv.test, bbox_inches='tight', pad_inches=2 )

    