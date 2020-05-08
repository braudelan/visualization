import constants


def make_table(
    stats,
    output_dir,
):

    #
    def insert_error(means, err):

        means_error = means.copy()
        for row in means.index:
            for column in means.columns:
                mean = means.loc[row, column]
                err = error.loc[row, column]

                means_error.loc[row, column] = \
                '{:.2f} +-'.format(mean) + ' {:.2f}'.format(err)
                
        return means_error

    # get the data and transpose for better presentation
    means = stats.means.T
    error = stats.stde.T

    # append a ±error to each mean value
    means_error = insert_error(means, error)

    # output path
    top_dir = constants.figures_directory
    output_file = f'{top_dir}/'\
                  f'{output_dir}/'\
                  f'baseline.tex'

    # table caption and lable
    caption = f'baseline values of soil parameters '
    label = f'baseline'
    means_error.to_latex(buf=output_file,
                         bold_rows=True,
                         caption=caption,
                         label=label)

