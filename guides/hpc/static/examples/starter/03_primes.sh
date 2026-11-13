#!/bin/bash
#SBATCH --job-name=primes
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=1G
#SBATCH --output=logs/%x_%j.out

# Try --cpus-per-task=1, 2 and 4, then compare the times. Do the answers match?
python3 03_primes.py 1000000
