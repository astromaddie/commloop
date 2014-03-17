

           /*  Skeleton manager code that launches     */
           /*  a slave code   launched_code            */
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
  int myid, world_size, number_to_spawn;
  char launched_program[100];
  MPI_Comm everyone;
  char buf[1000];

                                /* join the MPI virtual machine */
  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &myid);
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);
  strcpy(buf, "Manager code started - host ");
  gethostname(buf + strlen(buf), 100);
  fprintf( stderr, "%s -- myid & world_size %d %d\n", 
               buf, myid, world_size );

                                /* there can only be a single manager! */
  if ( world_size != 1 )
    {
      MPI_Finalize();
      fprintf( stderr,"Too many managers!!\n");
      exit(1);
    }
                               /* # of worker processes */
  number_to_spawn = 4;

                               /* launch codes */
  sprintf( launched_program, "./launched_code" );

  /* argv handling */
  argv = (char **)malloc( 3 * sizeof(char *) );
  argv[0] =  "First" ;
  argv[1] =  "Second" ;
  argv[2] = NULL ;

                               /*spawn processes                 */
                               /* use MPI_ARGV_NULL if no argv[] */
  MPI_Comm_spawn( launched_program, argv , number_to_spawn,
                  MPI_INFO_NULL, 0, MPI_COMM_SELF, &everyone,
                  MPI_ERRCODES_IGNORE );
  
  MPI_Finalize();
  exit(0);
}