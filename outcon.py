from mpi4py import MPI
import numpy as np

comm3 = MPI.Comm.Get_parent()
rank  = comm3.Get_rank()
size  = comm3.Get_size()
name  = "OutputConverter"

#print("This is {0}.{1}. There are {2} of us.".format(name, rank, size))

# Get number processes
nprocs = np.array(0, dtype='i')
comm3.Scatter(None, nprocs, root=0)
comm3.Barrier()

for x in range(nprocs):

  # Pause until DEMC contacts Output Converter again
  comm3.Barrier()

  # Receive array3 from DEMC
  array3 = np.zeros(1e6, dtype='d')
  comm3.Scatter(None, array3, root=0)
  #print("{0}.{1} received array3 {2}".format(name, rank, array3))

  # Send off array4 to DEMC
  array4 = np.ones(10, dtype='d')*8.3201
  comm3.Gather([array4, MPI.INT], None, root=0)
  #print("{0}.{1} sent off array4 {2}".format(name, rank, array4))

# Close communicators after all workers have caught up
comm3.Barrier()
comm3.Disconnect()
