#!/bin/bash
#SBATCH --job-name  ARG_CNT_15
#SBATCH --partition batch
#SBATCH -N          8
#SBATCH --ntasks    192
#SBATCH --time      72:00:00
#SBATCH --output    ARG_CNT_15.out
#SBATCH --error     ARG_CNT_15.err

module load tryton/gaussian/g16.c01

g16 ARG_CNT_15.com > ARG_CNT_15.log

