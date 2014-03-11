/* file: hellosquare.c */
void sayhello(MPI_Comm comm){
  /* MPI C Hello World worker.
     Receives a double value, squares, and returns it to the source.
      */
  int size, rank, count=1, tag=77;
  int source=0;
  double msg, square;

  MPI_Comm_size(comm, &size);
  MPI_Comm_rank(comm, &rank);
  printf("Hello, World!, I am process %d of %d.\n", rank, size);

  if (rank == 1){
    // Format -> http://condor.cc.ku.edu/~grobe/docs/intro-MPI-C.shtml
    MPI_Recv(&msg, count, MPI_DOUBLE, source, tag, MPI_COMM_WORLD,
             MPI_STATUS_IGNORE);
    printf("Process %d received number: %.2f\n", rank, msg);
    // Square the number:
    square = msg*msg;
    // Send it back to source (=rank 0).
    MPI_Send(&square, count, MPI_DOUBLE, source, tag, MPI_COMM_WORLD); 
    printf("Square sent.\n");
  }

}
