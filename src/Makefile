#Makefile for building the C worker
SRC		= worker_c.c
IFILE		= worker_c

# C compilation variables
CC		= mpicc
CFLAGS		= -fPIC

python::
	@echo "Compiling code"
	@$(CC) $(CFLAGS) -o $(IFILE) $(SRC)
	@echo "Moving file to bin/"
	@mv worker_c ../bin
