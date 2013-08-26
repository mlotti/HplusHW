ROOTINC := $(shell root-config --cflags | sed -e 's/-I/-isystem /')
ROOTLIBDIR := $(shell root-config --libdir)
ROOTLIBS := $(shell root-config --glibs)

OPT = -O -Wall -fPIC -D_REENTRANT

INC = -I.. $(ROOTINC)

LIBS = -L../.. -lPlotter -L$(ROOTLIBDIR) $(ROOTLIBS)

all:
	@cd .. && $(MAKE) --no-print-directory
	@$(CXX) test.cpp $(INC) $(LIBS) -o test.exe
	@./test.exe
clean:
	rm *.C *.exe

