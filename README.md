##Commloop

MPI-based communication loop framework; designed for communication between Python and C programs.

###Table of Contents
* [Team Members](#team-members)
* [Background](#background)
* [Filelist](#files)
* [Makefile](#makefile)
* [Commloop Benchmarks](#commloop-benchmarks)

####Team Members
* [Madison Stemm](https://github.com/astromaddie/) (author) (<madison.stemm@gmail.com>)
* [Patricio Cubillos](https://github.com/pcubillos/) (<pcubillos@fulbrightmail.org>)
* [Andrew Foster](https://github.com/AndrewSDFoster) (<andrew.scott.foster@gmail.com>)
* [Joe Harrington](https://github.com/joeharr4) (<jh@physics.ucf.edu>)

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

![Runtime Plot](http://i.imgur.com/U1kTDmv.png)

All of the above benchmarks were done with 10 processes per spawned Python worker, each with 1000 iterations. The min, max, median, and mean times were recorded for each transfer size. Performance remains constant up to about 10KB, before runtimes begin to logarithmically increase. The final benchmark was run with the default sourcecode setup (with arrays of sizes 10B, 1KB, 1MB, 10B respectively), with the 1MB array being passed to a C worker, showing runtimes at start, and loop speed breakdowns.

##### Default setup breakdown

| Part of code    | Time (seconds)   |
| :-------------: | :-------------:  |
| Start MPI Comm  | 0.291091918945   |
| Avg Iteration   | 0.194536820277   |
| Total Code      | 82.5224819183    |

##### Runtime Table

| Size of Array    | Median Time (in seconds)|  Minimum Time (in seconds)|
| :-------------:  |   :-------------:       |      :-------------:      |
|         [1B](#1-byte)       |         8.10623e-06     |         3.81469e-06       |
|        [10B](#10-bytes)       |         8.10623e-06     |         6.91413e-06       |
|       [100B](#100-bytes)       |         8.10623e-06     |         2.86102e-06       |
|        [1KB](#1-kilobyte)       |         6.19888e-06     |         4.76837e-06       |
|       [10KB](#10-kilobytes)       |         3.49283e-05     |         1.69277e-05       |
|      [100KB](#100-kilobytes)       |         0.00130105      |         0.00126290        |
|        [1MB](#1-megabyte)       |         0.0130050       |         0.0125229         |
|       [10MB](#10-megabytes)       |         0.155957        |         0.150859          |
|      [100MB](#100-megabytes)       |         1.60676         |         0.852834          |

##### Per-Array Plots of Benchmark Transfers

The transfer times for all 1000 iterations for each benchmark were recorded to show the variations in transfer times. Spikes occur periodically, which may indicate an MPI buffer being flushed. 

###### 1 Byte
![1B](http://i.imgur.com/t5Rcnqh.png)
###### 10 Bytes
![10B](http://i.imgur.com/AjqqaUt.png)
###### 100 Bytes
![100B](http://i.imgur.com/utMjdSv.png)
###### 1 Kilobyte
![1KB](http://i.imgur.com/TcNpjzT.png)
###### 10 Kilobytes
![10KB](http://i.imgur.com/8TG0JpT.png)
###### 100 Kilobytes
![100KB](http://i.imgur.com/EXB1DfO.png)
###### 1 Megabyte
![1MB](http://i.imgur.com/K30nAmw.png)
###### 10 Megabytes
![10MB](http://i.imgur.com/v8jqBiZ.png)
###### 100 Megabytes
![100MB](http://i.imgur.com/y8MCmtV.png)
