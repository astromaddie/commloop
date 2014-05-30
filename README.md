###Commloop

MPI-based communication loop framework; designed for communication between Python and C programs.

To run the code as-is, execute the following line:

  > `mpiexec -np 1 master.py`

The master code acts as a hub, where it sends data to the first Python worker and awaits output. The outputted data from PyWorker1 is sent back to Master, which then sends it to cWorker. The outputted cWorker data is returned to Master and sent to PyWorker2. Once that data is returned to Master, the loop repeats.

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

###Files

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

###Makefile

To compile the C worker, simply call `make` in src/. The compiled binary will be moved to bin/ automatically with the -f flag.

The makefile generates MPI-executable C code with the following command
  > `mpicc -fPIC -o worker_c worker_c.c`

###CommLoop Benchmarks

All of the following benchmarks are done with 10 processes per spawned Python worker with 400 iterations. The cumulative times are then averaged. Performance remains constant up to about 1KB, and begins decreasing linearly as the array size is increased. 10MB arrays were untested, but assumed to be on the order of 45s. Interestingly, consecutively handling arrays of varying sizes results in a larger performance loss. The final benchmark (10B, 1KB, 1MB, 10B) was run with the default sourcecode setup, with the 1MB array being passed to a C worker, showing runtimes at start, and loop speed breakdowns. The loop speeds indicate less performance loss with a C worker, than a Python worker.

#### Runtimes

| Size of Array    | Mean Time (in seconds)    |
| :-------------:  | :-------------:           |
|         1B       |       0.00505563914776    |
|        10B       |       0.0050656175613     |
|       100B       |       0.0056332963705     |
|        1KB       |       0.00832622706890    |
|       10KB       |       0.0449095028639     |
|      100KB       |       0.492187131643      |
|        1MB       |       4.45193855694       |
| 1B, 10B, 100B, 1KB, 10KB      | 0.0697515845299    |
| 10B, 1KB, 1MB, 10B      | 0.40219643116      |

#### Default setup breakdown

| Part of code    | Time (seconds)   |
| :-------------: | :-------------:  |
| Start MPI Comm  | 3.52986693382    |
| First loop iter | 1.15215110779    |
| Last loop iter  | 0.39165186882    |
| Avg iteration   | 0.40219643116    |
| Total Code      | 43.7606859207    |
