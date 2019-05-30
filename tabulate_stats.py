import pandas
from matplotlib import pyplot

from get_raw_data import get_setup_arguments
from get_stats import get_stats
from which_round import get_round


input_file = "all_tests.xlsx"

DATA_SET_KEYS = get_setup_arguments().specific

means_dict = {}
for data_set in DATA_SET_KEYS:

    # input data into DataFrame
    raw_data = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                 sheet_name=data_set,
                                 na_values=["-", " "]).rename_axis("days")
    raw_data.columns.rename(["soil", "treatment", "replicate"],
                            level=None, inplace=True)
    raw_data.columns.set_levels(['c', 't'], level='treatment', inplace=True)

    means, means_stde, normalized, diff = get_stats(raw_data)

    # if test == 'NH4' or test == 'NO3':
    #     continue

    if data_set == 'RESP':
        means = means * 24

    round_factor = get_round(means)

    means_dict[data_set] = means.round(round_factor).T

means_dict['Ni'] = means_dict['NH4'] + means_dict['NO3']
means_dict['Ni'] = means_dict['Ni'].round(get_round(means_dict['Ni']))

n = 1
for key in means_dict:

    data = means_dict[key]

    title_text = r'%s means' % key

    figure = pyplot.figure(n)

    axes = figure.add_subplot(111)
    axes.axis('off')
    axes.axis('tight')
    title = axes.set_title(title_text, pad=0.2, fontsize=20, position=(-0.5, 1.1))

    table = pyplot.table(cellText=data.values,
                               loc='center',
                               colLabels=data.columns,
                               rowLabels=data.index,
                               cellLoc='center',
                               colWidths=[0.1 for x in data.columns],
                               # bbox = [0.0, -1.3, 1.0, 1.0]
                               )

    for cell in table._cells:
        if cell[0] == 0 or cell[1] == -1:
            table._cells[cell].set_text_props(weight='bold')

    table.scale(2, 3)

    figure.savefig("./means_tables/%s.png" % key, bbox_inches='tight')
    pyplot.cla()

    n += 1

