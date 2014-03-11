

             /*         Simple client server skeleton                   */
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
void command_input ( char command[], char word_1[], char word_2[] )
{
      printf( " Enter a command (quit): " );
      scanf( "%s", command );
      lower_case_letters ( command );


      if ( strcmp ( command, "frequency" ) == 0 )
        {
          printf( " Word to search for    : " );
          scanf( "%s", word_1 );
          lower_case_letters ( word_1 );
        }
      else if ( strcmp ( command, "distribution" ) == 0 )
        {
          printf( " Word to search for    : " );
          scanf( "%s", word_1 );
          lower_case_letters ( word_1 );
        }
      else if ( strcmp ( command, "correlation" ) == 0 )
        {
          printf( " Words to correlate    : " );
          scanf( "%s", word_1 );
          scanf( "%s", word_2 );
          lower_case_letters ( word_1 );
          lower_case_letters ( word_2 );
	}
      else if ( strcmp ( command, "quit" ) == 0 )
	 exit(0); 
      else if ( strcmp ( command, "help" ) == 0 )
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
          printf( " Error - command not implemented \n");
        }

}



int main( int argc, char *argv[] )
{

   int n_word;
   char command[100], word_1[100], word_2[100];
   int occurences;
   int wscan, corr[5];
   int dist[3];
   char *directory;
   char fname[100];

                                                         /* get the text data */
   directory = getenv( "PWD" );
   strcpy( fname, "" );
   strcat( fname, directory );
   strcat( fname, "/plays/" );
   strcat( fname, argv[1] );
   printf( "\n\n File to read: %s \n", fname );

                                                         /* read the file in memory */
   get_the_data ( fname,  &n_word );
   printf( " \n Number of words: %d \n\n", n_word );

                                                         /* scan over commands */
   for ( ; ; )
     {
                                                         /* read in command */
       command_input(  command, word_1, word_2 );
                                                         /* frequency */
       if ( strcmp ( command, "frequency" ) == 0 )
	 {
            search_word( word_1, &occurences, n_word );
            printf( "\n %s  -- appears %d times \n\n", word_1, occurences );
	 }
                                                         /* correlations */
       if( strcmp ( command, "correlation" ) == 0 )
	 {
	   correlation( word_1, word_2, corr, n_word );
	   printf( "\n distance   number \n");
           for ( wscan=0 ; wscan<5 ; wscan++ )
             printf( "      %d         %d  \n", wscan, corr[wscan] );
           printf( " \n" );
	 }
                                                         /* distribution */
                                                         /* of word */
       if( strcmp ( command, "distribution" ) == 0 )
	 {
           distribution( word_1, dist, n_word );
           printf( " distribution: %d %d %d\n\n", 
                            dist[0], dist[1], dist[2] ); 
	 }
     }

}





