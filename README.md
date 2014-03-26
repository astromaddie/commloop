commloop
========

MPI-based communication loop framework for BART

Files:
- `master.py`
 - Holds all the master MPI calls
- `worker.py`
 - Holds worker MPI calls for input converter and output converter
- `src/worker_c.c`
 - Holds worker MPI calls for transit (formerly in transit.py)
- `src/worker_c.i`
 - SWIG interface file for compiling C wrapped in Python code.
- `worker_c_wrapper.py`
 - Python wrapper code to import worker_loop() from the SWIG-compiled worker_c

To compile with SWIG to interface with demc.py:

1. Generate the SWIG wrapper with

  > `swig -python worker_c.i`

2. Compile it with

  > `mpicc -fPIC $(python-config --includes) -c worker_c.c worker_c_wrap.c`

3. Create the shared object file with

  > `mpicc -shared worker_c.o worker_c_wrap.o -o _worker_c.so`

The resulting python file will just need to be imported into another code, upon which the functions may be called normally.
