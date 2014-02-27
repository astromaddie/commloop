from mpi4py import MPI
import numpy as np

comm2 = MPI.Comm.Get_parent()
rank  = comm2.Get_rank()
size  = comm2.Get_size()
name  = "Transit"

#print("This is {0}.{1}. There are {2} of us.".format(name, rank, size))

# Get number processes
nprocs = np.array(0, dtype='i')
comm2.Scatter(None, nprocs, root=0)
comm2.Barrier()

for x in range(nprocs):

  # Pause until DEMC contacts Transit again
  comm2.Barrier()

  # Receive array2 from DEMC
  array2 = np.zeros(1000, dtype='d')
  comm2.Scatter(None, array2, root=0)
 # print("{0}.{1} received array2 {2}".format(name, rank, array2))

  # Send off array3 to DEMC
  array3 = np.ones(1e6, dtype='d')*8.39291
  comm2.Gather([array3, MPI.INT], None, root=0)
  #print("{0}.{1} sent off array3 {2}".format(name, rank, array3))

# Close communicators after all workers have caught up
comm2.Barrier()
comm2.Disconnect()
