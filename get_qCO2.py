import pandas

from get_stats import get_stats

def get_qCO2():
    input_file = "all_tests.xlsx"

    # get statistics
    TESTS = ['MBC', 'RESP']
    stats = {}

    for test in TESTS:

        # input data into DataFrame
        raw_data = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                         sheet_name=test,
                                         na_values=["-", " "]).rename_axis("days")
        raw_data.columns.rename(["soil", "treatment", "replicate"],
                                level=None, inplace=True)
        raw_data.columns.set_levels(["c", "t"], level=1, inplace=True)

        #get statistics and parameters
        means, means_stde, effect = get_stats(raw_data)

        stats[test] = means


    # instantaneous qCO2
    MBC_means = stats['MBC']
    RESP_means = stats['RESP']
    qCO2_inst = RESP_means / MBC_means


    return qCO2_inst