#!/bin/bash
#SBATCH --job-name=tiles
#SBATCH --time=00:02:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=500M
#SBATCH --array=0-7
#SBATCH --output=logs/%x_%A_%a.out

# Run python3 07_make_tiles.py once before submitting this.
python3 07_tile_ndvi.py
