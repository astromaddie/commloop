#include <stdio.h>
#include <mpi.h>

MPI_Comm comm;
MPI_Comm_get_parent(&comm);

int myid, world_size, size;
int root = 0;
int* endloop = malloc(sizeof(int));
int nelements1 = 1E3;
int nelements2 = 1E6;
float* input = malloc(sizeof(float) * nelements1);
float output[nelements2];

int randomarray(){
	float array[nelements2];
	srand(time(NULL));
	for( i = 0; i < nelements2; i++ ){
		array[i] = rand() % 0 + 1E6
	}

	return array;

MPI_Comm_rank(MPI_COMM_WORLD, &myid);
MPI_Comm_size(MPI_COMM_WORLD, &world_size);
MPI_Comm_remote_size(parent, &size);

output = randomarray()

MPI_Scatter(endloop, 1, MPI_INT, root, comm);

while ( endloop[0] < 1) {
	MPI_Barrier(comm);
	MPI_Scatter(input, nelements1, MPI_FLOAT, root, comm);
	MPI_Barrier(comm);
	MPI_Gather(output, nelements2, MPI_FLOAT, root, comm);
	MPI_Scatter(endloop, 1, MPI_INT, root, comm);
}

MPI_Finalize();
