#!/usr/bin/env python
from mpi4py import MPI
import numpy as np
import sys
import timeit
import argparse

start = timeit.default_timer()

'''
 * MPI CommLoop - Python Master
 * by Madison Stemm
 * Completed 3/24/2014
 *
 * This file is part of CommLoop.
 *
 * CommLoop is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * CommLoop is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with CommLoop.  If not, see <http://www.gnu.org/licenses/>.
'''
# Create nprocs number of processes of eaach worker script, spawn communicators,
#  and send them the number of processes
nprocs = 10
iterat = 10

# Terminal Flag Parser
# Initialise parser
parser = argparse.ArgumentParser("usage: %prog [options] [arg1]")

# Add options
group = parser.add_argument_group('Runtime Options')
group.add_argument("-p", "--num-procs", action="store",
                 help="Number of worker processes per spawn [default: %default]",
                 dest="procnum", type=int, default=10)
group.add_argument("-g", "--benchmark", action="store_true", dest="bench", 
                 default="False")

# Retrieve all options and arguments:
options = parser.parse_args()
nprocs = options.procnum
bench = options.bench

# MPI Functions
def comm_spawn(type):
  if type == "c":
    comm = MPI.COMM_SELF.Spawn(sys.executable, args=["worker_c_wrapper.py"], maxprocs=nprocs)
  elif type == 'py':
    comm = MPI.COMM_SELF.Spawn(sys.executable, args=["worker.py"], maxprocs=nprocs)
  return comm

def comm_scatter(comm, array, type):

  comm_barrier(comm)
  comm.Scatter([array, type], None, root=MPI.ROOT)

def comm_gather(comm, array):
  comm_barrier(comm)
  comm.Gather(None, array, root=MPI.ROOT)
  return array

def comm_barrier(comm, quit=False):
  comm.Barrier()
  if quit == True:
    comm.Disconnect()

if bench == True:
  start_mpi = timeit.default_timer()

# Spawn the communicators
comm0 = comm_spawn("py")
comm1 = comm_spawn("py")
comm2 = comm_spawn("c")
comm3 = comm_spawn("py")

# Sample arrays and their lengths
array1 = np.ones(10*nprocs, dtype='d')*1.1
lnarr1 = np.ones(10, dtype='i')*(len(array1) / nprocs)
array2 = np.zeros(1000*nprocs, dtype='d')
lnarr2 = np.ones(10, dtype='i')*(len(array2) / nprocs)
array3 = np.zeros(1e6*nprocs, dtype='d')
lnarr3 = np.ones(10, dtype='i')*(len(array3) / nprocs)
array4 = np.ones(10*nprocs, dtype='d')*1.1
lnarr4 = np.ones(10, dtype='i')*(len(array4) / nprocs)

# Flag to exit loop
end_loop = np.zeros(nprocs, dtype='i')

if bench == True:
  start_loop = timeit.default_timer()
  loop_timer = []
  loop_timer2 = []

# Scatter the array lengths to their workers
comm_scatter(comm0, lnarr4, MPI.INT)
comm_scatter(comm0, lnarr1, MPI.INT)
comm_scatter(comm1, lnarr1, MPI.INT)
comm_scatter(comm1, lnarr2, MPI.INT)
comm_scatter(comm3, lnarr3, MPI.INT)
comm_scatter(comm3, lnarr4, MPI.INT)

# Communication loop between 1 Master, 2 pyWorkers, & 1 C worker
# Master acts as the hub
while np.mean(end_loop) < 1:

  if bench == True:
    loop_timer.append(timeit.default_timer())

  # Scatter init array4 to zeroth pyWorker communicator
  comm_scatter(comm0, array4, MPI.DOUBLE)
  array1 = comm_gather(comm0, array1)

  # Scatter array1 to first pyWorker communicator
  comm_scatter(comm1, array1, MPI.DOUBLE)
  array2 = comm_gather(comm1, array2)

  # Scatter array2 to C worker communicator
  comm_scatter(comm2, array2, MPI.DOUBLE)
  array3 = comm_gather(comm2, array3)

  # Scatter array3 to second pyWorker communicator
  comm_scatter(comm3, array3, MPI.DOUBLE)
  array4 = comm_gather(comm3, array4)

  # Set array1 to output array4 and begin loop again
  array1 = array4

  # Countdown iterations to end loop
  iterat -= 1
  if iterat == 0:
    end_loop += 1

  # Scatter the endloop flag
  comm_scatter(comm3, end_loop, MPI.INT)
  comm_scatter(comm2, end_loop, MPI.INT)
  comm_scatter(comm1, end_loop, MPI.INT)
  comm_scatter(comm0, end_loop, MPI.INT)

  if bench == True:
    loop_timer2.append(timeit.default_timer() - loop_timer[-1])

  # Exit!
  if np.mean(end_loop) == True:
    break

# Orders each worker to halt until all have caught up
# Then close communicators
comm_barrier(comm0, quit=True)
comm_barrier(comm1, quit=True)
comm_barrier(comm3, quit=True)

if bench == True:
  stop = timeit.default_timer()

if bench == True:
  print("Total time taken: {0}s".format(stop - start))
  print("Time to start MPI communicators: {0}s".format(start_loop - start_mpi))
  print("Time to run first loop: {0}s".format(loop_timer[1] - loop_timer[0]))
  print("Time to run last loop: {0}s".format(loop_timer[-1] - loop_timer[-2]))
  print("Time to run avg loop: {0}s".format(np.mean(loop_timer2)))
