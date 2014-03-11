// file: worker.i
%module worker
%{
#include <mpi.h>
#include <stdlib.h>
#include "worker.c"
%}

%include mpi4py.i
%mpi4py_typemap(Comm, MPI_Comm);
void randomarray();
void main(int argc, char *argv[]);

