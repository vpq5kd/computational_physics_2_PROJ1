import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser('2D ising simulation')
parser.add_argument('--outfile_location',type=str)
parser.add_argument('--filename', type=str)
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
    
    try:
        data = np.load(f"{args.outfile_location}/ising_results_{N}.npz")
    except:
        print(f"{N} not found, continuing to next iteration.")
        continue

    T = data["T"]
    energy = data["energy"]
    energy2 = data["energy2"]
    magnetization = data["magnetization"]
    magnetization2 = data["magnetization2"]
    magnetization4 = data["magnetization4"]
    magnetizationAbs = data["magnetizationAbs"]

    B_4 = 1 - (magnetization4/(3*(magnetization2)**2))
    FSS = (T-T_c)*N

    ax[0].plot(T,B_4,color=colors[iterator],label=N)
    ax[1].plot(FSS,B_4,color=colors[iterator],marker=markers[iterator],markerfacecolor='None',linestyle='None',label=N)

    iterator+=1


ax[0].set_xlabel(r"$T$")
ax[0].set_ylabel(r"$B_{4}$",rotation = 0, labelpad=labelpad)
ax[0].set_ylim(0.2,0.7)
ax[0].set_xlim(2.1,2.4)
ax[0].legend(loc='upper right')

ax[1].set_xlabel(r"$(T-T_{c})L^{\frac{1}{\nu}}$")
ax[1].set_ylabel(r"$B_{4}$",rotation=0,labelpad=labelpad)
ax[1].set_xlim(-20,30)
ax[1].set_ylim(0,0.7)
ax[1].legend(loc='upper right')

fig.tight_layout()
plt.savefig(f'{args.filename}')
plt.show()
    
