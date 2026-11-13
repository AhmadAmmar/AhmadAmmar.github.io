#!/bin/bash
#SBATCH --job-name=armagh
#SBATCH --time=00:02:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=500M
#SBATCH --output=logs/%x_%j.out

python3 04_armagh.py
