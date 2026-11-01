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

## Backups

Git is not a backup until a copy exists elsewhere, and a private repository on one laptop can be lost with that laptop. The common rule is **3-2-1**: three copies, on two kinds of storage, with one somewhere else.

Syncing services such as OneDrive aren't enough on their own, because they also sync deletions and corruption. And **a backup you've never restored is only a hope**, so test one:

```bash
git bundle create project.bundle --all     # one file holding a repository's whole history
git clone project.bundle restore-test      # prove that it comes back
```

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
