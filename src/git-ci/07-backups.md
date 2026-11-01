---
title: Data, backups and releases
slug: backups
description: Dated data folders, checksums, the 3-2-1 rule, testing restores, and making a release.
---

## Data

Git isn't built for large files, so keep data out of it, and record what you used.

- **Never overwrite.** Write each new run to a dated folder, such as `results_2026-10-31/`.
- **Record checksums**, which are fingerprints that change if a file changes: `sha256sum *.csv > MANIFEST.sha256`, and check later with `sha256sum -c MANIFEST.sha256`.
- **Note the source** of each dataset: its address, date and licence.

::: {.output}
**What you should see when nothing has changed**

```text
$ sha256sum -c MANIFEST.sha256
a.csv: OK
b.csv: OK
```
:::

::: {.output}
**What you should see after someone edits b.csv**

```text
$ sha256sum -c MANIFEST.sha256
a.csv: OK
b.csv: FAILED
sha256sum: WARNING: 1 computed checksum did NOT match
```
:::

## Backups

Git is not a backup until a copy exists elsewhere, and a private repository on one laptop can be lost with that laptop. The common rule is **3-2-1**: three copies, on two kinds of storage, with one somewhere else.

Syncing services such as OneDrive aren't enough on their own, because they also sync deletions and corruption. And **a backup you've never restored is only a hope**, so test one:

```bash
git bundle create project.bundle --all     # one file holding a repository's whole history
git clone project.bundle restore-test      # prove that it comes back
```

`git bundle create` prints nothing when it runs inside a script, as here, and shows progress when you type it yourself. Then read the restored history to check it:

::: {.output}
**What you should see**

```text
$ git clone project.bundle restore-test
Cloning into 'restore-test'...

$ git -C restore-test log --oneline -3
4912949 Colleague edit
b889be1 Merge left, keeping 14
a0a50db Main change
```
:::

Databases and uploaded files don't live in Git, so they need their own backups, including an encrypted copy off-site.

## Releases

Whenever something leaves your hands, freeze a copy.

1. Commit everything, so that the source is exact.
2. Run all the checks.
3. Build from clean.
4. Put the outputs in a dated, read-only folder, with checksums.
5. Tag the commit.

Then, for anything a reader sends back, you can find precisely what they had. If it needs correcting, make a new release and log the reason, without editing the old one.

## Secrets

Passwords and keys never go in a repository, because history keeps them even after deletion. Use environment variables or a secrets store. If one gets committed, treat it as exposed: change it first, then clean up.
