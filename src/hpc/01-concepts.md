---
title: What a cluster is
slug: concepts
description: Nodes, cores, memory, schedulers and the kinds of parallel work, explained from scratch.
---

## The idea

Picture a laptop as one cook in one kitchen. A cluster is a building with hundreds of kitchens, each with dozens of cooks. It rarely makes one cook much faster. What it gives you is the ability to cook thousands of dishes at once, or to share out one enormous dish. There is a reception desk where you hand in orders, and a head waiter who decides which kitchen is free.

| Word | Meaning | In the picture |
|---|---|---|
| Node | One computer in the cluster | A kitchen |
| Core | One independent processing unit in a node; it runs one stream of instructions at a time | A cook |
| Memory (RAM) | Fast working space that empties when the job ends | The worktop |
| Login node | The computer you arrive at. For editing, moving files and submitting work | Reception |
| Compute node | Where jobs run | The kitchens |
| Scheduler | Software that queues jobs and allocates resources. Slurm (Yoo et al., 2003) is widely used | The head waiter |
| Partition | A named queue of nodes with its own rules | A type of kitchen |
| Job | One piece of work submitted to the scheduler | An order |

The login node is shared with everyone. **Do not run heavy work there**: it slows the system for others, and your process may be killed.

## Do you need one?

A cluster helps when your work is too big, too long or too repetitive for your computer. It will not speed up one ordinary program that can only use a single core, beyond any difference in the processor. Three common patterns:

| Pattern | Example | What it needs |
|---|---|---|
| Many independent runs, called "many-task" (Raicu et al., 2008) or "embarrassingly parallel" | A parameter sweep, or one analysis per file | Job arrays. Often no code changes |
| One program sharing memory on a node | A threaded model, or machine learning on many cores | `--cpus-per-task`, and a program that can use them |
| One program across nodes | A large fluid simulation, using MPI | `--ntasks`, `--nodes`, and an MPI-aware program |

Asking for more cores does not by itself make a program use them. Even a parallel program has limits: the part that cannot be shared sets a ceiling on the speed-up, an idea known as Amdahl's law (Amdahl, 1967). If 10% of the work must run in series, then no number of cores can make it more than 10 times faster.

This guide concentrates on the first pattern, which is what many researchers need first. The habits in Wilson et al. (2014) are worth reading too.

## Kelvin2 in brief

**Kelvin2 only.** The [official pages](https://www.qub.ac.uk/sites/ni-hpc/Kelvin2/) describe about 100 standard compute nodes with 128 cores each (two AMD EPYC 7702 processors) and nearly 800 GB of memory, 8 high-memory nodes, GPU nodes, and 2 PB of scratch storage, joined by InfiniBand networking. Figures differ slightly between NI-HPC's pages and change over time. To see what exists now, use `sinfo`.

Access is for researchers at Queen's University Belfast and Ulster University, and others through national schemes: see NI-HPC's [access page](https://www.qub.ac.uk/sites/ni-hpc/Kelvin2/Access/). The [acceptable use policy](https://ni-hpc.github.io/nihpc-documentation) is on the documentation home page. Read it first.
