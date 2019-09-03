import pandas
from matplotlib import pyplot

from helpers import get_week_ends, Constants
h

SOILS = Constants.soils

def get_weekly_growth(data, stde):

    week_ends = get_week_ends(data)  # list day 0 and end of every week
    week_end_data = data.loc[week_ends, :]
    week_end_stde = stde.loc[week_ends, :]
    week_labels = ['1st', '2nd', '3rd', '4th'] if len(week_end_data.index) == 5 else ['1st', '2nd', '3rd']
    week_end_days = week_end_data.index
    last_day = week_end_days[-1]

    weekly_growth = pandas.DataFrame(index=SOILS)

    for day, week in zip(week_end_days, week_labels):

        growth = week_end_data.loc[day + 7] - week_end_data.loc[day]
        weekly_growth[week] = growth

    total_growth = week_end_data.loc[last_day] - week_end_data.loc[0]
    weekly_growth['total'] = total_growth

    return weekly_growth



def tabulate_growth(weekly_growth, data_set_name, number):

# variabels
    args = (number, data_set_name)
    #
    # row_labels = []
    # for soil in SOILS:
    #     control_label   = soil + r'$_{c}$'
    #     treatment_label = soil + r'$_{t}$'
    #     row_labels.append(control_label)
    #     row_labels.append(treatment_label)
    #
    # growth_columns = ['1st week', '2nd week', '3rd week', '4th week']


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
                                # colLabels=growth_columns,
                                # rowLabels=row_labels,
                                # # cellLoc='center',
                                # colWidths=[0.07, 0.1, 0.1, 0.1, 0.1],
                                )

    for cell in growth_table._cells:
        if cell[0] == 0 or cell[1] == -1:
            growth_table._cells[cell].set_text_props(weight='bold')

    growth_table.scale(2, 3)


    return table_figure

