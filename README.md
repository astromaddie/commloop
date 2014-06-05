##Commloop

MPI-based communication loop framework; designed for communication between Python and C programs.

###Table of Contents
* [Team Members](#team-members)
* [Background](#background)
* [Files](#files)
* [Makefile](#makefile)
* [Commloop Benchmarks](#commloop-benchmarks)

####Team Members
* [Madison Stemm](https://github.com/astromaddie/) (author) ([email](<madison.stemm@gmail.com>))
* [Patricio Cubillos](https://github.com/pcubillos/) ([email](<pcubillos@fulbrightmail.org>))
* [Andrew Foster](https://github.com/AndrewSDFoster) ([email](<andrew.scott.foster@gmail.com>))
* [Joe Harrington](https://github.com/joeharr4) ([email](<jh@physics.ucf.edu>))

####Background

MPI (Message-Passing Interface) is a standard communications protocol used to add parallel processing in programs. In this implementation, it creates separate programs as parallel processes and uses the interface to pass data back and forth between the spawned programs, allowing communication between programs of different languages.

Commloop is designed to be modular and expandable, with `master.py` acting as a central hub, and the workers being easily replaceable. MPI calls are all stored as function wrappers in `mutils.py`, so that MPI could be easily replaced with another parallel processing interface at a later date.

To run the code as-is, run:

  > `mpiexec master.py`

The master code acts as a hub, where it sends data to the first Python worker and awaits output. The outputted data from pyWorker1 is sent back to Master, which then sends it to cWorker. The outputted cWorker data is returned to Master and sent to PyWorker2. Once that data is returned to Master, the loop repeats.

The workers all divide the data they receive in half before sending it back. This scaling factor allows the starting number to rapidly approach zero, so there is a traceable difference between each worker operation, without risk of the values blowing up and causing double overflow issues.

The code currently passes dummy arrays in the following structure:


| Sender          | Data            | Receiver        |
| :-------------: | :-------------: | :-------------: |
| Master          | Array1          | pyWorker1       |
| pyWorker1       | Array2          | Master          |
| Master          | Array2          | cWorker         |
| cWorker         | Array3          | Master          |
| Master          | Array3          | pyWorker2       |
| pyWorker2       | Array4          | Master          |
|                 | Array1 = Array4 |                 |
|                 | _repeat_        |                 |

####Files

- `bin/mutils.py`
 - Holds python wrappers for all used MPI functions in general form
 - (used by both master.py and worker.py)
- `bin/master.py`
 - Holds all the master MPI calls
- `bin/worker.py`
 - Holds worker MPI calls for both Python portions of Commloop
- `bin/worker_c`
 - Holds worker MPI calls for C portion of Commloop
- `src/Makefile`
 - Compiles the C worker
- `src/worker_c.c`
 - Holds worker MPI calls for the C portion of Commloop

####Makefile

To compile the C worker, simply call `make` in src/. The compiled binary will be moved to bin/ automatically with the -f flag.

The makefile generates MPI-executable C code with the following command
  > `mpicc -fPIC -o worker_c worker_c.c`

####Commloop Benchmarks

![Runtime Plot](http://i.imgur.com/YCnfz6B.png)

All of the above benchmarks were done with 10 processes per spawned Python worker, each with 400 iterations. The cumulative times are then averaged. Performance remains constant up to about 10KB, before runtimes begin to logarithmically increase. The belowfinal benchmark was run with the default sourcecode setup (with arrays of sizes 10B, 1KB, 1MB, 10B respectively), with the 1MB array being passed to a C worker, showing runtimes at start, and loop speed breakdowns.

#### Default setup breakdown

| Part of code    | Time (seconds)   |
| :-------------: | :-------------:  |
| Start MPI Comm  | 0.291091918945   |
| Avg Iteration   | 0.194536820277   |
| Total Code      | 82.5224819183    |

#### Runtime Table

| Size of Array    | Mean Time (in seconds)|
| :-------------:  | :-------------:       |
|         1B       |       0.000379        |
|        10B       |       0.000365        |
|       100B       |       0.000437        |
|        1KB       |       0.000466        |
|       10KB       |       0.000729        |
|      100KB       |       0.004208        |
|        1MB       |       0.049231        |
|       10MB       |       0.476789        |
|      100MB       |       8.888832        |

