#!/bin/bash
# A safe practice run of everyday Git, in a new folder. Run: bash practice.sh
set -e
mkdir git-practice && cd git-practice
git init -q -b main
git config user.name "A Student"
git config user.email "student@example.org"

# Save a first version
echo "The mean is 10." > results.txt
git add results.txt
git commit -q -m "First results"

# Change it and see exactly what changed
echo "The mean is 12." > results.txt
git diff --stat
git add results.txt
git commit -q -m "Correct the mean"

# Name this version
git tag -a sent-to-supervisor -m "The version I sent"

# Try an idea safely on a branch, then bring it back
git switch -q -c idea
echo "The median is 11." >> results.txt
git add results.txt
git commit -q -m "Add the median"
git switch -q main
git merge -q idea

# Undo the last change, keeping the history
git revert --no-edit HEAD
git log --oneline
cat results.txt
