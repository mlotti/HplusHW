ROOTINC := $(shell root-config --cflags | sed -e 's/-I/-isystem /')
ROOTLIBDIR := $(shell root-config --libdir)
ROOTLIBS := $(shell root-config --glibs)

OPT = -O -Wall -fPIC -D_REENTRANT -g

INC = -I. -I$(ROOTINC)

LIBS = -L$(ROOTLIBDIR) $(ROOTLIBS) -L.


all:
	@$(CXX) $(OPT) generateTauIDFactorizationMap.cc $(INC) $(LIBS) -o generateTauIDFactorizationMap
	@echo "Program compiled"
