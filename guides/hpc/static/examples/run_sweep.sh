#!/bin/bash
# Runs a block of cases on one core, as one task of a Slurm job array.
#   sbatch --array=0-5 run_sweep.sh cases 5
# means: 6 tasks (numbered 0 to 5), with 5 cases per task, from the folder "cases".

# Lines starting #SBATCH are read by Slurm. To bash, they are just comments.
#SBATCH --job-name=sweep            # the label shown in the queue
#SBATCH --time=00:10:00             # hard limit, hours:minutes:seconds; the job is stopped when it is reached
#SBATCH --cpus-per-task=1           # one core: this program cannot use more
#SBATCH --mem=1G                    # memory for each task
#SBATCH --output=logs/%x_%A_%a.out  # %x job name, %A array job ID, %a task number; make logs/ first

IN="$1"                             # $1 is the first word after the script name
PER="${2:-5}"                       # $2 is the second word; :-5 means "use 5 if it is missing"

# Fill a bash array named CASES with the sorted file names.
# < <( ... ) feeds the output of a command into mapfile; -t removes the line endings.
mapfile -t CASES < <(ls "$IN"/case_*.json | sort)

# Slurm sets SLURM_ARRAY_TASK_ID for each task. $(( )) does whole-number arithmetic.
# Task 0 starts at case 0, task 1 at case 5, task 2 at case 10, and so on.
start=$(( SLURM_ARRAY_TASK_ID * PER ))

# ${CASES[@]:start:PER} means: PER items of the array, beginning at position start.
for f in "${CASES[@]:start:PER}"; do
  # ${f%.json} removes the ending .json. -f tests whether a file exists.
  # && continue skips to the next case if this one is done, so resubmitting is safe.
  [ -f "${f%.json}.out" ] && continue
  # || runs the echo only if python failed, leaving a line you can search for.
  python3 heat_loss.py "$f" || echo "FAILED $f"
done

echo "task $SLURM_ARRAY_TASK_ID finished its block, starting at case $start on $(hostname)"
