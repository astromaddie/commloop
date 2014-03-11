
             /*   MPI_Spawn()                   */
             /*                                 */
             /*   spawns  search_text_daemon.c  */

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
  int daemon;
  char buf[1000];
  FILE *fp;
  int no_files, length;
  char line_command[100];
  char file_name[20][100], name[20][100]; 
  MPI_Status status;
  char results[2000];

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

                               /* read list of plays */
  fp = fopen( "list_of_plays", "r" );
  no_files = 0;
  while ( fscanf( fp, "%s", file_name[no_files] ) != EOF )
    {
      printf( "File #: %d -- file %s\n", 
	      no_files, file_name[no_files] );
      no_files++;
    }
  fclose( fp );
  printf( "No of files (and spawned processes: %d\n", no_files );

                               /* # of worker processes */
  number_to_spawn = no_files;

                               /* launch codes */
  sprintf( launched_program, "./search_text_daemon" );

                               /*spawn processes                 */
                               /* use MPI_ARGV_NULL if no argv[] */
  MPI_Comm_spawn( launched_program, MPI_ARGV_NULL , number_to_spawn,
                  MPI_INFO_NULL, 0, MPI_COMM_SELF, &everyone,
                  MPI_ERRCODES_IGNORE );
 
                               /* distribute files among processes */
  for ( daemon=0; daemon<no_files ; daemon++ )
    {
      MPI_Ssend( file_name[daemon], 100, MPI_CHAR, daemon, 325, 
                   everyone );
    }

  for ( ; ; )
    {
                              /* delay */
      sleep(1);
                              /* get a command */
      printf( " Enter a command (quit): " );
      fgets( line_command, 200, stdin );

                              /* send command to spwaned processes */
      for ( daemon=0; daemon<no_files ; daemon++ )
	{
	  MPI_Ssend( line_command, 100, MPI_CHAR, daemon, 445, everyone );
	}

                              /* the end ? */
      if ( strstr( line_command, "quit") != NULL )
	{
          MPI_Finalize();
          exit(0);

	}
                              /* results back */
      for ( daemon=0; daemon<no_files ; daemon++ )
	{
          MPI_Recv( results, 2000, MPI_CHAR, daemon, 555, everyone, &status );
          printf( "%s\n", results ); 
	}

    }

  
}
