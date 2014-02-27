from mpi4py import MPI
import numpy as np

comm1 = MPI.Comm.Get_parent()
rank  = comm1.Get_rank()
size  = comm1.Get_size()
name  = "InputConverter"

#print("This is {0}.{1}. There are {2} of us.".format(name, rank, size))

# Get number processes
nprocs = np.array(0, dtype='i')
comm1.Scatter(None, nprocs, root=0)
comm1.Barrier()

for x in range(nprocs):

  # Pause until DEMC contacts input converter again
  comm1.Barrier()

  # Receive array1 from DEMC
  array1 = np.zeros(1000, dtype='d')
  comm1.Scatter(None, array1, root=0)
  #print("{0}.{1} received array1 {2}".format(name, rank, array1))

  # Send array2 back to DEMC
  array2 = np.ones(1000, dtype='d')*3.6939
  comm1.Gather([array2, MPI.INT], None, root=0)
  #print("{0}.{1} sent off array2 {2}".format(name, rank, array2))

# Close communicators after all workers have caught up
comm1.Barrier()
comm1.Disconnect()
