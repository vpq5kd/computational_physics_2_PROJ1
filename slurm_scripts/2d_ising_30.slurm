#!/bin/bash

#Submit this script with: sbatch myjob.slurm

#SBATCH --time=24:00:00   # job time limit
#SBATCH --nodes=1   # number of nodes
#SBATCH --ntasks-per-node=1   # number of tasks per node
#SBATCH --cpus-per-task=40   # number of CPU cores per task
#SBATCH --partition=standard   # partition
#SBATCH --account=phys5640_chern   # allocation name
#SBATCH --output=slurm_scripts/slurm_outfiles/2d_ising_slurm_30.out

python 2d_ising_slurm.py --melting_iterations 5000 --measuring_iterations 1000000 -N 30 --outfile_location slurm_scripts/slurm_data
