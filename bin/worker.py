from mpi4py import MPI
import numpy as np
import argparse
import mutils as mu

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

def worker_loop(array_1, array_2, end_loop):
  array_1 = mu.comm_scatter(comm, array_1)
  scale = np.mean(array_1) * 1.000001
  array_2 = np.multiply(array_2, scale)
  mu.comm_gather(comm, array_2, mpitype=MPI.DOUBLE)
  return array_2

# Sample arrays
# Array lengths are passed from master.py
#   array1
arrsiz = np.ones(1, dtype='i')
arrsiz = mu.comm_scatter(comm, arrsiz)
array1 = np.ones(arrsiz[0], dtype='d')
#   array2
arrsiz = mu.comm_scatter(comm, arrsiz)
array2 = np.ones(arrsiz[0], dtype='d')

# Flag to determine when to exit the loop
end_loop = np.zeros(1, dtype='i')

# Worker loop, communicating with Master
while end_loop[0] == False:
  if np.mean(end_loop) == True:
    break
  array2 = worker_loop(array1, array2, end_loop)
  end_loop = mu.comm_scatter(comm, end_loop)

# Close communications and disconnect
mu.exit(comm=comm)
