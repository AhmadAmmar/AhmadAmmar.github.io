---
title: Branches, tags and going back
slug: history
description: Trying ideas on branches, naming versions with tags, and undoing things safely.
---

## Branches

A branch is a separate line of work, which lets you try something without touching your working version.

```bash
git switch -c idea       # make a branch and move to it
# ... work and commit ...
git switch main          # go back
git merge idea           # bring the work in
```

If two branches changed the same lines, Git asks you to choose. Open the file, keep what you want, delete the markers, then `git add` and `git commit`.

## Tags

A tag gives a version a permanent name, such as what you sent to a journal.

```bash
git tag -a submitted-2026-11-01 -m "Sent to the journal"
git push origin submitted-2026-11-01
```

## Going back

| You want to | Use |
|---|---|
| See an old version | `git switch --detach <tag or commit>`, then `git switch main` to return |
| Undo a commit, keeping the history | `git revert <commit>` |
| Get one old file back | `git restore --source <commit> file.txt` |
| Discard edits you haven't committed | `git restore file.txt`, which can't be undone |
| Find which commit broke something | `git bisect` |

Prefer `revert` over rewriting history. Commands such as `git reset --hard` and `git push --force` can destroy work, so check what they do before using them.

## A sensible rule for versions

Keep one working copy of each file under Git, and stop putting versions in file names. For data, which is too large for Git, use dated read-only folders with recorded checksums, as described in the [backups chapter](../backups/).
