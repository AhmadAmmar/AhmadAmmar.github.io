---
title: Checklists and cheat sheet
slug: checklist
description: A checklist for starting a project and for sending anything out, with a list of everyday commands.
---

## Starting a project

- [ ] `git init`, a README and a `.gitignore`
- [ ] A folder layout that separates raw data, code and outputs
- [ ] A recorded environment
- [ ] A first test
- [ ] A remote copy and a backup
- [ ] A licence, if it's going public

## Before sending anything out

- [ ] All changes committed
- [ ] Tests and checks pass
- [ ] Built from clean, on the current source
- [ ] Every stated number traced to a result
- [ ] Links and references tested
- [ ] Read by a person against its sources
- [ ] Frozen as a dated release, with a tag and checksums
- [ ] Backed up

## Cheat sheet

```bash
git status                 # what changed?
git diff                   # how?
git add -A                 # choose everything
git commit -m "Why"        # save a version
git log --oneline          # list versions
git switch -c idea         # new branch
git merge idea             # bring it in
git tag -a v1 -m "Note"    # name a version
git push                   # send online
git pull                   # fetch from online
git revert <commit>        # undo, keeping history
python -m pytest           # run tests
sha256sum -c MANIFEST.sha256   # check files are unchanged
```
