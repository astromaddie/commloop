

             /*                                                         */
             /*         MPI_Spawn()                                     */
             /*                                                         */
             /*         Spawned analysis code based on                  */
             /*         sequential code  search_text.c                  */
             /*                                                         */
             /*         spawned by  manager.c                           */
             /*                                                         */
             /*         Searches litterary works                        */
             /*                                                         */
             /*         Sample built-in commands:                       */ 
             /*                  frequency "word"                       */
             /*                  distribution "word"                    */
             /*                  correlation  "word_1" " word_2"        */
             /*                  help                                   */
             /*                  quit                                   */


                                                         /* Michel Vallieres */
 
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <mpi.h>



#define MAX_WORDS 100000

char word[MAX_WORDS][100];



/* utility to rewrite string in small case letters only */
void lower_case_letters ( char string[] )
{
  int ic, lw;

  lw = strlen( string );
    for ( ic=0 ; ic<lw ; ic++ )
       string[ic] = tolower( string[ic] );
}



/* special characters clean-up routine - removes   */
/* single ocurence of in_string from string        */
void cleanup (   char string[], char in_string )
{
  int ic, nc, lw;
  char *found;

  if ( ( found = strchr( string, in_string ) ) != NULL )
         {
           nc = found-string;
           lw = strlen( string );
           for ( ic=nc ; ic<lw ; ic++ )
              string[ic] = string[ic+1];
         }
}


/* correlations between the words */
void correlation ( char word_1[], char word_2[], int corr[], int n_word )
{
  int iw, wscan, wscan_min, wscan_max;
                                                         /* zeroth */
                                                         /* correlation */
  for ( wscan=0; wscan<5 ; wscan++ )
    corr[wscan] = 0;
                                                         /* scan over text */
  for ( iw=0 ; iw<n_word ; iw++ )
    {                                                    /* find word #1 */
       if ( strcmp( word[iw] , word_1 ) == 0 )
	 {
	    wscan_max = iw + 5;
            if ( wscan_max > n_word )
	      wscan_max = n_word;
            wscan_min = iw+1;
            if ( wscan_min > n_word )
	      wscan_min = n_word;                        /* find word #2 */
	                                                 /* nearby */
            if ( wscan_max >= wscan_min )
	      {
                for ( wscan=wscan_min ; wscan<wscan_max ; wscan++ )
	          {
                    if ( strcmp( word[wscan] , word_2 ) == 0 )
		      corr[wscan-iw-1] = corr[wscan-iw-1] + 1;
		  }
	      }
	 }
    }

}



/*  frequency  search  */
void search_word( char *a_word, int *occurences, int n_word )
{
  int iw, times;

  times = 0;
  for ( iw=0 ; iw<n_word ; iw++ )
    {
      if ( strcmp( word[iw] , a_word ) == 0 )
	times++;
    }
  *occurences = times;
}


/*  distribution search  */
void distribution( char *a_word, int dist[], int n_word )
{
  int iw, iw_1_3, iw_2_3, times;

                                                         /* first third */
  iw_1_3 = n_word/3;
  iw_2_3 = 2*n_word/3;
  times = 0;
  for ( iw=0 ; iw<iw_1_3 ; iw++ )
    {
      if ( strcmp( word[iw] , a_word ) == 0 )
	times++;
    }
  dist[0] = times;
                                                         /* second third */
  times = 0;
  for ( iw=iw_1_3 ; iw<iw_2_3 ; iw++ )
    {
      if ( strcmp( word[iw] , a_word ) == 0 )
	times++;
    }
  dist[1] = times;
                                                         /* last third */
  times = 0;
  for ( iw=iw_2_3 ; iw<n_word ; iw++ )
    {
      if ( strcmp( word[iw] , a_word ) == 0 )
	times++;
    }
  dist[2] = times;
}



/* read in the data */
void get_the_data ( char *fname, int *n_word )
{
   FILE *fp;
   int  i_word;
   char *found, comma, dot, semi_colon, colon, question, exclamation;
   int  ic, nc, lw;

   if ( ( fp = fopen( fname, "r" ) )  == NULL )
     {
       printf( " error in opening file \n" );
       exit(1);
     }

   comma = ',';
   dot = '.';
   semi_colon = ';';
   colon = ':';
   question = '?';
   exclamation = '!';
   i_word = 0;

   while ( fscanf( fp, "%s", word[i_word] ) != EOF )
     {
                                                         /* clean out | */
       if ( strcmp( word[i_word], "|" ) == 0 ) 
                           i_word--;
                                                         /* removes , */
       cleanup ( word[i_word],  comma );
                                                         /* removes . */
       cleanup ( word[i_word],  dot );
                                                         /* removes ; */
       cleanup ( word[i_word],  semi_colon );
                                                         /* removes : */
       cleanup ( word[i_word],  colon );
                                                         /* removes ? */
       cleanup ( word[i_word],  question );
                                                         /* removes ! */
       cleanup ( word[i_word],  exclamation );
                                                         /* small case letters */
       lower_case_letters ( word[i_word] );
                                                         /* next word */
       i_word++;

       if ( i_word == MAX_WORDS )
	 {
	   printf( "\n Dimension too small - increase MAX_WORDS\n\n" );
           exit(1);
	 }
     }
                                                         /* close file */
   fclose(fp);

   *n_word = i_word-1;

}


