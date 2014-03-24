from mpi4py import MPI
import numpy as np
import optparse

# MPI CommLoop - Python Worker
# by Madison Stemm
# Completed 3/24/2014
'''
 This file is part of CommLoop.

 CommLoop is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 CommLoop is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
'''

################### Terminal Flag Parser ###################
# Initialise parser
parser = optparse.OptionParser("usage: %prog [options] [arg1]")

# Add options
parser.add_option("--incon", action="store_const", const="incon",
                  help="Spawn input converter worker.", dest="worker")
parser.add_option("--transit", action="store_const", const="transit",
                  help="Spawn transit worker.", dest="worker")
parser.add_option("--outcon", action="store_const", const="outcon",
                  help="Spawn output converter worker.", dest="worker")

# Retrieve all options and arguments:
(options, args) = parser.parse_args()
worker_type = options.worker
############################################################

# Open communications with the Master
comm = MPI.Comm.Get_parent()
rank  = comm.Get_rank()
size  = comm.Get_size()

if worker_type == "incon":
  name = "InputConverter"
  switch = 0
if worker_type == "outcon":
  name = "OutputConverter"
  switch = 1

################### MPI Functions ###################
def mpi_scatter(array):
  comm.Barrier()
  comm.Scatter(None, array, root=0)
  return array

def mpi_gather(array, type):
  # Check array contents type, then scatter accordingly.
  # If elements are not int or float, exit function.
  comm.Barrier()
  comm.Gather([array, type], None, root=0)

def mpi_barrier():
  comm.Barrier()

def worker_loop(array_1, array_2, end_loop):
  array = mpi_scatter(array_1)
  array_2 = array_2 * (np.mean(array) * 1.2)
  mpi_gather(array_2, MPI.DOUBLE)
  return array_2
#####################################################

# Sample arrays
array1 = np.ones(10, dtype='d')
array2 = np.ones(1000, dtype='d')
array3 = np.ones(1e6, dtype='d')
array4 = np.ones(10, dtype='d')
end_loop = np.zeros(1, dtype='i')

# Worker loop, communicating with Master
while end_loop[0] == False:
  if np.mean(end_loop) == True:
    break
  if switch == 0:
    array2 = worker_loop(array1, array2, end_loop)
  elif switch == 1:
    array4 = worker_loop(array3, array4, end_loop)
  end_loop = mpi_scatter(end_loop)

# Close communications and disconnect
comm.Barrier()
comm.Disconnect()
