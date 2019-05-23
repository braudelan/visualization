import pandas
import numpy
from matplotlib import pyplot
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

from get_stats import get_stats

input_file = "all_tests.xlsx"
raw_data = pandas.read_excel(input_file, index_col=0, header=[0, 1, 2],
                                 sheet_name='RESP',
                                 na_values=["-", " "]).rename_axis("days")
raw_data.columns.rename(["soil", "treatment", "replicate"],
                        level=None, inplace=True)
raw_data.columns.set_levels(['c', 't'], level='treatment', inplace=True)

groupby_soil_treatment = raw_data.groupby(level=[0, 1], axis=1)

means, means_stde, normalized = get_stats(raw_data)

first = [1, 3, 7]
second  = [8, 10, 14]

TIME_STEPS = [first, second]
SOILS = ('COM', 'MIN', 'UNC')
TREATMENTS = ['t', 'c']

for soil in SOILS:
    for treatment in TREATMENTS:
        for step in TIME_STEPS:

# define vectors
            data        = means.xs(key=[soil, treatment], level=[0,1], axis=1)
            data_weekly = data.loc[step]
            ym          = numpy.array(data_weekly).flatten()
            time        = data_weekly.index

# define function for fitting
            def Yfit(time, p1, p2, p3):
                return p1 * numpy.exp(p2 * time) + p3

#find optimal paramaters
            p0     = [1, 1e-6, 1]
            p, cov =  curve_fit(Yfit, time, ym, p0)

# calculate prediction
            yp = Yfit(time, p[0], p[1], p[2])

# calculate r^2
            r_square = r2_score(ym, yp)

# plot data and prediction
            figure   = pyplot.figure()
            title    = pyplot.title('fit model,' + soil + treatment)
            ylabel   = pyplot.ylabel('respiration rate')
            xlabel   = pyplot.xlabel('time[h]')
            legend   = pyplot.legend(loc='best')
            r_2_text = pyplot.text(0.1, 0.7, ('r_square:' + str(r_square)))

            pyplot.plot(ym, 'r--', label='measured')
            pyplot.plot(yp, 'b--', label='predicted')

            variables = (soil, treatment, step)
            figure.savefig('./cumulative_resp/%s-%s-%s.png' % variables)

            pyplot.cla()


# todo fit an equation for data points of means for every soil on every week of incubation using scipy curve_fit
# todo iterate through the three soils both in control and treatment means and do this with an exponential equation
#    as well as a power function ( https://www.youtube.com/watch?v=sGZbQgDOfi4 )