
                      /*                      */
                      /* MPI-2                */
                      /*                      */
                      /* Remote Memory Access */
                      /*                      */
                      /* Example of MPI_Get() */
                      /*                      */

/* Version 2 */

                                        /* Michel Vallieres  */

#include <mpi.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

#define  WINDOW_SIZE 1000


int main( int argc, char *argv[] )
{
  int  myid, world_size;
  char info_data[200];
  char window_buffer[WINDOW_SIZE];
  MPI_Aint size;
  int disp_unit;
  MPI_Info info;
  MPI_Win window;
  int target_disp, target_rank;

                                /* join the MPI virtual machine */
  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &myid);
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);

                                /* echo some info data */
  strcpy(info_data, "Code ");
  sprintf( info_data + strlen(info_data), " -- myid %d out of %d -- host: ",
			myid, world_size );
  gethostname(info_data + strlen(info_data), 100);
  sprintf( info_data + strlen(info_data), "\n" );
  fprintf( stderr, "%s",  info_data );

                               /* load info data in shared buffer */
                               /* window_buffer[] will form the   */
                               /* basis for the RMA memory window */
  strcpy( window_buffer, "<<<<<<<<<>>>>>>>>>\n" );
  if ( myid != 0 )
    strcpy( window_buffer, info_data );

                               /* create an MPI memory window   */
                               /* for Remote Memory Access      */
  disp_unit = sizeof( char );
  size = WINDOW_SIZE * disp_unit;
  MPI_Win_create( window_buffer, size, disp_unit, info, 
                     MPI_COMM_WORLD, &window );

                               /* ONLY node 0 calls function */
                               /* for RMA                    */
  if ( myid == 0 )
    {
                               /* scan over codes */
      for ( target_rank=1 ; target_rank<world_size ; target_rank++ )
	{
                               /* open RMA epoch during       */
                               /* which RMA access occurs     */
                               /* called by all nodes because */
                               /* of required synchronization */
                               /* between nodes               */
           MPI_Win_lock( MPI_LOCK_EXCLUSIVE, target_rank, 0, window );

                               /* process 0 "gets" info from */
                               /* target_rank process        */
                               /* only called by process 0   */
           target_disp = 0;
           MPI_Get( window_buffer, WINDOW_SIZE, MPI_CHAR, target_rank,
	          target_disp, WINDOW_SIZE, MPI_CHAR, window );

                               /* close RMA epoch           */
                               /* blocking call             */
                               /* data transfered once back */
           MPI_Win_unlock( target_rank, window );

                               /* echo info from process 0 */
           fprintf( stderr, "Process 0 rreceived from target rank %d \n%s",
	            target_rank, window_buffer  );
	}

    }

                               /* free window buffer */
  MPI_Win_free( &window );
                               /* done */
  MPI_Finalize();
  exit(0);
}
