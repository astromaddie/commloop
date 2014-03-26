#!/usr/bin/env python
from mpi4py import MPI
import numpy as np
import sys
import timeit
import optparse

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

################### Terminal Flag Parser ###################
# Initialise parser
parser = optparse.OptionParser("usage: %prog [options] [arg1]")

# Add options
group = optparse.OptionGroup(parser, "Wavelength Options")
group.add_option("-p", "--num-procs", action="store",
                 help="Number of worker processes per spawn [default: %default]",
                 dest="procnum", type="int", default=10)
# Add group to parser
parser.add_option_group(group)
# Retrieve all options and arguments:
(options, args) = parser.parse_args()
nprocs = options.procnum
############################################################

###################### MPI Functions #######################
def mpi_spawn(exe, type):
  if type == "c":
    comm = MPI.COMM_SELF.Spawn(sys.executable, args=["worker_c_wrapper.py"], maxprocs=nprocs)
  else:
    comm = MPI.COMM_SELF.Spawn(sys.executable, args=["worker."+type, "--"+exe], maxprocs=nprocs)
  return comm

def comm_scatter(comm, array, type):

  mpi_barrier(comm)
  comm.Scatter([array, type], None, root=MPI.ROOT)

def comm_gather(comm, array):
  mpi_barrier(comm)
  comm.Gather(None, array, root=MPI.ROOT)
  return array

def comm_barrier(comm, quit=False):
  comm.Barrier()
  if quit == True:
    comm.Disconnect()
#########################################################

# Spawn the communicators
comm1 = comm_spawn("incon", "py")
comm2 = comm_spawn("transit", "c")
comm3 = comm_spawn("outcon", "py")

# Sample arrays
array1 = np.ones(10*nprocs, dtype='d')*1.1
array2 = np.zeros(1000*nprocs, dtype='d')
array3 = np.zeros(1e6*nprocs, dtype='d')
array4 = np.zeros(10*nprocs, dtype='d')

# Flag to exit loop
end_loop = np.zeros(nprocs, dtype='i')

# Communication loop between 1 Master, 2 pyWorkers, & 1 C worker
# Master acts as the hub
while np.mean(end_loop) < 1:
  # Scatter array1 to first pyWorker communicator
  comm_scatter(comm1, array1, MPI.DOUBLE)
  array2 = mpi_gather(comm1, array2)

  # Scatter array2 to C worker communicator
  comm_scatter(comm2, array2, MPI.DOUBLE)
  array3 = mpi_gather(comm2, array3)

  # Scatter array3 to second pyWorker communicator
  comm_scatter(comm3, array3, MPI.DOUBLE)
  array4 = mpi_gather(comm3, array4)

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

  # Exit!
  if np.mean(end_loop) == True:
    break

# Orders each worker to halt until all have caught up
# Then close communicators
comm_barrier(comm1, quit=True)
comm_barrier(comm3, quit=True)
