"""Count primes below a limit, on as many cores as Slurm gave this job. Standard library only."""
import multiprocessing as mp
import os
import sys
import time


def is_prime(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, int(n ** 0.5) + 1))


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    cores = int(os.environ.get("SLURM_CPUS_PER_TASK", 1))
    start = time.time()
    with mp.Pool(cores) as pool:
        count = sum(pool.map(is_prime, range(limit), chunksize=10_000))
    print(f"{count} primes below {limit}, on {cores} core(s), in {time.time() - start:.1f} s")
