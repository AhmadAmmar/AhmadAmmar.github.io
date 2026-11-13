#!/bin/bash
#SBATCH --job-name=add
#SBATCH --time=00:02:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=500M
#SBATCH --output=logs/%x_%j.out

# If python3 is not found, load a module first. Find one with: module avail python
python3 --version
python3 02_add.py 1 1
python3 02_add.py 21 21
