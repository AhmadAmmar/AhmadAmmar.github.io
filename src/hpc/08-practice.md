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
