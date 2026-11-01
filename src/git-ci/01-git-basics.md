---
title: Git basics
slug: git-basics
description: Repositories, commits, viewing history and the everyday cycle of saving versions.
---

## The idea

The blocks labelled "What you should see" in this guide come from running these commands in a test folder. Your commit codes, dates and folder names will differ, `...` marks a shortened folder path, and very long output is trimmed.

Git is a program that records versions of a folder. Each saved version, called a *commit*, stores what changed, who changed it, when and why. Nothing committed is lost, so you never need files such as `final_v2_really_final.docx`.

Install it from [git-scm.com](https://git-scm.com), then tell it who you are, once:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.org"
```

## The everyday cycle

```bash
git init -b main         # start tracking this folder, once, on a branch called main
git status               # what has changed?
git diff                 # show the changes, line by line
git add results.txt      # choose what goes in the next version
git commit -m "Correct the mean"   # save that version, with a reason
git log --oneline        # list the versions
```

::: {.output}
**What you should see**

```text
$ git init -b main
Initialized empty Git repository in .../project/.git/

$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	notes.txt
	results.txt

nothing added to commit but untracked files present (use "git add" to track)

$ git add results.txt
$ git commit -m "First results"
[main (root-commit) 4f2d1b0] First results
 1 file changed, 1 insertion(+)
 create mode 100644 results.txt
```
:::

Now change the number in `results.txt` and look again. In `git status --short`, `M` means modified and `??` means not tracked. In `git diff`, a line starting `-` was removed and a line starting `+` was added.

::: {.output}
**What you should see**

```text
$ git status --short
 M results.txt
?? notes.txt

$ git diff
diff --git a/results.txt b/results.txt
index 62b900e..de5c1f9 100644
--- a/results.txt
+++ b/results.txt
@@ -1 +1 @@
-The mean is 10.
+The mean is 12.

$ git add results.txt
$ git commit -m "Correct the mean"
[main 2f4cdbe] Correct the mean
 1 file changed, 1 insertion(+), 1 deletion(-)

$ git log --oneline
2f4cdbe Correct the mean
4f2d1b0 First results
```
:::

Without `-b main`, this version of Git names the first branch `master` and prints a long hint about it. The rest of this guide uses `main`.

The `add` step exists so that one commit can hold one logical change, even if you changed other files too.

## Try it safely

This script makes a new folder and goes through the whole cycle. Read it, then run it.

!include examples/practice.sh bash

::: {.output}
**What you should see**

```text
 results.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
[main ab8a9f9] Revert "Add the median"
 Date: Sun Nov 1 16:26:34 2026 +0000
 1 file changed, 1 deletion(-)
ab8a9f9 Revert "Add the median"
bd9ec39 Add the median
6f32cdc Correct the mean
8c59d4e First results
The mean is 12.
```
:::

The last line matters: the median has gone from the file, yet all four versions are still in the history.

## What to track

Track what you write by hand: text, code and small inputs. Don't track what can be regenerated, large data, or anything secret. A file called `.gitignore` lists what to skip:

```text
__pycache__/
*.log
build/
data/raw/
.env
```

With that file in place, and `run.log`, `.env` and `build/a.pdf` in the folder, Git no longer mentions them:

::: {.output}
**What you should see**

```text
$ git status --short
?? .gitignore
?? notes.txt
```
:::

## Good commit messages

Write what changed and why, briefly, such as `Correct the living-wage year`. Commit often, in small steps, so that each can be understood or undone by itself.