/* input command  */
void command_input ( char line_command[], char command[], char word_1[], 
                           char word_2[], int myid )
{
  int n;

      sscanf( line_command, "%s", command );
      lower_case_letters ( command );
      n = strlen( command );

      if ( strcmp ( command, "frequency" ) == 0 )
        {
          sscanf( &line_command[n+1], "%s", word_1 );
          lower_case_letters ( word_1 );
        }
      else if ( strcmp ( command, "distribution" ) == 0 )
        {
          sscanf( &line_command[n+1], "%s", word_1 );
          lower_case_letters ( word_1 );
        }
      else if ( strcmp ( command, "correlation" ) == 0 )
        {
          sscanf( &line_command[n+1], "%s %s", word_1, word_2 );
          lower_case_letters ( word_1 );
          lower_case_letters ( word_2 );
	}
      else if ( strcmp ( command, "quit" ) == 0 )
	{
          MPI_Finalize();
	  exit(0); 
	}
      else if ( strcmp ( command, "help" ) == 0 && myid == 0 )
	{
          printf( "\n" );
          printf( " Syntax:   help \n" );
          printf( "           frequency  word \n" );
          printf( "           distribution word \n" );
          printf( "           corrolation  word_1  word_2 \n" );
          printf( "           quit \n\n" );
	}
      else 
        {
          if ( myid == 0 )
              printf( " Error - command not implemented \n");
        }

}



int main( int argc, char *argv[] )
{

   int  empty, shift, n_word;
   char line_command[100], command[100], word_1[100], word_2[100];
   int  occurences;
   int  wscan, corr[5];
   int  dist[3];
   char *directory;
   char fname[100], path[100];
   char results[2000];
   MPI_Status status;
   MPI_Comm parent;
   char buf[1000];
   int  myid, world_size, size;


                                                       /* join the MPI virtual machine */
   MPI_Init(&argc, &argv);
   MPI_Comm_rank(MPI_COMM_WORLD, &myid);
   MPI_Comm_size(MPI_COMM_WORLD, &world_size);
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
                                                         /* file to read */
   MPI_Recv( fname, 100, MPI_CHAR, 0, 325, 
                parent, &status );

                                                         /* get the text data */
   directory = getenv( "PWD" );
   strcpy( path, "" );
   strcat( path, directory );
   strcat( path, "/plays/" );
   strcat( path, fname );
                                                         /* read the file in memory */
   get_the_data ( path,  &n_word );
   printf( "Daemon %d --> # words: %d -- file: %s\n", 
                     myid, n_word, path );
                                                         /* scan over commands */
   for ( ; ; )
     {
                                                         /* receive a command */
       MPI_Recv( line_command, 100, MPI_CHAR, 0, 445, 
                                      parent, &status );

                                                         /* read in command */
       command_input( line_command, command,  word_1, word_2, myid );

                                                         /* output string */
       strcpy( results, fname );
       sprintf( results+strlen(results), "\n" );
       shift = strlen(results);
       empty = 0;
                                                         /* frequency */
       if ( strcmp ( command, "frequency" ) == 0 )
	 {
            search_word( word_1, &occurences, n_word );
            sprintf( results+shift, " %s  -- appears %d times \n", 
                             word_1, occurences );
	    empty++;
	 }
                                                         /* correlations */
       if( strcmp ( command, "correlation" ) == 0 )
	 {
	   correlation( word_1, word_2, corr, n_word );
	   sprintf( results+shift, " distance   number \n");
           for ( wscan=0 ; wscan<5 ; wscan++ )
             sprintf( results+strlen(results),
                 "      %d         %d  \n", wscan, corr[wscan] );
           sprintf( results+strlen(results), " \n" );
	   empty++;
	 }
                                                         /* distribution */
                                                         /* of word */
       if( strcmp ( command, "distribution" ) == 0 )
	 {
           distribution( word_1, dist, n_word );
           sprintf( results+shift, " distribution: %d %d %d\n", 
                            dist[0], dist[1], dist[2] );
	   empty++; 
	 }
       
       if ( empty == 0 )
	 strcpy( &results[0], "  " );

                                                         /* send results to manager */
       MPI_Ssend( results, 2000, MPI_CHAR, 0, 555, parent );
     }

}





