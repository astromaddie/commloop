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


###Compile the C Worker

To compile with SWIG to interface with demc.py:

1. Generate the SWIG wrapper with

  > `swig -python worker_c.i`

2. Compile it with

  > `mpicc -fPIC $(python-config --includes) -c worker_c.c worker_c_wrap.c`

3. Create the shared object file with

  > `mpicc -shared worker_c.o worker_c_wrap.o -o _worker_c.so`

The resulting python file will just need to be imported into another code, upon which the functions may be called normally.

###Files

- `master.py`
 - Holds all the master MPI calls
- `worker.py`
 - Holds worker MPI calls for both Python portions of CommLoop
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

Performance is fairly constant when arrays are all the same size, but handling arrays of varying sizes produces a performance hit.

#### 4 1B arrays, 100 iterations

| Part of code    | Time (seconds)   |
| :-------------: | :-------------:  |
| Start MPI Comm  | 3.40975117683    |
| First loop iter | 0.83363199234    |
| Last loop iter  | 0.0146758556366  |
| Avg iteration   | 0.0516275525093  |
| Total Code      | 8.58752012253    |

#### 4 100MB arrays, 100 iterations

| Part of code    | Time (seconds)   |
| :-------------: | :-------------:  |
| Start MPI Comm  | 3.52083706856    |
| First loop iter | 0.434430837631   |
| Last loop iter  | 0.0823819637299  |
| Avg iteration   | 0.0841367840767  |
| Total Code      | 11.9525020123    |

#### 4 100MB arrays, 1000 iterations

| Part of code    | Time (seconds)   |
| :-------------: | :-------------:  |
| Start MPI Comm  | 3.45876288414    |
| First loop iter | 1.12678909302    |
| Last loop iter  | 0.0827310085297  |
| Avg iteration   | 0.0984846527576  |
| Total Code      | 102.092504025    |

#### 1.25B, 125B, 125MB, 1.25B arrays, 100 iterations

| Part of code    | Time (seconds)   |
| :-------------: | :-------------:  |
| Start MPI Comm  | 3.52986693382    |
| First loop iter | 1.15215110779    |
| Last loop iter  | 0.39165186882    |
| Avg iteration   | 0.40219643116    |
| Total Code      | 43.7606859207    |
