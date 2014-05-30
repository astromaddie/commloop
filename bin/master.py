#!/usr/bin/env python
from mpi4py import MPI
import mutils as mu
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

# Terminal Flag Parser
# Initialise parser
parser = argparse.ArgumentParser("usage: %prog [options] [arg1]")

# Add options
group = parser.add_argument_group('Runtime Options')
group.add_argument("-p", "--num-procs", action="store",
                 help="Number of worker processes per spawn [default: %default]",
                 dest="procnum", type=int, default=10)
group.add_argument("-i", "--num-iter", action="store",
                 help="Number of iterations to loop through [default: %default]",
                 dest="numiter", type=int, default=10)
group.add_argument("-g", "--benchmark", action="store_true", dest="bench", 
                 default="False")

# Retrieve all options and arguments:
options = parser.parse_args()
spawn   = options.procnum
iterat  = options.numiter
bench   = options.bench

if bench == True:
  start_mpi = timeit.default_timer()

# Spawn the communicators
comm0 = mu.comm_spawn(sys.executable, ["worker.py"], 1)
comm1 = mu.comm_spawn(sys.executable, ["worker.py"], spawn)
comm2 = mu.comm_spawn("worker_c", None,  spawn)
comm3 = mu.comm_spawn(sys.executable, ["worker.py"], spawn)

# Sample arrays and their lengths
array1 = np.ones(10*spawn, dtype='d')
lnarr1 = np.ones(10, dtype='i')*(len(array1) / spawn)
lnarr10 = np.ones(1, dtype='i')*len(array1) # array1 for master

array2 = np.zeros(1e3*spawn, dtype='d')
lnarr2 = np.ones(10, dtype='i')*(len(array2) / spawn)

array3 = np.zeros(1e6*spawn, dtype='d')
lnarr3 = np.ones(10, dtype='i')*(len(array3) / spawn)

array4 = np.ones(10*spawn, dtype='d')*1.1
lnarr4 = np.ones(10, dtype='i')*(len(array4) / spawn)
lnarr40 = np.ones(1, dtype='i')*len(array4) # array4 for master

if bench == True:
  start_loop = timeit.default_timer()
  loop_timer = []
  loop_timer2 = []

# Scatter the array lengths to their workers
print(lnarr40)
mu.comm_scatter(comm0, lnarr40, mpitype=MPI.INT)
mu.comm_scatter(comm0, lnarr10, mpitype=MPI.INT)
print("Got through to 1")
mu.comm_scatter(comm1, lnarr1,  mpitype=MPI.INT)
mu.comm_scatter(comm1, lnarr2,  mpitype=MPI.INT)
print("Got through to 2")

mu.comm_scatter(comm3, lnarr3,  mpitype=MPI.INT)
mu.comm_scatter(comm3, lnarr4,  mpitype=MPI.INT)
print("Got through to 3")

# Bcast iterat to all workers
niterat = np.asarray([iterat], 'i')
mu.comm_bcast(comm0, niterat, MPI.INT)
mu.comm_bcast(comm1, niterat, MPI.INT)
mu.comm_bcast(comm2, niterat, MPI.INT)
mu.comm_bcast(comm3, niterat, MPI.INT)
print("Bcasted to all workers")


# Communication loop between 1 Master, 2 pyWorkers, & 1 C worker
# Master acts as the hub
while iterat >= 0:
  print(iterat)
  if bench == True:
    loop_timer.append(timeit.default_timer())

  # Scatter init array4 to zeroth pyWorker communicator
  mu.comm_scatter(comm0, array4, mpitype=MPI.DOUBLE)
  array1 = mu.comm_gather(comm0, array1)

  # Scatter array1 to first pyWorker communicator
  mu.comm_scatter(comm1, array4, mpitype=MPI.DOUBLE)
  array2 = mu.comm_gather(comm1, array2)

  # Scatter array2 to C worker communicator
  mu.comm_scatter(comm2, array2, mpitype=MPI.DOUBLE)
  array3 = mu.comm_gather(comm2, array3)

  # Scatter array3 to second pyWorker communicator
  mu.comm_scatter(comm3, array3, mpitype=MPI.DOUBLE)
  array4 = mu.comm_gather(comm3, array1)

  print("array4: {0}".format(np.mean(array4)))

  # Countdown iterations to end loop
  iterat -= 1

  if bench == True:
    loop_timer2.append(timeit.default_timer() - loop_timer[-1])

print("Exited the loop!")
# Orders each worker to halt until all have caught up
# Then close communicators
mu.exit(comm0)
print("Closed 1")
mu.exit(comm1)
print("Closed 2")
mu.exit(comm2)
print("Closed 3")
mu.exit(comm3)
print("Closed 4")

print("Finished disconnecting.")

if bench == True:
  stop = timeit.default_timer()

if bench == True:
  print("Total time taken: {0}s".format(stop - start))
  print("Time to start MPI communicators: {0}s".format(start_loop - start_mpi))
  print("Time to run first loop: {0}s".format(loop_timer[1] - loop_timer[0]))
  print("Time to run last loop: {0}s".format(loop_timer[-1] - loop_timer[-2]))
  print("Time to run avg loop: {0}s".format(np.mean(loop_timer2)))
