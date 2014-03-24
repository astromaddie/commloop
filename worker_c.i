// file: worker_c.i
%module worker_c
%{
//#include <mpi.h>
//#include "worker_c.c"
//#include <stdio.h>
//#include <stdlib.h>
%}

%include mpi4py/mpi4py.i
%mpi4py_typemap(Comm, MPI_Comm);
int worker_loop(int argc, char **argv[]);
