#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

int worker_loop(int argc, char *argv[]){
int nelements1 = 1E3;
int nelements2 = 1E6;
int myid, world_size;//, size;
int root = 0;
int endloop[1];
double input[nelements1];
double output[nelements2];
double sendbuff[nelements1];
int recv = 1;
int i = 0;

//printf("We've initialized stuff, moving on to MPI!!\n");

//MPI_Init(&argc, &argv);

//printf("Init just happened, we're alive!\n");

MPI_Comm comm;
MPI_Comm_get_parent(&comm);

//printf("We found our parents, according to Maury!\n\nDoom is here!\n");

MPI_Comm_rank(MPI_COMM_WORLD, &myid);
MPI_Comm_size(MPI_COMM_WORLD, &world_size);

//printf("\nEntering Process %d\n", myid);

//printf("Y2K came and went. Bummer.\n");

for( i = 0; i < nelements2; i++ ){
	output[i] = 1.9;
}

printf("Output full of %f\n",output[0]);

//MPI_Barrier(comm);
//MPI_Scatter(sendbuff, nelements1, MPI_INT, endloop, recv, MPI_INT, root, comm);

endloop[0] = 0;

while ( endloop[0] < 1) {
	MPI_Barrier(comm);
	MPI_Scatter(sendbuff, nelements1, MPI_DOUBLE, input, nelements1, MPI_DOUBLE, root, comm);
	MPI_Barrier(comm);
	MPI_Gather(output, nelements2, MPI_DOUBLE, sendbuff, nelements1, MPI_DOUBLE, root, comm);
	MPI_Barrier(comm);
	MPI_Scatter(sendbuff, nelements1, MPI_INT, endloop, recv, MPI_INT, root, comm);
}

MPI_Finalize();

}
