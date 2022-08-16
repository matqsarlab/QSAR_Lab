#!/bin/bash
#SBATCH --job-name
#SBATCH --partition batch
#SBATCH -N          8
#SBATCH --ntasks    192
#SBATCH --time      72:00:00
#SBATCH --output
#SBATCH --error

module load tryton/gaussian/g16.c01

g16

