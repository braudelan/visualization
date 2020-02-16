import pdb

import numpy
from pandas import Series
from scipy.stats import zscore

from data.raw_data import *

SIGMA = 1.7

def exclude_outliers(raw_data: DataFrame):
    ''' replace outlying raw data entries with None.'''

    def get_outliers(series):
        '''
        return a Series of booleans representing outliers.

        to be used as parameter for apply DataFrame apply method.
        a mask for conditional replacing of outliers with None.

        :param series:
        a Series passed from apply method

        :return: outliers_booleand:
        Series with boolean values. False represent outliers
        '''

        levels_to_groupby = ['treatment', 'soil']

        def zscore_as_booleans(series):

            def get_outliers_mask(array, sigma=SIGMA):
                absolute_values = numpy.absolute(array)
                max = absolute_values.max()
                outliers_mask = numpy.empty_like(array, dtype=bool)

                for x in absolute_values:
                    where_x = numpy.where(absolute_values == x)
                    index_x = where_x[0]
                    if x == max and x > sigma:
                        outliers_mask[index_x] = False
                    else:
                        outliers_mask[index_x] = True

                return outliers_mask

            scored = zscore(series)
            outliers_booleaned = get_outliers_mask(scored)
            outliers_booleaned = Series(outliers_booleaned)

            return outliers_booleaned

        grouped = series.groupby(level=levels_to_groupby)
        outliers = grouped.apply(zscore_as_booleans)

        return outliers

    outliers = raw_data.apply(get_outliers, axis=1)
    outliers = outliers.rename(columns={0: 1, 1: 2, 2: 3, 3: 4}, level=2) #todo columns argument should be replaced with namespace
    outliers = outliers.reindex(labels=['MIN', 'ORG', 'UNC'], axis=1, level=1) #todo same as above for labels argument
    # pdb.set_trace()
    outliers_excluded = raw_data.where(outliers == True, None)
    outliers_excluded = outliers_excluded.astype('float64')

    return outliers_excluded

# test
if __name__ == '__main__':

    raw_doc = get_raw_data('DOC')
    excluded = exclude_outliers(raw_doc)
