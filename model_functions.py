import numpy
from numpy import exp


def delay_coefficient(t, delay):
    coefficient = numpy.zeros(len(t))
    coefficient[numpy.where(t > delay)] = 1

    return coefficient


# first order reaction functions
def first_order(time, initial_conc, rate_constant):
    return initial_conc * (1 -exp(-rate_constant*time))

def first_order_rate(time, initial_conc, rate_constant):
    return initial_conc * (exp(-rate_constant * (time - 0.5)) - exp(-rate_constant * (time + 0.5)))


# respiration rate cycles
def respiration_rate(t, a, k):

    c1 = delay_coefficient(t, 7)
    c2 = delay_coefficient(t, 14)

    return first_order_rate(t, a, k) + c1 * first_order_rate(t - 7, a, k) + c2 * first_order_rate(t - 14, a, k)


# microbial growth and decay
def growth_decay(time, initial_growth, initial_decay, k_growth, k_decay):
    return first_order(time, initial_growth, k_growth) - first_order(time, initial_decay, k_decay)

# microbial carbon cycles
def microbial_carbon(t, a, b, k_a, k_b):

    c1 = delay_coefficient(t, 7)
    c2 = delay_coefficient(t, 14)

    return growth_decay(t, a, b, k_a, k_b) + \
                            c1 * growth_decay(t-7, a, b, k_a, k_b) + c2 * growth_decay(t-14, a, b, k_a, k_b)