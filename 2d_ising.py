import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

rng = np.random.default_rng()

parser = argparse.ArgumentParser('2D ising simulation')
parser.add_argument('--melting_iterations', type=int)
parser.add_argument('--measuring_iterations', type=int)
parser.add_argument('--outfile_location',type=str)
args = parser.parse_args()

def hamiltonian(spins, J=1):
    N = spins.shape[0]
    energy = 0
    
    for i in range(N):
        for j in range(N):
            s = spins[i, j]
            
            right = spins[i, (j + 1) % N]
            down  = spins[(i + 1) % N, j]
            
            energy += -J * s * right
            energy += -J * s * down
            
    return energy

def vectorized_hamiltonian(spins, J=1):
    return -J * (np.sum(spins * np.roll(spins, 1, axis=0)) + np.sum(spins * np.roll(spins, 1, axis=1)))

def magnetization(spins):
    return np.sum(spins)

def wolff_cluster_logic(N, T, spins):

    random_site_x = rng.integers(N)
    random_site_y = rng.integers(N)

    random_site = (random_site_x, random_site_y)
    cluster = set()
    cluster.add(random_site)
    f_old = set()
    f_old.add(random_site)

    while len(f_old) > 0:
        f_new = set()
        for test_pair in f_old:
            test_pair_x = test_pair[1]
            test_pair_y = test_pair[0]

            right = (test_pair_y, (test_pair_x + 1)%N)
            down = ((test_pair_y + 1)%N, test_pair_x)
            left = (test_pair_y, (test_pair_x - 1)%N)
            up = ((test_pair_y - 1)%N, test_pair_x)

            neighbors = [up, down, right, left]

            for neighbor in neighbors:

                neighbor_x = neighbor[1]
                neighbor_y = neighbor[0]

                if (neighbor not in cluster) and (spins[neighbor_y,neighbor_x] == spins[test_pair_y, test_pair_x]):

                    B = 1/T
                    if np.random.rand() < (1-np.exp(-2*B)):
                        f_new.add(neighbor)
                        cluster.add(neighbor)
        f_old = f_new
        
    for spin in cluster:
        x = spin[1]
        y = spin[0]
        spins[y,x]*=-1


def wolff_cluster(N, T, spins, melting_iterations, measuring_iterations):
    
    temp_energy_array = []
    temp_magnetization_array = []
    
    for i in range(melting_iterations):
        wolff_cluster_logic(N, T, spins)    
    
    for i in range(measuring_iterations):
        wolff_cluster_logic(N, T, spins)
        temp_energy_array.append(vectorized_hamiltonian(spins))
        temp_magnetization_array.append(magnetization(spins))
    
    e = np.array(temp_energy_array)
    m = np.array(temp_magnetization_array)

    return np.mean(e), np.mean(e**2), np.mean(m), np.mean(m**2), np.mean(m**4), np.mean(np.abs(m))
def temperature_logic(args):
    
    N, T, melting_iterations, measuring_iterations = args

    #spins_metropolis = np.random.choice([-1,1], size=(N,N))
    #spins_wolff = np.random.choice([-1,1], size=(N,N))

    spins_wolff = np.ones((N,N))

    wolff_energy, wolff_energy_squared, wolff_magnetization, wolff_magnetization_squared, wolff_magnetization_biquadrated, wolff_magnetization_absolute = wolff_cluster(N, T, spins_wolff, melting_iterations, measuring_iterations)

    return T, wolff_energy, wolff_energy_squared, wolff_magnetization, wolff_magnetization_squared, wolff_magnetization_biquadrated, wolff_magnetization_absolute

def run_sim(N, melting_iterations, measuring_iterations):
    
    temperature_array = np.linspace(1.8, 2.8, 50)[::-1]
    
    args = [(N, T, melting_iterations, measuring_iterations) for T in temperature_array]
    
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(tqdm(executor.map(temperature_logic, args), total=len(args)))

    T_arr, wolff_e_arr, wolff_e_2_arr, wolff_m_arr, wolff_m_2_arr, wolff_m_4_arr, wolff_m_abs = zip(*results)

    return np.array(T_arr), np.array(wolff_e_arr), np.array(wolff_e_2_arr), np.array(wolff_m_arr), np.array(wolff_m_2_arr), np.array(wolff_m_4_arr), np.array(wolff_m_abs)

def main():
    
    Ns = [30,60,120]
    melting_iterations = args.melting_iterations
    measuring_iterations = args.measuring_iterations
    

    for N in Ns:
        
        temperature_array, wolff_energy_array, wolff_energy_array_squared, magnetization_array, magnetization_array_squared, magnetization_array_biquadrated, magnetization_array_absolute = run_sim(N, melting_iterations, measuring_iterations)

        np.savez(f"{args.outfile_location}/ising_results_{N}.npz", T = temperature_array, energy=wolff_energy_array, energy2 = wolff_energy_array_squared, magnetization = magnetization_array, magnetization2=magnetization_array_squared, magnetization4=magnetization_array_biquadrated, magnetizationAbs=magnetization_array_absolute)

if __name__ == "__main__":
    main()
