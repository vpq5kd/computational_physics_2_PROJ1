import numpy as np
import matplotlib.pyplot as plt


fig, ax = plt.subplots(1,2)

labelpad = 15
markersize = 3
colors = ['purple', 'green', 'lightskyblue']
markers = ['+', 'x', 's']
iterator = 0

Ns = [30,60,120]
T_c = 2.269

for N in Ns:
    data = np.load(f"working_data/ising_results_{N}.npz")
    T = data["T"]
    energy = data["energy"]
    energy2 = data["energy2"]
    magnetization = data["magnetization"]
    magnetization2 = data["magnetization2"]
    magnetization4 = data["magnetization4"]

    B_4 = 1 - (magnetization4/(3*(magnetization2)**2))
    FSS = (T-T_c)*N

    ax[0].plot(T,B_4,color=colors[iterator],label=N)
    ax[1].plot(T,FSS,color=colors[iterator],marker=markers[iterator],markerfacecolor='None')
    iterator+=1

ax[0].set_xlabel("Temperature")
ax[0].set_ylabel(r"$B_{4}$",rotation = 0, labelpad=labelpad)
ax[0].set_ylim(0.2,0.7)

ax[1].set_xlabel(r"$(T-T_{c})L^{\frac{1}{v}}$")
ax[1].set_ylabel(r"$B_{4}$",rotation=0,labelpad=labelpad)

fig.legend(loc='upper right')
fig.tight_layout()

plt.show()
    
