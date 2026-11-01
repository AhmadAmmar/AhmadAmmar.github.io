---
title: "Seven exercises to build confidence"
slug: first-jobs
description: Small, safe practice jobs on a cluster, from one plus one to a job array over satellite tiles and a real 150-year weather record.
---

The fastest way to feel at home on a cluster is to run small jobs that cannot go wrong for long. Each exercise here takes a minute or two and adds one new idea. You compare your output with the answer given, so you know whether it worked.

They need only Python's standard library, so there is nothing to install. Every job has a short time limit and asks for little memory, so it should start quickly and costs almost nothing.

## Get the files

[Download the starter kit](https://ahmadammar.github.io/teaching/hpc/examples/hpc-starter-kit.zip) to your computer, or fetch it directly on the cluster:

```bash
# cluster
cd ~
# -O keeps the file name from the address
curl -LO https://ahmadammar.github.io/teaching/hpc/examples/hpc-starter-kit.zip
unzip hpc-starter-kit.zip
cd hpc-starter-kit
# Slurm will not create a log folder for you
mkdir logs
```

Your cluster may need extra settings, such as a partition or account name. If a job is refused, the error message and your cluster's documentation will say which. If `python3` is not found, run `module avail python` and add the right `module load` line to the script.

## Exercise 1: Hello from a compute node

**New idea:** a job runs on a different computer from the one you typed on.

!include examples/starter/01_hello.sh bash

```bash
# cluster
hostname
sbatch 01_hello.sh
# Watch it until it disappears from the queue
squeue -u $USER
# The log is named after the job and its number
cat logs/hello_*.out
```

**Check:** the log ends with `1 + 1 = 2`, and the name in `Hello from` differs from what `hostname` printed on the login node. That difference is the whole idea of a batch system.

## Exercise 2: Run a small program

**New idea:** a job can run your own code, with arguments.

!include examples/starter/02_add.py python

```bash
# cluster
sbatch 02_add.sh
cat logs/add_*.out
```

**Check:** you see your Python version, then `1.0 + 1.0 = 2.0` and `21.0 + 21.0 = 42.0`.

**Try:** break it on purpose. Change the script to run `02_add.py 1` with one number, submit it and read the error in the log. Then run `sacct -X -j <job id>`. You have now seen a failed job, and how to find out why.

## Exercise 3: Ask for more cores

**New idea:** more cores help only if the program uses them, and the gain is rarely perfect.

!include examples/starter/03_primes.py python

```bash
# cluster
sbatch 03_primes.sh
# Change --cpus-per-task to 1 in the script, then submit it again
sbatch 03_primes.sh
grep primes logs/primes_*.out
```

**Check:** every run reports `78498 primes below 1000000`, the known value. Only the time changes. On a test laptop, 1 core took 16.9 s and 4 cores took 7.7 s: 2.2 times faster, not 4. Your times will differ, because splitting and collecting work takes time too.

## Exercise 4: Analyse real data

**New idea:** data travels with the job, and a relative path works because the job starts in the folder you submitted from.

The data is the monthly record from Armagh Observatory in Northern Ireland, published by the Met Office. It is real, so it has gaps: early years lack temperatures, and only complete years count.

```bash
# cluster
head -8 data/armaghdata.txt
sbatch 04_armagh.sh
cat logs/armagh_*.out
```

The first command shows the top of the data file, which is how you learn its layout:

::: {.output}
**What you should see from head**

```text
Armagh
Location: 287800E 345800N (Irish Grid), Lat 54.352 Lon -6.649, 62 metres amsl
Estimated data is marked with a * after the value.
Missing data (more than 2 days missing in month) is marked by  ---.
Sunshine data taken from an automatic Kipp & Zonen sensor marked with a #, otherwise sunshine data taken from a Campbell Stokes recorder.
   yyyy  mm   tmax    tmin      af    rain     sun
              degC    degC    days      mm   hours
   1853   1    ---     ---     ---    57.3     ---
```
:::

**Check, for the file in the kit:**

```text
2085 monthly records, 159 complete years, 1867 to 2025
Warmest: 2023, mean 10.95 C
Coldest: 1892, mean 7.89 C
Wettest: 1872, 1249 mm
```

## Exercise 5: Your first job array

**New idea:** one submission can start many tasks, and each uses its number to choose its own work. This is how most research sweeps run.

!include examples/starter/05_decade.py python

```bash
# cluster
sbatch 05_decades.sh
# Each task appears with its number, such as 12345_3
squeue -u $USER
# After all finish, count the results: expect 15
ls results/decade_*.csv | wc -l
# Join them, with the coolest decade first and the warmest last
cat results/decade_*.csv | sort -t, -k3 -n
```

Each line reads decade, years used, mean temperature. **Check:** the coolest is `1880,10,8.65` and the warmest is `2000,10,10.08`.

::: {.output}
**What you should see**

```text
$ cat results/decade_*.csv | sort -t, -k3 -n
1880,10,8.65
1890,10,8.87
1900,10,8.91
1910,10,8.94
1920,10,9.08
1960,10,9.11
1970,10,9.12
1980,10,9.14
1930,10,9.27
1950,10,9.35
1870,10,9.52
1940,10,9.58
1990,10,9.71
2010,10,9.87
2000,10,10.08
```
:::

These results come from running the same Python scripts on a laptop, with the task number set by hand. On the cluster, the same numbers appear, in the files or logs named above.

The pattern to remember is that the tasks never talk to each other. Each writes its own file, and a simple command joins them at the end.

## Exercise 6: A geospatial calculation

**New idea:** an input can come from the command line, so one script can answer many questions.

The data is about 240 cities from Natural Earth, a public domain map dataset. The script uses the haversine formula for distance over a sphere.

```bash
# cluster
sbatch 06_cities.sh
cat logs/cities_*.out
```

**Check:**

```text
243 cities. Nearest to London:
  The Hague: 309 km
  Brussels: 319 km
  Paris: 343 km
Farthest: Wellington, 18815 km
```

**Try:** pick another city from `data/cities_natural_earth.csv`. Do the distances look right on a map?

## Exercise 7: Satellite tiles in parallel

**New idea:** large images are usually cut into tiles and processed one tile per task.

The Normalised Difference Vegetation Index measures greenness from red and near-infrared light:

```text
NDVI = (NIR - red) / (NIR + red)
```

These tiles are **synthetic**: a script invents them so that the exercise runs anywhere. They are built to run from built-up land (tile 0) to parkland (tile 7).

```bash
# cluster
# Light setup work like this is fine on a login node
python3 07_make_tiles.py
sbatch 07_tiles.sh
# When it has finished
cat results/ndvi_*.csv
```

**Check:** mean NDVI rises steadily from `0.045` in tile 0 to `0.787` in tile 7. Run it again and the numbers stay the same, because the script fixes its random seed.

::: {.output}
**What you should see**

```text
$ python3 07_make_tiles.py
wrote 8 tiles to tiles/

$ cat results/ndvi_*.csv
0,10000,0.045
1,10000,0.181
2,10000,0.304
3,10000,0.416
4,10000,0.522
5,10000,0.616
6,10000,0.705
7,10000,0.787
```
:::

Each line reads tile, pixels, mean NDVI. These results come from running the same Python scripts on a laptop, with the task number set by hand. On the cluster, the same numbers appear, in the files or logs named above.

## From exercises to your own project

You have now used every piece of a real workflow. To move your own work across:

1. Run your program once on your own computer, or in an interactive session on the cluster, on the smallest input you can.
2. Submit that as one job. Compare the answer with the known one.
3. Use `sacct` to see the time and memory it really used, then set your limits a little above that.
4. Run a few tasks of the array, not all of them: `sbatch --array=0-3`.
5. Check that the outputs make sense and can be restarted. Then run the rest.

The next chapter does this at full size, with a parameter sweep.
