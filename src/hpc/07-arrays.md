---
title: "Job arrays: a parameter sweep"
slug: arrays
description: A complete worked example you can run, with every line explained, from generating inputs to collecting results.
---

Say you want to run one program on hundreds of inputs. Submitting hundreds of separate jobs is clumsy. A **job array** submits them as one, with each **task** told its number (SchedMD, n.d.).

This chapter builds a working sweep. Download the three files: [`heat_loss.py`](examples/heat_loss.py), [`make_cases.py`](examples/make_cases.py) and [`run_sweep.sh`](examples/run_sweep.sh). The "simulation" estimates a building's yearly heating need, but you can swap in your own program.

## The science in one paragraph

Heat flows out through a wall in proportion to its area, how leaky it is (its **U-value**, in W per m² per kelvin) and the temperature difference. Air leaking out takes heat too: warming 1 m³ of air by 1 K takes about 0.33 Wh. **Degree days** measure how cold a year is, summing how far each day falls below a base temperature. So heat in kWh per year is:

Q = (U × A + 0.33 × n × V) × DD × 24 / 1000

where A is wall area, n is air changes per hour, V is volume and DD is degree days.

## Step 1: the program

!include examples/heat_loss.py python

## Step 2: make the inputs

!include examples/make_cases.py python

Three settings, each with three values, give 3 × 3 × 3 = 27 combinations.

```bash
# cluster, in a project folder holding the three files

# Find your Python first. Look for a module with: module avail 2>&1 | grep -i python
module load <python-module>
python3 make_cases.py cases
ls cases | head                # case_000.json, case_001.json ...
python3 heat_loss.py cases/case_000.json && cat cases/case_000.out    # 11016.0
```

The last line is your test. For the first case, U = 2.1, A = 90, n = 1, V = 200 and DD = 1800, so by hand: (189 + 66) × 1800 × 24 / 1000 = 11016. Then delete that output, with `rm cases/case_000.out`, so that the job below runs every case.

## Step 3: the job script

Running one input per task works, but very short tasks are wasteful, because starting each one has a cost. So **pack** several runs into each task.

!include examples/run_sweep.sh bash

Add your `module load` line just before the `mapfile` line. Slurm usually passes your session's environment on to the job, but stating it in the script is what makes the job repeatable.

## Step 4: how many tasks?

With N cases and P per task, divide and round up, so that the last few cases are covered. Tasks are numbered from 0. For 27 cases at 5 per task, that is 6 tasks, numbered 0 to 5.

```bash
# cluster

# Line endings, if you edited on Windows
sed -i 's/\r$//' run_sweep.sh

# The log folder must exist before submission
mkdir -p logs

# Count the cases, and work out the last task number
N=$(ls cases/case_*.json | wc -l)
PER=5
# In whole-number arithmetic, (N + P - 1) / P rounds up
LAST=$(( (N + PER - 1) / PER - 1 ))
echo "$N cases, tasks 0 to $LAST"

sbatch --array=0-$LAST run_sweep.sh cases $PER
```

A useful extra: `--array=0-99%10` runs at most 10 tasks at once, which is polite on a busy system.

## Step 5: did it all work?

```bash
# cluster
squeue -u $USER                       # wait until it is empty
ls cases/*.out | wc -l                # expect 27
grep -l FAILED logs/*.out | wc -l     # expect 0
tail -2 logs/sweep_*_0.out            # read one log
```

If some failed, resubmit the same command. Because each task skips cases that already have an output, only the missing ones run. Being safe to re-run like this makes large runs much less stressful.

## Step 6: collect the results

```bash
# cluster
# A loop that prints each case's name and answer into a CSV file.
# ${f%.out} strips the ending, and $(cat "$f") inserts the file's contents
for f in cases/*.out; do echo "$(basename "${f%.out}"),$(cat "$f")"; done > results.csv
head -3 results.csv
```

```powershell
# laptop
scp kelvin:~/project/results.csv "D:\My Work"
```

## Choosing a packing

| | Few runs per task (many tasks) | Many runs per task (few tasks) |
|---|---|---|
| Finishes | Sooner, if cores are free | Later: each task takes longer |
| Overhead | Higher: more starts, more load on the scheduler | Lower |
| After a failure | Less lost | More to redo, unless it is restart-safe |

There is no single right answer. Test with your own program, with care: submit each setting separately, repeat it, and keep the copying of files out of your timing. If you are planning a very large run, ask your support team what they prefer.
