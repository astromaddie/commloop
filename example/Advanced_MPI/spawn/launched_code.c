

           /*  Skeleton slave code to be launched by   */
           /*  the master code  manager.c              */
           /*                                          */
           /*  Example patterned on the documentation  */
           /*  in MPI2 web site                        */
           /*  http://www.mpi-forum.org/               */

                                               /* Michel Vallieres  */
#include <mpi.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>


int main( int argc, char *argv[] )
{
  int myid, world_size, universe_size, size;
  MPI_Comm parent;
  char buf[1000];


                                /* join the MPI virtual machine */
  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &myid);
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);
  strcpy(buf, "Spawned code - host ");
  gethostname(buf + strlen(buf), 100);
  fprintf( stderr, "%s -- myid & world_size %d %d -- argc & argv %d %s %s\n", 
	   buf, myid, world_size, argc, argv[1], argv[2] );

                               /* find parent process */
  MPI_Comm_get_parent( &parent);
  if ( parent == MPI_COMM_NULL )
    {
      MPI_Finalize();
      fprintf( stderr,"Launched code has no parent\n");
      exit(1);
    }
                                /* size of parent */
  MPI_Comm_remote_size( parent, &size );
  if ( size != 1 ) 
    {
      MPI_Finalize();
      fprintf( stderr,"Error in parent\n");
      exit(1);
    }

                                /* give sign of life */
  fprintf( stderr, "Process %d has %d parent\n", myid, size );
  MPI_Finalize();
  exit(0);
}