#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

const int nelements1 = 1E3;
const int nelements2 = 1E6;

//float outarray(){
//	float* array = malloc(sizeof(float) * nelements2);
//	int i = 0;
//	for( i = 0; i < nelements2; i++ ){
//		array[i] = 1.110001;
//	}
//
//	return *array;
//}

int main(argc, argv)
int argc;
char *argv[];
{

int myid, world_size;//, size;
int root = 0;
int* endloop = malloc(sizeof(int));
float* input = (float *)malloc(sizeof(float) * nelements1);
float output[nelements2];
void* sendbuff;
int recv = 1;
int i = 0;

MPI_Init(&argc, &argv);
MPI_Comm comm;
MPI_Comm_get_parent(&comm);

MPI_Comm_rank(MPI_COMM_WORLD, &myid);
MPI_Comm_size(MPI_COMM_WORLD, &world_size);

for( i = 0; i < nelements2; i++ ){
	output[i] = 1.1100001*i;
}

//OMPI_DECLSPEC  int MPI_Scatter(void *sendbuf, int sendcount, MPI_Datatype sendtype,
//                void *recvbuf, int recvcount, MPI_Datatype recvtype, int root, MPI_Comm comm);

MPI_Scatter(sendbuff, recv, MPI_INT, endloop, recv, MPI_INT, root, comm);

while ( endloop[0] < 1) {
	MPI_Barrier(comm);
	MPI_Scatter(sendbuff, recv, MPI_FLOAT, input, nelements1, MPI_FLOAT, root, comm);
	MPI_Barrier(comm);
	MPI_Gather(sendbuff, recv, MPI_FLOAT, output, nelements2, MPI_FLOAT, root, comm);
	MPI_Scatter(sendbuff, recv, MPI_INT, endloop, recv, MPI_INT, root, comm);
}

//free(endloop);
//free(input);

MPI_Finalize();
}
