#from mpi4py import MPI
import worker_c as c

print("Imported the SWIG-wrapped worker, about to call main")
#c.worker_loop(int(5))
c.worker_loop(0, None)
