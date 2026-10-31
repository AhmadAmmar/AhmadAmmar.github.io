#!/bin/bash
#SBATCH --job-name=hello
#SBATCH --time=00:02:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=500M
#SBATCH --output=logs/%x_%j.out

# The simplest useful job: where am I, when is it, and can I do a sum?
echo "Hello from $(hostname)"
echo "The time is $(date)"
echo "Job $SLURM_JOB_ID, submitted from $SLURM_SUBMIT_DIR"
echo "1 + 1 = $(( 1 + 1 ))"
