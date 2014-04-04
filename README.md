###CommLoop

MPI-based communication loop framework; designed for communication between Python and C programs.

The master code acts as a hub, where it sends data to the first Python worker and awaits output. The outputted data from PyWorker1 is sent back to Master, which then sends it to cWorker. The outputted cWorker data is returned to Master and sent to PyWorker2. Once that data is returned to Master, the loop repeats.

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


###Makefile

To compile the C worker, simply call `make` in src/ and move the shared object file out to the directory with the Python scripts.

The makefile generates Python-executable C code with the following steps

1. Generate the SWIG wrapper with

  > `swig -python worker_c.i`

2. Compile it with

  > `mpicc -fPIC $(python-config --includes) -c worker_c.c worker_c_wrap.c`

3. Create the shared object file with

  > `mpicc -shared worker_c.o worker_c_wrap.o -o _worker_c.so`

The resulting python file just needs to be imported into another code, upon which the functions may be called normally.

###Files

- `master.py`
 - Holds all the master MPI calls
- `worker.py`
 - Holds worker MPI calls for both Python portions of CommLoop
- `src/Makefile`
 - Compiles the Python-executable C worker
- `src/worker_c.c`
 - Holds worker MPI calls for the C portion of CommLoop
- `src/worker_c.i`
 - SWIG interface file for compiling C wrapped in Python code.
- `_worker_c.so`
 - Compiled worker_c shared object file
- `worker_c.py`
 - SWIG wrapper to execute `_worker_c.so`
- `worker_c_wrapper.py`
 - Python code to run worker_loop() from the SWIG-compiled worker_c


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
