import numpy

import data.raw_data as raw_data
import data.stats as stats
import visualization.dynamics as dynamics
import constants

TOP_DIRECTORY = constants.figures_directory
DPI = 144

def visualize_multiple_plots(
        data_sets_names,
        output_dir,
        treatment,
        normalize=None,
        # title_prefix: str=None,
):

    raw_data_sets = raw_data.get_multi_sets(data_sets_names,
                               treatment=treatment, normalize_by=normalize,)

    data_sets = stats.get_multiple_stats(raw_data_sets)

    for data_name, data in data_sets.items():

        wknds = [0, 7, 14, 21, 28]
        index = data.means.index
        
        is_in_wknds = numpy.isin(index, wknds)
        all_in = is_in_wknds.all()
        
        if all_in and len(is_in_wknds) == 5:
            dynamics.make_bar_plot(stats=data,
                                   data_set_name=data_name,
                                   output_dir=output_dir)

        elif all_in and len(is_in_wknds) < 5:
            dynamics.make_table(stats=data,
                                data_set_name=data_name,
                                output_dir=output_dir,
                                treatment=treatment)

        else:
            dynamics.make_line_plot(stats=data,
                                    data_set_name=data_name,
                                    output_dir=output_dir)



#
# def visualize_single_plot(data, data_name, y_label, output_dir):
#
#     # setup figure, axes
#     figure: Figure = setup_figure()
#     axes = setup_axes(figure, y_label)
#
#     # plot
#     make_line_plot(data, axes, with_legend=True)
#
#     # save
#     file_path = f'{TOP_DIRECTORY}/{output_dir}/{data_name}.pdf'
#     figure.savefig(file_path, format='pdf', bbox_inches='tight', dpi=DPI)
#
#     return figure
