// file: worker_c.i
%module worker_c
%{
#include <mpi.h>
#include <stdlib.h>
#include "worker_c.c"
%}

%include mpi4py/mpi4py.i
%mpi4py_typemap(Comm, MPI_Comm);
void outarray();
void main(int argc, char *argv[]);

