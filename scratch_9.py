import numpy
from numpy import pi, sin, exp
from matplotlib import pyplot

from get_raw_data import get_setup_arguments
from get_raw_data import get_raw_data, get_multi_sets
from get_stats import get_stats, get_carbon_stats, get_baseline
from square_wave import switch_on_off
from helpers import replace_nan, SOILS


# # setup and get data
# setup_arguments = get_setup_arguments()
# set_name = setup_arguments.sets[0]
# raw_data = get_raw_data(set_name)
# stats = get_stats(raw_data
#
# # specific data
# MRE = stats.MRE
# control = stats.control
# difference = MRE - control



X = numpy.linspace(0,14,10000)
N_HARMONICS = 1000

def decay_cycles(x, a, k, n_harmonics):

    return a * exp(-k * (x)) + switch_on_off(n_harmonics, x+7) * a * exp(-k * (x-7))

f = []
for i in X:
    f.append(decay_cycles(i, 125, 0.35,N_HARMONICS))

pyplot.plot(X,f,color="red",label="decay cycels")
pyplot.title("decay cycels" + str(N_HARMONICS))
pyplot.legend()
pyplot.show()
