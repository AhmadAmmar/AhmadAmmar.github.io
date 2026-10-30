---
title: Troubleshooting and cheat sheet
slug: troubleshooting
description: Common errors with causes and fixes, a one-page command reference, and references.
---

## Errors and what they mean

| Symptom | Likely cause | Fix |
|---|---|---|
| `Permission denied (publickey)` | Wrong key, username or port, or the key is not installed yet | Check `.ssh/config`, and that the cluster has your key |
| Host identification warning | A login node you have not met, or a real problem | Read your cluster's guidance before accepting |
| `scp`: "No such file" with a stray `"` | Trailing backslash in a Windows path | Remove the backslash |
| `scp`: wrong port | `-p` instead of `-P` | `scp` uses capital `-P` |
| `Killed` on the login node | Too much memory on a shared node | Use `srun` or `sbatch` |
| `CondaError: Run 'conda init'` | Shell not set up for conda | `conda init`, then log in again; or call the environment's Python directly |
| `EnvironmentLocationNotFound` | The environment was never created, often as an earlier step failed | Scroll up and fix the first error |
| `SRE module mismatch` or strange Python errors | `PYTHONPATH` points at another Python's libraries | `unset PYTHONPATH PYTHONHOME` |
| `No module named ...` in a job | The job is using a different Python | Call your Python by its full path |
| `rustup` says no default toolchain | Only the installer is loaded | `rustup default stable` |
| Downloads fail in a job | Compute nodes may have restricted internet | Download on the login node first, and build offline |
| `Permission denied` on your own files | Read-only after copying | `chmod -R u+w folder` |
| `$'\r': command not found` | Windows line endings | `sed -i 's/\r$//' script.sh` |
| No log file appears | The `--output` folder does not exist | `mkdir -p logs` before you submit |
| State `TIMEOUT` | Hit the time limit | More `--time`, or a longer partition |
| State `OUT_OF_MEMORY` | Hit the memory limit | More `--mem` |
| Stuck on `PD` for ages | Busy, or you asked for too much | `squeue -u $USER` shows the reason; ask for less |
| Files vanished from scratch | Purged after no access | Keep copies elsewhere |
| Pasted lines ran in an odd order | Multi-line paste in a terminal | Paste one line at a time and check |

The general method: read the **first** error rather than the last, as later errors are often consequences. Then search for its exact text.

## Cheat sheet

```bash
# cluster: daily use
squeue -u $USER                                # what is running
sbatch job.sh                                  # submit
sbatch --array=0-9 job.sh args                 # submit an array
scancel <jobid>                                # cancel
tail -20 "$(ls -t logs/*.out | head -1)"       # newest log
sacct -X -P -S 2026-01-01 -u $USER -o JobID,JobName,Elapsed,State   # history
srun --cpus-per-task=1 --mem=4G --time=00:15:00 --pty bash          # interactive
module avail; module load <name>; module list  # software
quota -s; du -sh ~/project                     # storage
tar czf out.tgz folder; tar xzf out.tgz        # pack and unpack
```

```powershell
# laptop
ssh kelvin                                     # log in
scp file kelvin:~/project/                     # upload
scp kelvin:~/project/file "D:\My Work"         # download
```

## References

Amdahl, G.M. (1967) 'Validity of the single processor approach to achieving large scale computing capabilities', *AFIPS Spring Joint Computer Conference*, pp. 483-485. <https://doi.org/10.1145/1465482.1465560>

Klabnik, S. and Nichols, C. (n.d.) *The Rust Programming Language*. <https://doc.rust-lang.org/book/>

Kurtzer, G.M., Sochat, V. and Bauer, M.W. (2017) 'Singularity: scientific containers for mobility of compute', *PLoS ONE*, 12(5), e0177459. <https://doi.org/10.1371/journal.pone.0177459>

McNabb, R. (n.d.) *Introduction to high performance computing*. <https://iamdonovan.github.io/teaching/hpc-intro/index.html>

Merkel, D. (2014) 'Docker: lightweight Linux containers for consistent development and deployment', *Linux Journal*, 2014(239).

NI-HPC (n.d.) *NI-HPC documentation*. <https://ni-hpc.github.io/nihpc-documentation>

OpenSSH (n.d.) *OpenSSH manual pages*. <https://www.openssh.com/manual.html>

Raicu, I., Foster, I.T. and Zhao, Y. (2008) 'Many-task computing for grids and supercomputers', *Workshop on Many-Task Computing on Grids and Supercomputers*, pp. 1-11. <https://doi.org/10.1109/MTAGS.2008.4777912>

SchedMD (n.d.) *Slurm job array support*. <https://slurm.schedmd.com/job_array.html>

Shotts, W. (2019) *The Linux Command Line*. 5th internet edn. <https://linuxcommand.org/tlcl.php>

Wilson, G., Aruliah, D.A., Brown, C.T., et al. (2014) 'Best practices for scientific computing', *PLoS Biology*, 12(1), e1001745. <https://doi.org/10.1371/journal.pbio.1001745>

Yoo, A.B., Jette, M.A. and Grondona, M. (2003) 'SLURM: Simple Linux Utility for Resource Management', in *Job Scheduling Strategies for Parallel Processing*. Springer, pp. 44-60. <https://doi.org/10.1007/10968987_3>
