OBJS := $(patsubst %.cxx,%.o,$(wildcard *.cxx))

ROOTINC := $(shell root-config --cflags | sed -e 's/-I/-isystem /')
ROOTLIBDIR := $(shell root-config --libdir)
ROOTLIBS := $(shell root-config --glibs)

OPT = -O -Wall -fPIC -D_REENTRANT -g

INC = -I. -I$(ROOTINC) -I.

LIBS = -L$(ROOTLIBDIR) $(ROOTLIBS) -L.

%.o: %.cxx
	$(CXX) $(OPT) $(INC) $(LIBS) $< -o $@ -c -g

all: $(OBJS)
#	@echo $(OBJS)
	$(CXX) $(OPT) $(INC) $(LIBS) $(OBJS) -o makeControlPlots
	@echo "Program compiled"
