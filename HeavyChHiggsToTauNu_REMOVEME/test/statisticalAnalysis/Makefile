ROOTINC := $(shell root-config --cflags | sed -e 's/-I/-isystem /')
ROOTLIBDIR := $(shell root-config --libdir)
ROOTLIBS := $(shell root-config --glibs)

OPT = -O -Wall -fPIC -D_REENTRANT

INC = -I. -I$(ROOTINC)

LIBS = -L$(ROOTLIBDIR) $(ROOTLIBS) -L. -lPlotter


all:
	@cd Plotter && $(MAKE)
	@$(CXX) tanbReach.cpp signif.cpp BR_top_Hplus_function.cpp $(INC) $(LIBS) -o tanbReach

