from mpi4py import MPI
import numpy as np
import optparse

# initialise parser
parser = optparse.OptionParser("usage: %prog [options] [arg1]")

# add options
parser.add_option("--incon", action="store_const", const="incon",
                  help="Spawn input converter worker.", dest="worker")
parser.add_option("--transit", action="store_const", const="transit",
                  help="Spawn transit worker.", dest="worker")
parser.add_option("--outcon", action="store_const", const="outcon",
                  help="Spawn output converter worker.", dest="worker")

# retrieve all options and arguments:
(options, args) = parser.parse_args()
worker_type = options.worker

comm = MPI.Comm.Get_parent()
rank  = comm.Get_rank()
size  = comm.Get_size()

if worker_type == "incon":
  name = "InputConverter"
  switch = 0
if worker_type == "transit":
  name = "Transit"
  switch = 1
if worker_type == "outcon":
  name = "OutputConverter"
  switch = 2

def mpi_scatter(array):
  comm.Barrier()
  comm.Scatter(None, array, root=0)
  print("Scattering to {0}".format(name))
  return array

def mpi_gather(array, type):
  comm.Barrier()
  # Check array contents type, then scatter accordingly.
  # If elements are not int or float, exit function.
  comm.Gather([array, type], None, root=0)
  print("Gathering from {0}".format(name))

def mpi_barrier():
  comm.Barrier()

def worker_loop(array_1, array_2, end_loop):
  array = mpi_scatter(array_1)
  array_2 = array_2 * (np.mean(array) * 1.2)
  mpi_gather(array_2, MPI.DOUBLE)
  return array_2

# Get number processes
#nprocs = np.array(0, dtype='i')
#mpi_scatter(comm, nprocs)

array1 = np.ones(10, dtype='d')
array2 = np.ones(1000, dtype='d')
array3 = np.ones(1e6, dtype='d')
array4 = np.ones(10, dtype='d')
end_loop = np.zeros(1, dtype='i')

while end_loop[0] == False:
  if np.mean(end_loop) == True:
    break
  if switch == 0:
    array2 = worker_loop(array1, array2, end_loop)
  elif switch == 1:
    array3 = worker_loop(array2, array3, end_loop)
  elif switch == 2:
    array4 = worker_loop(array3, array4, end_loop)
  end_loop = mpi_scatter(end_loop)
#  if end_loop[0] == True:
#    break
print("{0} {1} got out!".format(name, rank))
# Close communicators after all workers have caught up
comm.Barrier()
comm.Disconnect()

