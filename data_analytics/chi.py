import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser('2D ising simulation')
parser.add_argument('--outfile_location',type=str)
args = parser.parse_args()

fig, ax = plt.subplots(1,2)

labelpad = 15
markersize = 3
colors = ['purple', 'green', 'lightskyblue']
markers = ['+', 'x', 's']
iterator = 0

Ns = [30,60,120]
T_c = 2.269

for N in Ns:
    data = np.load(f"{args.outfile_location}/ising_results_{N}.npz")
    T = data["T"]
    energy = data["energy"]
    energy2 = data["energy2"]
    magnetization = data["magnetization"]
    magnetization2 = data["magnetization2"]
    magnetization4 = data["magnetization4"]
    magnetizationAbs = data["magnetizationAbs"]

    chi = (magnetization2 - (magnetizationAbs)**2)/(T*N**2)
    fss_chi = chi*N**(-7/4)
    FSS = (T-T_c)*N

    ax[0].plot(T,chi,color=colors[iterator],label=N)
    ax[1].plot(FSS,fss_chi,color=colors[iterator],marker=markers[iterator],markerfacecolor='None',linestyle='None',label=N)

    iterator+=1

ax[0].set_xlabel(r"$T$")
ax[0].set_ylabel(r"$\chi$",rotation = 0, labelpad=labelpad)
ax[0].set_ylim(0,400)
ax[0].legend(loc='upper right')

ax[1].set_xlabel(r"$(T-T_{c})L^{\frac{1}{\nu}}$")
ax[1].set_ylabel(r"$\chi L^{\frac{-\gamma}{\nu}}$",rotation=0,labelpad=labelpad)
ax[1].set_xlim(-20,30)
ax[1].set_ylim(0,0.05)
ax[1].legend(loc='upper right')

fig.tight_layout()
plt.savefig("data_analytics/graphs/chi.png")
plt.show()
    
