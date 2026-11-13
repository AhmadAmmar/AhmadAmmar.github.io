#!/bin/bash
#SBATCH --job-name=decades
#SBATCH --time=00:02:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=500M
#SBATCH --array=0-14
#SBATCH --output=logs/%x_%A_%a.out

# 15 tasks: 0 is the 1870s and 14 is the 2010s.
python3 05_decade.py
