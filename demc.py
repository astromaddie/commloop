#!/usr/bin/env python
from mpi4py import MPI
import numpy as np
import sys
import timeit
import optparse

#start = timeit.default_timer()
# Create nprocs number of processes of eaach worker script, spawn communicators,
#  and send them the number of processes
nprocs = 10
iterat = 100

# initialise parser
parser = optparse.OptionParser("usage: %prog [options] [arg1]")

# add options
group = optparse.OptionGroup(parser, "Wavelength Options")
group.add_option("-p", "--num-procs", action="store",
                 help="Number of worker processes per spawn [default: %default]",
                 dest="procnum", type="int", default=10)
# add group to parser
parser.add_option_group(group)
# retrieve all options and arguments:
(options, args) = parser.parse_args()

nprocs = options.procnum

def mpi_spawn(exe, type):
  if type == "c":
    comm = MPI.COMM_SELF.Spawn(sys.executable, args=["worker"], maxprocs=nprocs)
  else:
    comm = MPI.COMM_SELF.Spawn(sys.executable, args=["worker."+type, "--"+exe], maxprocs=nprocs)
  return comm

def mpi_scatter(comm, array, type):

  comm.Barrier()

  # Check array contents type, then scatter accordingly.
  # If elements are not int or float, exit function.
  comm.Scatter([array, type], None, root=MPI.ROOT)

def mpi_gather(comm, array):
  comm.Barrier()
  # Check if the array can be gathered to
  if len(array) % nprocs != 0:
    print("Array must be a multiple of nprocs: {0}".format(nprocs))
    return 0
  comm.Gather(None, array, root=MPI.ROOT)
  return array

def mpi_barrier(comm, quit=False):
  comm.Barrier()
  if quit == True:
    comm.Disconnect()

# Add Spawn into a function
comm1 = mpi_spawn("incon", "py")
comm2 = mpi_spawn("transit", "c")
comm3 = mpi_spawn("outcon", "py")

# Test arrays
array1 = np.ones(10*nprocs, dtype='d')*1.1
array2 = np.zeros(1000*nprocs, dtype='d')
array3 = np.zeros(1e6*nprocs, dtype='d')
array4 = np.zeros(10*nprocs, dtype='d')

#start_loop = timeit.default_timer()
end_loop = np.zeros(nprocs, dtype='i')

# Communication loop between input converter, transit, and output converter
# DEMC is the hub
# Make this into a while loop
while np.mean(end_loop) < 1:
#for x in np.arange(iterat):
  # Add Barrier() and Scatter() into a function.
  # Add Gather() into a function

  # Scatter array1 through input converter communicator
  print("array1: {0}".format(array1))
  mpi_scatter(comm1, array1, MPI.DOUBLE)
  array2 = mpi_gather(comm1, array2)

  # Scatter array2 through transit communicator
  print("array2: {0}".format(array2))
  mpi_scatter(comm2, array2, MPI.DOUBLE)
  array3 = mpi_gather(comm2, array3)

  # Scatter array3 through transit communicator
  print("array3: {0}".format(array3))
  mpi_scatter(comm3, array3, MPI.DOUBLE)
  array4 = mpi_gather(comm3, array4)

  print("array4: {0}".format(array4))
  array1 = array4

  if np.mean(array1) > 100000:
    print("In here")
    end_loop += 1

  mpi_scatter(comm3, end_loop, MPI.INT)
  mpi_scatter(comm2, end_loop, MPI.INT)
  mpi_scatter(comm1, end_loop, MPI.INT)

  if np.mean(end_loop) == True:
    print("array1, array2, array3: {0} {1} {2}".format(np.mean(array1), np.mean(array2), np.mean(array3)))
    print("BREAK")
    break

 # if x == 0:
 #   split = timeit.default_timer()
 # elif x == iterat-2:
 #   last_split = timeit.default_timer()
 # elif x == iterat-1:
 #   last_loop = timeit.default_timer()

# Orders each worker to halt until all have caught up
# Then close communicators
print("I got out!")
mpi_barrier(comm1, quit=True)
mpi_barrier(comm2, quit=True)
mpi_barrier(comm3, quit=True)

#stop = timeit.default_timer()

#print("Time Til Loop: {4} s. \nFirst loop: {0} s. \nLast loop: {5} s. \nTotal Runtime: {3} s. \nLoop Runtime: {2} s. \nAverage loop: {1} s.".format((split - start_loop), (stop - split)/iterat, stop-split, stop-start, start_loop-start, last_loop-last_split))

