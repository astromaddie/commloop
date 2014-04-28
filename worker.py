from mpi4py import MPI
import numpy as np
import argparse

'''
 * MPI CommLoop - Python Worker
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

# Open communications with the Master
comm = MPI.Comm.Get_parent()
rank  = comm.Get_rank()
size  = comm.Get_size()

# MPI Functions
def comm_scatter(array):
  comm.Barrier()
  comm.Scatter(None, array, root=0)
  return array

def comm_gather(array, type):
  # Check array contents type, then scatter accordingly.
  # If elements are not int or float, exit function.
  comm.Barrier()
  comm.Gather([array, type], None, root=0)

def comm_barrier():
  comm.Barrier()

def worker_loop(array_1, array_2, end_loop):
  array_1 = comm_scatter(array_1)
  scale = np.mean(array_1) * 1.000001
  array_2 = np.multiply(array_2, scale)
  comm_gather(array_2, MPI.DOUBLE)
  return array_2

# Sample arrays
# Array lengths are passed from master.py
#   array1
arrsiz = np.ones(1, dtype='i')
arrsiz = comm_scatter(arrsiz)
array1 = np.ones(arrsiz[0], dtype='d')
#   array2
arrsiz = comm_scatter(arrsiz)
array2 = np.ones(arrsiz[0], dtype='d')
# Flag to determine when to exit the loop
end_loop = np.zeros(1, dtype='i')
#print("Array lengths: {0}, {1}".format(len(array1), len(array2)))
# Worker loop, communicating with Master
while end_loop[0] == False:
  if np.mean(end_loop) == True:
    break
  array2 = worker_loop(array1, array2, end_loop)
  end_loop = comm_scatter(end_loop)

# Close communications and disconnect
comm.Barrier()
comm.Disconnect()
