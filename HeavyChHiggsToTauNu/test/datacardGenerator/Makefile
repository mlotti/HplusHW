OBJS := $(patsubst %.cc,%.o,$(wildcard *.cc))

ROOTINC := $(shell root-config --cflags | sed -e 's/-I/-isystem /')
ROOTLIBDIR := $(shell root-config --libdir)
ROOTLIBS := $(shell root-config --glibs)

OPT = -O -Wall -fPIC -D_REENTRANT -g

INC = -I. -I$(ROOTINC)

LIBS = -L$(ROOTLIBDIR) $(ROOTLIBS) -L.

%.o: %.cc
	$(CXX) $(OPT) $(INC) $(LIBS) $< -o $@ -c -g

all: $(OBJS)
#	@echo $(OBJS)
	$(CXX) $(OPT) $(INC) $(LIBS) $(OBJS) -o datacardgenerator
	@echo "Program compiled"
