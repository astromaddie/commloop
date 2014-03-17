// file: hellosquare.i
%module hellosquare
%{
#include <mpi.h>
#include "hellosquare.c"
%}

%include mpi4py/mpi4py.i
%mpi4py_typemap(Comm, MPI_Comm);
void sayhello(MPI_Comm comm);
