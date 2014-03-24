// file: worker_c.i
/* SWIG Interface wrapper for interfacing the C worker
     with a python master */
/*
 This file is part of CommLoop.

 CommLoop is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 CommLoop is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
*/

%module worker_c
%{
%}

%include mpi4py/mpi4py.i
%mpi4py_typemap(Comm, MPI_Comm);
int worker_loop(int argc, char **argv[]);
