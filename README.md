commloop
========

MPI-based communication loop framework for BART

Source Files:
- demc.py
 - Holds all the master MPI calls
- worker.py
 - Holds worker MPI calls for input converter and output converter
- worker.c
 - Holds worker MPI calls for transit (formerly in transit.py)
- worker.i
 - SWIG interface file for compiling C wrapped in Python code.

To compile with SWIG to interface with demc.py:

1. Generate the swig wrapper with

  > swig -python worker_c.i

2. Compile it with

  > mpicc -fPIC $(python-config --includes) -c worker_c.c worker_c_wrap.c

3. Create the shared object file with

  > ld -zmuldefs -shared worker_c.o worker_c_wrap.o -o _worker_c.so

The resulting python file will just need to be imported into another code, upon which the functions may be called normally.
