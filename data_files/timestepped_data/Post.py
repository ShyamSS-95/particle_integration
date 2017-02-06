import numpy as np
import pylab as pl
import h5py

pl.rcParams['figure.figsize']  = 12, 7.5
pl.rcParams['lines.linewidth'] = 1.5
pl.rcParams['font.family']     = 'serif'
pl.rcParams['font.weight']     = 'bold'
pl.rcParams['font.size']       = 20  
pl.rcParams['font.sans-serif'] = 'serif'
pl.rcParams['text.usetex']     = True
pl.rcParams['axes.linewidth']  = 1.5
pl.rcParams['axes.titlesize']  = 'medium'
pl.rcParams['axes.labelsize']  = 'medium'

pl.rcParams['xtick.major.size'] = 8     
pl.rcParams['xtick.minor.size'] = 4     
pl.rcParams['xtick.major.pad']  = 8     
pl.rcParams['xtick.minor.pad']  = 8     
pl.rcParams['xtick.color']      = 'k'     
pl.rcParams['xtick.labelsize']  = 'medium'
pl.rcParams['xtick.direction']  = 'in'    

pl.rcParams['ytick.major.size'] = 8     
pl.rcParams['ytick.minor.size'] = 4     
pl.rcParams['ytick.major.pad']  = 8     
pl.rcParams['ytick.minor.pad']  = 8     
pl.rcParams['ytick.color']      = 'k'     
pl.rcParams['ytick.labelsize']  = 'medium'
pl.rcParams['ytick.direction']  = 'in'    

h5f = h5py.File('solution_200.h5', 'r')
sol = h5f['sol'][:]
p   = h5f['kinetic_energy'][:]
time = h5f['time'][:]
h5f.close()

"""
pl.title('$\mathrm{Pressure/HeatFlux}$')
pl.xlabel('$t$')
pl.plot(time[:-1],heatflux_x[:-1],'b',label='$<v^2v_x>$')
pl.plot(time[:-1],heatflux_y[:-1],'g',label='$<v^2v_y>$')
pl.plot(time[:-1],heatflux_z[:-1],'y',label='$<v^2v_z>$')
pl.plot(time[:-1],pressure[:-1],'r',label='$<v^2>$')
pl.legend(loc='center right')
pl.savefig('plot.png')
"""
k=m=1
theta=0.333
v0=np.zeros(10000)
y1=sol[10000:20000]
y2=sol[30000:40000]
v0=np.sqrt(y1**2+y2**2)
f_numerical1, v1, patches = pl.hist(v0, bins=20,normed='True')
pl.clf()
pl.plot(v1[:-1], f_numerical1,'g',label='$\mathrm{Obtained}$')
an=2*np.pi*v1*(m/(2*np.pi*k*theta))**(2./2.) * np.exp(-m*v1**2./(2.*k*theta))
pl.plot(v1, an, color='red',label='$\mathrm{Expected}$')
pl.legend()
pl.title('$\mathrm{Final}$ $\mathrm{Velocity}$ $\mathrm{Distribution}$')
pl.xlabel('$v$')
pl.ylabel('$\phi(v)$')
pl.savefig('FinalDistribution.png')
pl.clf()

#pl.plot(time[:], mom_x[:-1], label='$p_x$')
#pl.plot(time[:-1], mom_y[:-1], label='$p_y$')
pl.plot(time[:100], p[:100], label='$E$')
pl.title('$\mathrm{Variation}$ $\mathrm{Of}$ $\mathrm{Energy}$')
pl.xlabel('$\mathrm{Time}$')
pl.savefig('EnergyMomentumPlots.png')