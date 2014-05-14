from mpi4py import MPI
import numpy as np
import sys

def comm_spawn(cmd, arg, nprocs):
  """ 
  Spawn a worker and return the communicator.

  Parameters:
  -----------
  comm: MPI communicator
     The MPI Intracommunicator instance
  worker: string
     Filename of worker to spawn
  nprocs: int
     Number of processes to spawn of worker
  ext: string
     Extension of file to spawn. [Default: python]
  arg: string
     Command-line argument for worker spawning [Default: empty]

  Modification History:
  ---------------------
  05-14-2014	Madison		Initial implementation. madison.stemm@gmail.com
  """

  MPI.COMM_SELF.Spawn(cmd, arg, nprocs)
  return comm     
#  if ext == 'py':
#    arg = [worker]
#    comm = MPI.COMM_SELF.Spawn(sys.executable, arg, nprocs)
#  elif:
#    comm = MPI.COMM_SELF.Spawn(worker, arg, nprocs)
#  return comm

def comm_scatter(comm, array, mpitype=None):
  """ 
  Scatter to send or receive an MPI array.

  Parameters:
  -----------
  comm: MPI communicator
     The MPI Intracommunicator instance.
  array: 1D ndarray
     The array transferred.
  mpitype: MPI data type
     The data type of the array to be send (if not None). If None,
     assume it is receiving an array.

  Notes:
  ------
  Determine whether to send or receive an array depending on 'mpitype'

  Modification History:
  ---------------------
  2014-03-24  Madison   Initial implementation. Madison Stemm, UCF.
  2014-04-13  patricio  Documented.  pcubillos@fulbrightmail.org.
  2014-04-18  patricio  Joined master and worker routines.
  2014-05-06  Madison   Ported implementation to Commloop
  """
  comm.Barrier()
  if mpitype is None:  # Receive
    comm.Scatter(None, array, root=0)
    return array
  else:                # Send
    comm.Scatter([array, mpitype], None, root=MPI.ROOT)


def comm_gather(comm, array, mpitype=None):
  """ 
  Gather to send or receive an MPI array.

  Parameters:
  -----------
  comm: MPI communicatior
     The MPI Intracommunicator.
  array: 1D ndarray
     The array transferred.
  mpitype: MPI data type
     The data type of the array to be send (if not None). If None,
     assume it is receiving an array.

  Modification History:
  ---------------------
  2014-03-24  Madison   Initial implementation. Madison Stemm, UCF.
  2014-04-13  patricio  Documented.  pcubillos@fulbrightmail.org
  2014-04-18  patricio  Joined master and worker routines.
  2014-05-06  Madison   Ported implementation to Commloop
  """
  comm.Barrier()
  if mpitype is None:  # Receive
    comm.Gather(None, array,            root=MPI.ROOT)
    return array
  else:                # Send
    comm.Gather([array, mpitype], None, root=0)


def comm_bcast(comm, array, mpitype=None):
  """ 
  Broadcast to send or receive an MPI array.

  Parameters:
  -----------
  comm: MPI communicatior
     The MPI Intracommunicator.
  array: 1D ndarray
     The array transferred.
  mpitype: MPI data type
     The data type of the array to be send (if not None). If None,
     assume it is receiving an array.

  Modification History:
  ---------------------
  2014-04-18  patricio  Initial implementation. pcubillos@fulbrightmail.org
  2014-05-06  Madison   Ported implementation to Commloop
  """
  comm.Barrier()
  if mpitype is None:  # Receive
    comm.Bcast(array,            root=0)
  else:                # Send
    comm.Bcast([array, mpitype], root=MPI.ROOT)


def exit(comm=None, abort=False, message=None, comm2=None):
  """ 
  Stop execution.

  Parameters:
  -----------
  comm: MPI communicator
     An MPI Intracommunicator.
  abort: Boolean
     If True send (gather) an abort flag integer through comm.
  message: String
     Print message on exit.

  Modification History:
  ---------------------
  2014-04-20  patricio  Initial implementation. pcubillos@fulbrightmail.org
  2014-05-06  Madison   Ported implementation to Commloop
  """
  if message is not None:
    print(message)
  if comm is not None:
    if abort:
      comm_gather(comm, np.array([1]), MPI.INT)
    comm.Barrier()
    comm.Disconnect()
  if comm2 is not None:
    comm2.Barrier()
    comm2.Disconnect()
  sys.exit(0)

def progressbar(frac):
   """ 
   Print out to screen a progress bar, percentage and current time.

   Parameters:
   -----------
   frac: Float
      Fraction of the task that has been completed, ranging from 0.0 (none)
      to 1.0 (completed).

   Modification History:
   ---------------------
   2014-04-19  patricio  Initial implementation.
  2014-05-06  Madison   Ported implementation to Commloop
   """
   barlen = int(np.clip(10*frac, 0, 10))
   bar = ":"*barlen + " "*(10-barlen)
   print("\n[%s] %5.1f%% completed  (%s)"%(bar, 100*frac, time.ctime()))
