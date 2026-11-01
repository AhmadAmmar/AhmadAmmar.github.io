---
title: Measuring and good practice
slug: practice
description: Wall time, core time, sacct, fair benchmarks and considerate use of a shared system.
---

## Words for time

| Term | Meaning |
|---|---|
| Wall time | Real time by the clock on the wall |
| Core time | Sum of the time on each core. 10 tasks of 1 minute each: 1 minute of wall time, 10 of core time |
| Queue wait | From submitting to starting |
| Speed-up | Old wall time / new wall time |
| Efficiency | Speed-up / number of cores used |

## Slurm's accounts

Slurm records everything, and `sacct` reads it back.

```bash
# cluster

# -X: whole jobs only. -P: separate columns with |, ready for a spreadsheet or pandas.
# -S: from this date. -o: which columns. > saves to a file
sacct -X -P -S 2026-01-01 -u $USER -o JobID,JobName,Submit,Start,End,Elapsed,State > jobs.txt
```

Times are in whole seconds, which is too coarse for tasks of a few seconds. Time those from inside the job with `date +%s.%N`.

## A measured example

The same prime-counting program from the exercises, up to 5 million, was run three times at each core count on Kelvin2 and on one laptop (Intel Core i5-10210U, 4 physical cores, doing other work at the time). Each cell is the middle of three runs. All 27 runs found the same answer, 348,513.

| Cores | Kelvin2 | Speed-up | Efficiency | Laptop | Laptop range |
|---:|---:|---:|---:|---:|---:|
| 1 | 46.0 s | 1.0x | 100% | 209 s | 125 to 255 s |
| 2 | 23.2 s | 2.0x | 99% | 125 s | 82 to 156 s |
| 4 | 12.0 s | 3.8x | 96% | 69 s | 66 to 105 s |
| 8 | 6.3 s | 7.3x | 91% | 61 s | 55 to 66 s |
| 16 | 3.7 s | 12.4x | 78% | n/a | n/a |

Three things are worth noticing:

- **Efficiency falls as cores rise**, because splitting and collecting work takes time. Sixteen cores gave 12.4 times the speed, not 16.
- **The laptop barely gains beyond 4 cores.** It has 4 physical cores, and its 8 are logical threads sharing them. Its times also vary widely, because it was busy, while Kelvin2's stayed within a fraction of a second. So don't read a single speed-up figure from this comparison.
- **Many jobs can run at once.** The 15 Kelvin2 jobs were submitted together in 2026, waited 10 seconds, and finished within 57 seconds. One after another they would take about 4.6 minutes.

This program is well suited to splitting up. Yours may not be, so measure it.

To repeat the test:

```bash
# cluster, in the starter kit folder
for r in 1 2 3; do for c in 1 2 4 8 16; do
  sbatch --job-name=t${c}_${r} --cpus-per-task=$c --mem=4G --time=00:30:00 \
    --output=logs/timing_${c}_${r}.out --wrap="python3 03_primes.py 5000000"
done; done
```

## Benchmarking fairly

Comparing a cluster with a laptop is easy to do badly.

- Compare like with like: same program, version, input and output settings.
- Report what you measured. "First task start to last task end" and "submission to finish" are different numbers.
- Separate setup from running. If your script copies files between submissions, you are timing the copying. I made this mistake in my own first test.
- Repeat. Shared systems vary with load. Report a range, not your best run.
- Say what you projected, and what you measured.
- Check that the answers match, not just the speed.

## Good habits

These follow the spirit of Wilson et al. (2014).

- Keep code in version control, such as git. Keep raw data unchanged, with scripts that make everything else from it.
- Never overwrite results. Use dated output folders: `outputs/$(date +%Y-%m-%d_%H%M)`.
- Record versions: `module list`, `conda env export`, `git rev-parse HEAD`.
- Keep job scripts, as they are the record of what you did.
- Make jobs restartable.
- Read your inputs back: check a run's settings, such as the simulated period, before you describe it.
- Copy results off scratch.

## Being a good neighbour

- No heavy work on login nodes.
- Ask for what you need, not the maximum. Over-asking makes your own job queue for longer, and blocks others.
- Avoid millions of tiny files. Pack them, or write summaries.
- Run only what you need. Smarter sampling can replace brute force, as NI-HPC's [Green HPC page](https://ni-hpc.github.io/nihpc-documentation/Green%20HPC/) notes.
- Read your cluster's acceptable use policy.
- Acknowledge the service in your papers. **Kelvin2:** "We are grateful for use of the computing resources from the Northern Ireland High Performance Computing (NI-HPC) service funded by EPSRC (EP/T022175)."
- When stuck, write to the support team with your job ID, the exact command and the error message.
