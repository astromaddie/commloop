CommLoop
========

MPI-based communication loop framework; designed for communication between Python and C programs.

The master code acts as a hub, where it sends data to the first Python worker and awaits output. The outputted data from PyWorker1 is sent back to Master, which then sends it to cWorker. The outputted cWorker data is returned to Master and sent to PyWorker2. Once that data is returned to Master, the loop repeats.

The code currently passes dummy arrays witht the following structure:
- Master    --array1--> PyWorker1
- PyWorker1 --array2--> Master
- Master    --array2--> cWorker
- cWorker   --array3--> Master
- Master    --array3--> PyWorker2
- PyWorker2 --array4--> Master

  _--repeat--_

Files:
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

To compile with SWIG to interface with demc.py:

1. Generate the SWIG wrapper with

  > `swig -python worker_c.i`

2. Compile it with

  > `mpicc -fPIC $(python-config --includes) -c worker_c.c worker_c_wrap.c`

3. Create the shared object file with

  > `mpicc -shared worker_c.o worker_c_wrap.o -o _worker_c.so`

The resulting python file will just need to be imported into another code, upon which the functions may be called normally.
