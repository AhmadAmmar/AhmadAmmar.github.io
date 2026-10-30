---
title: Files and storage
slug: files
description: Where to keep things on a cluster, and how to move data in and out.
---

## Where things go

Clusters have several storage areas with different rules. Learn yours before you create anything big.

**Kelvin2 only**, according to the [quick-start guide](https://ni-hpc.github.io/nihpc-documentation/Quickstart%20Guide/):

| Area | Path | Limit | Deletion |
|---|---|---|---|
| Home | `/users/$USER` | 50 GB and 100k files | None automatic |
| Scratch | `/mnt/scratch2/users/$USER` | No per-user quota | **After 90 days without access** |
| Temp | `/tmp` on each node | The node's disk | When the session ends |
| McClayRDS | Project paths | By project | QUB projects only |

`quota -s` shows your actual allocation.

The key rule: **scratch is not a backup and not an archive.** Keep a copy of results that matter on your institution's storage, and ask your support team what, if anything, is backed up.

## A tidy project

```bash
# cluster

# Braces expand: this makes all four folders
mkdir -p ~/project/{code,jobs,logs,envs}

# Big data lives on scratch
mkdir -p /mnt/scratch2/users/$USER/project/{data,outputs,tmp}

# A shortcut, so ~/project/scratch stands for the long path
ln -s /mnt/scratch2/users/$USER/project ~/project/scratch
```

## Moving files with scp

`scp source destination` copies securely. A remote location is written `kelvin:path`, using your shortcut. **Run it from your laptop**, in a separate terminal from your cluster session.

```powershell
# laptop

# Upload a file. Quotes are needed because of the space in the path
scp "D:\My Work\data.csv" kelvin:~/project/scratch/data/

# Upload a folder: -r means recursive
scp -r "D:\My Work\code" kelvin:~/project/

# Download: the source is now the remote one
scp kelvin:~/project/scratch/outputs/results.tgz "D:\My Work"
```

Without the shortcut, the port needs a **capital** `-P`, unlike `ssh`, which uses a lower-case `-p`:

```powershell
# laptop
scp -P 55890 -i $HOME\.ssh\my-kelvin-key data.csv <username>@login.kelvin.alces.network:~/project/
```

**A Windows trap.** Do not end a quoted folder with a backslash. In `"D:\My Work\"`, the `\"` is read as a literal quote mark, and you get a confusing "No such file or directory". Write `"D:\My Work"`.

## Many small files: pack first

Sending thousands of small files one by one is slow, and hard on shared storage. Pack, send, unpack:

```powershell
# laptop
# c create, z compress, f file name. --exclude leaves out unwanted folders
tar --exclude=.git -czf code.tgz code
scp code.tgz kelvin:~/project/
```

```bash
# cluster
# x extract. && means each step runs only if the last succeeded
cd ~/project && tar xzf code.tgz && rm code.tgz
```

Coming back, pack only what you need, such as summaries rather than every raw output.

## Large transfers

**Kelvin2 only.** For large amounts of data, use a data movement node rather than a login node: `dm1.kelvin.alces.network` or `dm2.kelvin.alces.network`. Tools such as `rsync` can resume an interrupted transfer. MobaXterm and WinSCP offer drag and drop.

## Files that arrive read-only

Copied files can keep restrictive permissions, leading to `Permission denied` when you edit them. `chmod -R u+w ~/project/code` gives you write permission on everything in that folder.
