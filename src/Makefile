#Makefile for building the SWIG-wrapped C worker
SRC		= worker_c.c
IFILE		= worker_c
INTERFACE	= $(IFILE).i
WRAPFILE	= $(IFILE)_wrap.c

# C compilation variables
CC		= mpicc
CFLAGS		= -fPIC -I/usr/include/python2.7 -c $(SRC) $(WRAPFILE)
LDFLAG		= -shared $(IFILE).o $(IFILE)_wrap.o -o _$(IFILE).so

python::
	@echo "Generating SWIG wrapper"
	@swig -python -o $(WRAPFILE) $(INTERFACE)
	@echo "Compiling code"
	@$(CC) $(CFLAGS)
	@echo "Linking object files"
	@$(CC) $(LDFLAG)
	@echo "Removing intermediary files..."
	@rm -rf *.o
	@rm -rf $(IFILE).py
