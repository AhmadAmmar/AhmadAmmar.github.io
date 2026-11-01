---
title: Git basics
slug: git-basics
description: Repositories, commits, viewing history and the everyday cycle of saving versions.
---

## The idea

Git is a program that records versions of a folder. Each saved version, called a *commit*, stores what changed, who changed it, when and why. Nothing committed is lost, so you never need files such as `final_v2_really_final.docx`.

Install it from [git-scm.com](https://git-scm.com), then tell it who you are, once:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.org"
```

## The everyday cycle

```bash
git init                 # start tracking this folder, once
git status               # what has changed?
git diff                 # show the changes, line by line
git add results.txt      # choose what goes in the next version
git commit -m "Correct the mean"   # save that version, with a reason
git log --oneline        # list the versions
```

The `add` step exists so that one commit can hold one logical change, even if you changed other files too.

## Try it safely

This script makes a new folder and goes through the whole cycle. Read it, then run it.

!include examples/practice.sh bash

## What to track

Track what you write by hand: text, code and small inputs. Don't track what can be regenerated, large data, or anything secret. A file called `.gitignore` lists what to skip:

```text
__pycache__/
*.log
build/
data/raw/
.env
```

## Good commit messages

Write what changed and why, briefly, such as `Correct the living-wage year`. Commit often, in small steps, so that each can be understood or undone by itself.
