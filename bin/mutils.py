from mpi4py import MPI
import numpy as np
import sys
import math as m

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

  comm = MPI.COMM_SELF.Spawn(cmd, arg, nprocs)
  return comm     

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


def exit(comm):
  """ 
  Stop execution.

  Parameters:
  -----------
  comm: MPI communicator
     An MPI Intracommunicator.

  Modification History:
  ---------------------
  2014-04-20  patricio  Initial implementation. pcubillos@fulbrightmail.org
  2014-05-06  Madison   Ported implementation to Commloop
  2014-05-30  Madison   Revised for purpose in Commloop
  """
  comm.Barrier()
  comm.Disconnect()

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

def planck(T=1400, wave=[1e-8, 1e-4]):
  """ 
  Generates a Planck distribution at a specified blackbody temperature,
  over a defined wavelength spectral range.

  Parameters:
  -----------
  T: int
      Temperature of blackbody object [units: Kelvin]
  wave: list of int
      Wavelength boundaries to integrate over (in nm steps) [units: meter]

  Modification History:
  ---------------------
  2014-05-22  Madison   Initial implementation.
  """

  h = 6.83e-34 # J/s
  c = 3e8      # m/s
  T = 1400     # K
  k = 1.38e-23 # J/K
  nWaves = (wave[1] - wave[0]) / 1e-9
  planck = np.ones(nWaves)
  waves = np.ones(nWaves)
  wave1 = wave[0]
  for i in np.arange(nWaves):
    wave = wave1 + i*1e-9
    bottom = (np.exp((h * c) / (wave * k * T)) - 1)
    top = ((2 * h * c**2) / wave**5)
    planck[i] = top / bottom
    waves[i] = wave
  return planck, waves
