---
title: Getting started on an HPC cluster
slug: index
description: A from-scratch tutorial on high-performance computing for researchers, with worked examples on NI-HPC's Kelvin2 that carry over to other Slurm clusters.
---

This is the guide I wanted when I first logged into a supercomputer as a PhD researcher. I trained in geo-informatics and remote sensing, which combine geography, geospatial science, programming and mathematics, yet a shared supercomputer was still new to me. It assumes you have never used a command line. By the end, you will have logged in securely, moved files, installed software, built confidence with seven small practice jobs on real data, and run a parameter sweep of many jobs. A final chapter carries these skills to other clusters, the cloud and everyday Linux administration.

The examples use [Kelvin2](https://ni-hpc.github.io/nihpc-documentation), the cluster run by the Northern Ireland High Performance Computing service (NI-HPC). Most of what you learn carries over to any Linux cluster that uses the Slurm scheduler. **Kelvin2 only** marks details specific to that system; check your own cluster's documentation for the equivalents.

## How to use it

Prefer one long page? [Read the whole tutorial on one page](full/).

Read in order if you are new, or jump in if you are not. Blocks of code are labelled with where they run, because typing a command on the wrong computer is the most common beginner's mistake:

- `laptop` means a terminal on your own computer.
- `cluster` means after you have logged in.

Lines beginning with `#` are comments, which the computer ignores. In this guide, they explain the line beneath them. Anything in `<angle brackets>` is a placeholder to replace, without keeping the brackets.

## Practice files

The [starter kit](https://ahmadammar.github.io/teaching/hpc/examples/hpc-starter-kit.zip) holds small programs and open data for [the exercises](https://ahmadammar.github.io/teaching/hpc/first-jobs/). Start there if you learn best by doing.

## Other good guides

This guide is my own, written from setting up on Kelvin2, and it is not an official NI-HPC document. Always treat the official documentation as the authority on your cluster's rules.

- [NI-HPC documentation](https://ni-hpc.github.io/nihpc-documentation): the official reference for Kelvin2.
- [Introduction to high performance computing](https://iamdonovan.github.io/teaching/hpc-intro/index.html) by Bob McNabb: a workshop on the shell and on running jobs, on two other university clusters. I recommend it alongside this guide.
- [The Unix Shell](https://swcarpentry.github.io/shell-novice/) from Software Carpentry, and [Introduction to High-Performance Computing](https://carpentries-incubator.github.io/hpc-intro/) from HPC Carpentry.

Corrections are welcome: contact details are at the foot of the page.
