#!/bin/bash
#SBATCH --job-name=cities
#SBATCH --time=00:02:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=500M
#SBATCH --output=logs/%x_%j.out

# Change the city name to any in data/cities_natural_earth.csv.
python3 06_cities.py London
