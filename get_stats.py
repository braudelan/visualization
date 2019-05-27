from collections import namedtuple

BasicStats = namedtuple('BasicStats', ['means', 'MRE', 'control', 'means_stde',
                                               'MRE_stde', 'difference', 'normalized_diff'])
def get_stats(raw_data):

    # means
    groupby_soil_treatment = raw_data.iloc[:,1:].groupby(level=['treatment', 'soil'],axis=1)  # group 4 replicates from every soil-treatment pair
    means                  = groupby_soil_treatment.mean()  # means of 4 replicates
    means_stde             = groupby_soil_treatment.sem()  # stnd error of means

    # means of control\MRE-treatment
    control = means.xs('c', axis=1, level='treatment')
    MRE = means.xs('t', axis=1, level='treatment')
    MRE_stde = means_stde.xs('t', axis=1, level='treatment')
    control_stde = means_stde.xs('c', axis=1, level='treatment')

    #treatment effect
    difference = MRE - control   # treatment - control
    normalized_diff = difference / control * 100  # difference normalized to control (percent)


    return BasicStats(means=means, MRE=MRE, control=control, means_stde=means_stde, MRE_stde=MRE_stde,
                                                             difference=difference, normalized_diff=normalized_diff)



def get_carbon_info():

    sets_names = ['MBC', 'MBN', 'RESP', 'DOC', 'HWE-S','TOC']
    dataframes = get_multi_sets(sets_names)
    stats_frames = {}
    for set in sets_names:
        raw = dataframes[set]
        stats = get_stats(raw)
        means = stats.means
        means_stde = stats.means_stde
        set_stats = {'means': means, 'means_stde': means_stde}
        stats_frames[set] = set_stats

    MBC = stats_frames['MBC']['means']
    MBN = stats_frames['MBN']['means']
    RESP = stats_frames['RESP']['means']
    DOC = stats_frames['DOC']['means']
    HWES = stats_frames['HWE-S']['means']
    HWES_C = HWES / 4  # 40% C in glucose
    C_to_N_ratio = MBC / MBN
    soil_available_C = MBC + HWES_C + DOC
    available_C_control = available_C.xs(key='c', level=0, axis=1)
    available_C_MRE = available_C.xs(key='t', level=0, axis=1)
    available_C_difference = available_C_MRE- available_C_control # todo plot available_c and available_C_difference

    return soil_available_C, available_C_difference, C_to_N_ratio


