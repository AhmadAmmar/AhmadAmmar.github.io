---
title: "Other clusters, the cloud and Linux basics"
slug: beyond
description: Translating these skills to other schedulers and cloud computing, with the everyday Linux administration a researcher needs.
---

Nearly everything in this guide carries over. A new system mostly changes the names, the storage rules and who pays. This chapter is a map to help you adapt, and each system's own documentation has the final word.

## A checklist for any new system

1. Who can use it, and how do I apply?
2. How do I log in: which address, port, keys and multi-factor steps?
3. Which storage is backed up, which is fast, and how much do I have?
4. Which scheduler does it use, and which partitions or queues?
5. How is software provided: modules, containers, or my own installs?
6. What are the limits on time, memory and number of jobs?
7. How should I acknowledge it in publications?

Then run Exercise 1 of this guide. If that works, the rest will follow.

## Other schedulers

Slurm is common but not universal. The ideas match, while the words differ.

| Task | Slurm | PBS / Torque | Grid Engine | LSF |
|---|---|---|---|---|
| Submit | `sbatch` | `qsub` | `qsub` | `bsub` |
| See the queue | `squeue` | `qstat` | `qstat` | `bjobs` |
| Cancel | `scancel` | `qdel` | `qdel` | `bkill` |
| Script directive | `#SBATCH` | `#PBS` | `#$` | `#BSUB` |
| Array task number | `$SLURM_ARRAY_TASK_ID` | `$PBS_ARRAYID` or `$PBS_ARRAY_INDEX` | `$SGE_TASK_ID` | `$LSB_JOBINDEX` |

## Cluster or cloud?

| | Shared cluster | Cloud |
|---|---|---|
| Cost | Usually free or allocated to researchers | Paid by use, so a forgotten machine keeps charging |
| Waiting | A queue | Usually starts at once |
| Control | Fixed system; no administrator rights | You control the machine, and so must secure and maintain it |
| Best for | Large batches, shared storage | Special hardware, short bursts, web services |

A cloud virtual machine feels familiar: you create it, log in with SSH using the same kind of key, and run commands on Linux. The usual pattern is:

1. Set a budget alert before you start anything.
2. Create the smallest machine that does the job, and allow SSH only from your own address where you can.
3. Keep data in object storage, such as S3-style buckets, as a machine's own disk may be deleted with it.
4. Run long work inside `tmux`, described below, so that it survives a dropped connection.
5. Stop or delete the machine when you finish. Check that its disks and addresses are gone too, as they can keep charging.

For many tasks, services such as AWS Batch, Azure Batch and Google Cloud Batch offer something like a job array, and some providers can build a Slurm cluster for you. Containers from the software chapter move well between all of these.

## Linux basics for looking after your own work

### Permissions

Every file has an owner and a group, with read (`r`), write (`w`) and execute (`x`) rights for each.

```bash
# any Linux system
# Shows, for example, -rwxr-x--- : owner all, group read and run, others nothing
ls -l run.sh
# Let yourself run a script
chmod u+x run.sh
# Keep a private SSH key readable only by you. SSH refuses keys left more open
chmod 600 ~/.ssh/my-key
```

### Space

```bash
# any Linux system
# How full are the disks?
df -h
# What is using the space here, biggest last?
du -sh * | sort -h
```

Many clusters have their own command for your quota. Check its documentation.

### Processes

```bash
# any Linux system
# A live view of what is running. Press q to leave
top
# Just your own programs
ps -u $USER
# Stop a process politely, using its number from ps
kill <process id>
```

On a cluster, stop jobs with `scancel`, not `kill`.

### Sessions that survive a disconnection

`tmux` keeps a terminal running on the remote machine after you leave.

```bash
# any Linux system
tmux new -s work
# Do your work, then press Ctrl-b, then d, to leave it running
# Come back later
tmux attach -t work
```

On a cluster, use it for light work on login nodes. Heavy work still belongs in jobs.

### Scheduled tasks

`cron` runs commands at set times on a machine you manage. Edit your list with `crontab -e`. This line runs a backup at 02:00 every day:

```bash
0 2 * * * /home/me/backup.sh >> /home/me/backup.log 2>&1
```

Check whether your cluster allows it before relying on it.

### Installing system software

On your own machine or cloud server, you have administrator rights through `sudo`:

```bash
# Debian or Ubuntu
sudo apt update && sudo apt install tmux
# Red Hat, Rocky or Fedora
sudo dnf install tmux
```

On a shared cluster you will not have `sudo`. Use modules, conda or containers.

### Keeping your own server safe

If you run a cloud machine, its security is your job. Log in with keys and not passwords, apply updates regularly, open only the network ports you need, keep secrets out of git, and keep backups somewhere else. Test that you can restore them.
