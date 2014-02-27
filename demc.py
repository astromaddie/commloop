#!/usr/bin/env python
from mpi4py import MPI
import numpy as np
import sys
import timeit

start = timeit.default_timer()
# Create nprocs number of processes of eaach worker script, spawn communicators,
#  and send them the number of processes
nprocs = 10
iterat = 10000
#print("Spawning {0} processes.".format(nprocs))

comm1 = MPI.COMM_SELF.Spawn(sys.executable, args=["incon.py"],   maxprocs=nprocs)
comm2 = MPI.COMM_SELF.Spawn(sys.executable, args=["transit.py"], maxprocs=nprocs)
comm3 = MPI.COMM_SELF.Spawn(sys.executable, args=["outcon.py"],  maxprocs=nprocs)

procarray = np.ones(nprocs, dtype='i')*iterat

comm1.Scatter([procarray, MPI.INT], None, root=MPI.ROOT)
comm2.Scatter([procarray, MPI.INT], None, root=MPI.ROOT)
comm3.Scatter([procarray, MPI.INT], None, root=MPI.ROOT)

comm1.Barrier()
comm2.Barrier()
comm3.Barrier()

# Starting condition:
array1 = np.ones(10*nprocs, dtype='d')*3.589

#print("Before DEMC loop: {0}".format(array1))
start_loop = timeit.default_timer()
# Communication loop between input converter, transit, and output converter
# DEMC is the hub
for x in np.arange(iterat):
  # Scatter array1 through input converter communicator
  comm1.Barrier()
  comm1.Scatter([array1, MPI.INT], None, root=MPI.ROOT)
  array2 = np.zeros(1000*nprocs, dtype='d')
  comm1.Gather(None, array2, root=MPI.ROOT)

  # Scatter array2 through transit communicator
  comm2.Barrier()
  comm2.Scatter([array2, MPI.INT], None, root=MPI.ROOT)
  array3 = np.zeros(1e6*nprocs, dtype='d')
  comm2.Gather(None, array3, root=MPI.ROOT)

  # Scatter array3 through transit communicator
  comm3.Barrier()
  comm3.Scatter([array3, MPI.DOUBLE], None, root=MPI.ROOT)
  array4 = np.zeros(10*nprocs, dtype='d')
  comm3.Gather(None, array4, root=MPI.ROOT)

  # Reformat array1 to match array4, restart the loop
#  array1 = np.array(array4)

#  print("DEMC Loop {0}: {1}".format(x, array1))

  if x == 0:
    split = timeit.default_timer()
  elif x == iterat-2:
    last_split = timeit.default_timer()
  elif x == iterat-1:
    last_loop = timeit.default_timer()

# Orders each worker to halt until all have caught up
comm1.Barrier()
comm2.Barrier()
comm3.Barrier()

stop = timeit.default_timer()

print(array1)

# Close communicators
comm1.Disconnect()
comm2.Disconnect()
comm3.Disconnect()

print("Time Til Loop: {4} s. \nFirst loop: {0} s. \nLast loop: {5} s. \nTotal Runtime: {3} s. \nLoop Runtime: {2} s. \nAverage loop: {1} s.".format((split - start_loop), (stop - split)/iterat, stop-split, stop-start, start_loop-start, last_loop-last_split))
