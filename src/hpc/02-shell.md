---
title: The command line
slug: shell
description: Shells, paths and the Linux commands you actually need, each explained.
---

A **shell** reads what you type and runs it. On Windows you will probably use PowerShell to connect; on the cluster, you will be using `bash`. macOS and Linux terminals work almost the same as `bash`. For a longer course, see Shotts (2019) or [Software Carpentry](https://swcarpentry.github.io/shell-novice/).

## Anatomy of a command

```bash
# cluster
ls -l ~/project
```

`ls` is the command: what to do (list files). `-l` is an option: how to do it (long format). `~/project` is the argument: what to act on. Spaces separate the parts, so a path containing a space needs double quotes, or the shell reads it as two things.

## Paths

| Symbol | Meaning |
|---|---|
| `~` | Your home folder |
| `.` and `..` | This folder, and the one above |
| `/` | Top of the Linux file tree, and the separator between folders |
| `*` | Wildcard: `case_*.json` matches every such file |
| `$HOME`, `$USER` | Variables that hold your home folder and username |

Linux names are case-sensitive, so `Data` and `data` differ. Windows writes `C:\Users\me`, and Linux writes `/users/me`.

## Commands worth knowing

| Command | What it does |
|---|---|
| `pwd` | Print the folder you are in |
| `ls`, `ls -l`, `ls -t` | List files; with details; newest first |
| `cd folder`, `cd ..`, `cd` | Go to a folder; up one; home |
| `mkdir -p a/b` | Make folders, including parents, with no error if they exist |
| `cp a b`, `cp -r a b` | Copy a file; `-r` copies a folder and its contents |
| `mv a b` | Move or rename |
| `rm file` | Delete. **There is no recycle bin.** Look first with `ls` |
| `ln -s target name` | Make a shortcut (a symbolic link) |
| `cat`, `head -5`, `tail -20` | Print a whole file; its first 5 lines; its last 20 |
| `less file` | Read a long file page by page; `q` quits |
| `wc -l` | Count lines |
| `grep "text" file` | Show lines containing text. `-i` ignores case, `-l` lists only file names |
| `sed -i 's/old/new/' file` | Replace text in a file |
| `chmod u+x file` | Let yourself (`u`) execute (`x`) a file. `chmod -R u+w folder` lets you write to everything in a folder |
| `tar czf a.tgz folder` | Pack a folder into one compressed archive (create, gzip, file) |
| `tar xzf a.tgz` | Unpack it (extract) |
| `df -h .`, `du -sh folder` | Free space on this disk; size of a folder |
| `hostname`, `nproc` | Which computer am I on? How many cores may I use? |
| `man ls` | The manual for a command; `q` quits |

To edit on the cluster, `nano file` is the easiest editor if it is installed: the keys are listed at the bottom. NI-HPC's guide uses `vi`, which is powerful but odd at first.

## Joining commands

```bash
# cluster

# | (a pipe) feeds one command's output into the next: count the log files
ls logs/*.out | wc -l

# > saves output to a file, replacing what was there; >> adds to the end
ls -l > listing.txt

# && runs the second command only if the first succeeded
mkdir -p results && cd results

# ; runs the second command whatever happened to the first
cd results; ls

# 2>/dev/null throws away error messages (stream 2) instead of printing them
ls /no/such/folder 2>/dev/null

# $( ) puts one command's output inside another: show the newest log
cat "$(ls -t logs/*.out | head -1)"
```

## Variables and loops

```bash
# cluster

# Set a variable. No spaces around the =
DATA=/mnt/scratch2/users/$USER/data

# Use it with $. Double quotes keep it in one piece even if it contains a space
ls "$DATA"

# A for loop: repeat for each folder; $d holds the current one
for d in results/*/; do
  # basename strips the path; wc -l counts the files listed
  echo "$(basename "$d"): $(ls "$d" | wc -l) files"
done
```

## Windows line endings

Windows ends each line of text with two invisible characters (carriage return, line feed), and Linux with one. A script written on Windows can fail on Linux with baffling errors such as `$'\r': command not found`. Fix it on the cluster:

```bash
# cluster
# In each line, replace a carriage return (\r) at the end of the line ($) with nothing
sed -i 's/\r$//' myscript.sh
```
