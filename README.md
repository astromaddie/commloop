commloop
========

MPI-based communication loop framework for BART

Files:
- demc.py
 - Holds all the master MPI calls
- worker.py
 - Holds worker MPI calls for input converter (formerly in incon.py) and output converter (formerly in outcon.py)
- worker.c
 - Holds worker MPI calls for transit (formerly in transit.py)
- incon.py
 - Deprecated worker for input converter
- transit.py
 - Deprecated worker for transit
- outcon.py
 - Deprecated worker for output converter
