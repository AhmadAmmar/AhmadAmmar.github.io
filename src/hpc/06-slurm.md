---
title: Running jobs with Slurm
slug: slurm
description: Interactive and batch jobs, every setting in a job script, and how to choose resources.
---

## Two ways to run

| | `srun ... --pty bash` | `sbatch script.sh` |
|---|---|---|
| Style | Interactive: you get a shell on a compute node | Hand it in and walk away |
| Good for | Short tests, installs | All real work |
| If you disconnect | Work stops | It carries on |

## A first job

Save this as `first.sh`:

```bash
#!/bin/bash
# The first line (the "shebang") says which program should run this file.

# Lines starting #SBATCH are instructions to Slurm. They must come before any command.
#SBATCH --job-name=first             # a label for the queue
#SBATCH --time=00:05:00              # limit: hours:minutes:seconds. The job is stopped at this point
#SBATCH --cpus-per-task=2            # cores for this job
#SBATCH --mem=2G                     # memory for this job
#SBATCH --output=first_%j.out        # where printed output goes; %j becomes the job ID

hostname                             # which node am I on?
nproc                                # how many cores did I get?
date                                 # when did it run?
```

```bash
# cluster
sbatch first.sh                # hand it in. Prints: Submitted batch job <jobid>
squeue -u $USER                # my jobs. PD means pending, R means running
cat first_<jobid>.out          # read what it printed
```

When your job vanishes from `squeue`, it has ended, either successfully or not, so always read the log. By default a job starts in the folder from which you submitted it.

## The settings you need

| Setting | Meaning | Choosing it |
|---|---|---|
| `--job-name` | A label | Short and useful |
| `--time` | Hard limit, also `days-hh:mm:ss` | Run a test, and add a margin. An accurate limit helps a job start sooner |
| `--cpus-per-task` | Cores for a threaded program | Only what it can actually use |
| `--ntasks` | Separate processes, as in MPI | 1, unless you use MPI |
| `--nodes` | Number of nodes | Usually leave it, unless using MPI |
| `--mem` or `--mem-per-cpu` | Memory | Check real use with `sacct`, then trim it |
| `--partition` or `-p` | Which queue | See below |
| `--output`, `--error` | Files for printed output and errors | Use `%x` job name, `%j` job ID, `%A` array ID, `%a` task number. The folder must already exist, or the log is lost |
| `--array` | Many tasks; see the next chapter | |
| `--gres=gpu:<type>:1` | A GPU | Only on GPU partitions, and only if your code uses it |
| `--mail-type`, `--mail-user` | Email on start and end | Handy for long jobs; avoid it for arrays |

The definitive list is in the [`sbatch` manual](https://slurm.schedmd.com/sbatch.html).

Partitions, **Kelvin2 only**, from [Running Jobs](https://ni-hpc.github.io/nihpc-documentation/Running%20Jobs/); check there for changes:

| Partition | Time limit | For |
|---|---|---|
| `k2-hipri` (default) | 3 hours | Short jobs |
| `k2-medpri` | 24 hours | Longer jobs |
| `k2-lowpri` | Not listed | Long jobs |
| `k2-himem` | 3 days | Very large memory |
| `k2-gpu-*` | 3 days | GPUs |
| `k2-sandbox` | See `sinfo` | Testing, per the Green HPC page |

## Watching and managing

```bash
# cluster
squeue -u $USER                 # my queued and running jobs
squeue -u $USER -h | wc -l      # -h removes the header, so this counts my jobs
scancel <jobid>                 # cancel a job
scancel -u $USER                # cancel all my jobs. Careful
sinfo -s                        # a summary of partitions
sacct -j <jobid> --format=JobID,Elapsed,MaxRSS,State    # after it ends: time, peak memory, outcome
```

Job states you will see include `COMPLETED`, `FAILED`, `TIMEOUT` (it hit `--time`), and `OUT_OF_MEMORY`.

## Start small

Test on a tiny case before running at scale. A good first job proves that it runs on a compute node (`hostname`), has the cores you asked for (`nproc`), finds your software, and can see your files. NI-HPC's [Green HPC page](https://ni-hpc.github.io/nihpc-documentation/Green%20HPC/) makes the same point on carbon grounds: failed jobs waste energy too.
