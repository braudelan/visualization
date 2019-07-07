import numpy
from numpy import pi, sin, exp
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Setup
N_HARMONICS = 1000

# bn coefficient
def bn(n):
    n = int(n)
    if (n%2 != 0):
        return 2/(pi*n)
    else:
        return 0

# Wn
def wn(n):
    wn = (2*pi*n)/28
    return wn


# Fourier Series approximating a square wave alternating between 0 and 1 with delay
def delay_factor(x, delay):
    a0 = 0.5
    partialSums = a0
    for n in range(1, N_HARMONICS):
        partialSums = partialSums + bn(n) * sin(wn(n) * (x - delay))
    return partialSums

a = 125
k = 0.5
def rate_unit(x):
    return a * ( exp(-k*(x-0.5)) - exp(-k*(x+0.5)))




# ploting
X = numpy.linspace(0.1, 43, 10000)
plt.style.use("ggplot")
major_ticks = numpy.arange(0, 43, 7)

all = []
one_delay = []
first_delay_factor = []
seconed_delay_factor = []
d0 = 0
d1 = 7
d2 = 14
for i in X:
    all.append(delay_factor(i,0)*rate_unit(i) + delay_factor(i,d1)*rate_unit(i-d1) + delay_factor(i,d2)*rate_unit(i-d2))
    one_delay.append(rate_unit(i) + delay_factor(i,d1)*rate_unit(i-d1))
    first_delay_factor.append(delay_factor(i,d1))
    seconed_delay_factor.append(delay_factor(i, d2))

plt.plot(X,all,color="red", label='all')
plt.plot(X,one_delay,color="blue", label='one_delay')
plt.plot(X,first_delay_factor,color="green", label='fisrt_factor')
plt.plot(X,seconed_delay_factor, color="yellow", label='seconed_factor')



plt.xticks(major_ticks, list(major_ticks))
plt.title("square wave, delay = " + str())
plt.legend()
plt.savefig('/home/elan/Desktop/both.png')
plt.cla
