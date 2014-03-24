commloop
========

MPI-based communication loop framework for BART

To compile:

1. Generate the swig wrapper with

  > `swig -python worker_c.i`

2. Compile it with

  > `mpicc -fPIC $(python-config --includes) -c worker_c.c worker_c_wrap.c`

3. Create the shared object file with

  > `mpicc -shared worker_c.o worker_c_wrap.o -o _worker_c.so`

4. Simply run

  > `python master.py`

Source Files:
- master.py
 - Holds all the master MPI calls (formerly demc.py)
- worker.py
 - Holds worker MPI calls for input converter and output converter
- worker_c.c
 - Holds worker MPI calls for transit (formerly in transit.py)
- worker.i
 - SWIG interface file for compiling C wrapped in Python code.
- worker_c_wrapper.py
 - Python wrapper to call the SWIG-wrapped worker_c function
