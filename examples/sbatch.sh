#!/bin/sh

##SBATCH --job-name=
##SBATCH --array=
##SBATCH --time=
##SBATCH --ntasks=
##SBATCH --cpus-per-task=
##SBATCH --ntasks-per-node=
##SBATCH --output=
##SBATCH --exclusive
##SBATCH --constraint=
##SBATCH --partition=

srun ./$1
