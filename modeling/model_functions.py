import numpy
from numpy import exp




def delay_coefficient(t, delay):
    coefficient = numpy.zeros(len(t))
    coefficient[numpy.where(t > delay)] = 1

    return coefficient



# rate of product accumulation
def rate(t, A, k):
    return A * (exp(-k * (t - 0.5)) - exp(-k * (t + 0.5)))

# respiration rate
def resp_rate_entire_incubation(t, a, k):

    c1 = delay_coefficient(t, 7)
    c2 = delay_coefficient(t, 14)

    return rate(t, a, k) + c1 * rate(t - 7, a, k) + c2 * rate(t - 14, a, k)


# # concentration of 1st order reaction product
# def conc(t, a, k):
#     return a * (1 -exp(-k*t))


# weekly growth and decay
def growth_decay(t, A, k_a, k_b):

    # concentration of 1st order reaction product
    def conc(t, a, k):
        return a * (1 - exp(-k * t))

    return conc(t, A, k_a) - conc(t, A, k_b)


# microbial carbon
def weekly_growth_decay(t, A, k_g, k_d):

    c1 = delay_coefficient(t, 7)
    c2 = delay_coefficient(t, 14)

    return growth_decay(t, A, k_g, k_d) + \
           c1 * growth_decay(t - 7, A, k_g, k_d) \
           + c2 * growth_decay(t - 14, A, k_g, k_d)
