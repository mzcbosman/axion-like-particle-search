import numpy as np
import math
from matplotlib import pyplot as plt

Ma = 3*np.logspace(-2, 0.7, 100)  # GeV, from 0.03 to 3
# Ma = 1

BF = 4.58E-5  # actual value
# BF = 1E-6  # example from paper
tau = 1/(1.519E-12)  # decay rate [s-1]
c = 6.59E-25  # conversion [s-1Gev-1]

Mb = 5.280  # GeV
Mkst = 0.8917  # GeV

r1 = 1.364
r2 = -0.990
m2fit = 36.78

A0 = r1/(1-(Ma**2)/(Mb**2)) + r2/(1-(Ma**2)/(m2fit))

labda = (1-(Ma + Mkst)**2/(Mb**2))*(1-(Ma - Mkst)**2/(Mb**2))
gabs = (BF * tau * c * 64*np.pi*Mb**(-3)*A0**(-2)*labda**(-3./2.))**(1./2.)

MW = 80.4
GF = 1.1664E-5
Mc = 1.275
Mt = 173

Vcb = 0.0410
Vcs = 0.987
Vtb = 1.013
Vts = 0.0388

xc = Mc**2/MW**2
xt = Mt**2/MW**2

fc = xc*(1+xc*(np.log(xc)-1))/(1-xc)**2
ft = xt*(1+xt*(np.log(xt)-1))/(1-xt)**2

gaw = gabs*16*np.pi**2/(3*2**(1/2)*GF*MW**2)/(Vcb*Vcs*fc + Vtb*Vts*ft)

print(Ma)

plt.loglog(Ma, gaw)
plt.xlim(0.03, 6)
plt.ylim(5E-7, 1E-3)
plt.show()
