import numpy as np
from statsmodels.formula.api import wls
import pandas

delay, weight, u, v = np.loadtxt('data.txt',usecols=(2,3,4,5),unpack=True)
c = 3e8
radtomas = 206264806.2471
# get u,v in the units of s, delay in the units of s*mas
u = u/c
v = v/c
delay = delay*radtomas

# convert weight to statsmodel language
w = weight**4
data = pandas.DataFrame({'x':u, 'y':v, 'z':delay})
model = wls('z ~ x ',data,weight=w)

results = model.fit()
print(results.summary())
print results.params
print results.cov_params()
print results.mse_resid/radtomas
