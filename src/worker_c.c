#include <stdio.h>
#include <stdlib.h>
#include <mpi/mpi.h>

/* MPI CommLoop - C worker
 * by Madison Stemm
 * Completed 3/24/2014
 *
 * This file is part of CommLoop.
 *
 * CommLoop is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * CommLoop is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with CommLoop.  If not, see <http://www.gnu.org/licenses/>.
*/

int main(int argc, char *argv[]){
int nelements1 = 1000;
int nelements2 = 1E6;
int myid, world_size;//, size;
int root = 0;
int iterat = -1;
double input[nelements1];
double output[nelements2];
double sendbuff[nelements1];
int recv = 1;
int i = 0;

// Open communications with the Master
MPI_Comm comm;
MPI_Init(NULL, NULL);
MPI_Comm_get_parent(&comm);

// Populate sample array
for( i = 0; i < nelements2; i++ ){
	output[i] = 1.000001;
}

// Number of iterations to loop over
MPI_Barrier(comm);
MPI_Bcast(&iterat, 1, MPI_INT, root, comm);

printf("iterat=%d\n",iterat);

while (iterat >= 0) {

	// Scatter in the array from the first worker's output
	MPI_Barrier(comm);
	MPI_Scatter(sendbuff, nelements1, MPI_DOUBLE, input, nelements1, MPI_DOUBLE, root, comm);

	// Scatter back out the new array
	MPI_Barrier(comm);
	MPI_Gather(output, nelements2, MPI_DOUBLE, sendbuff, nelements1, MPI_DOUBLE, root, comm);

	iterat -= 1;
}

// Close communications
MPI_Barrier(comm);
MPI_Finalize();

}
