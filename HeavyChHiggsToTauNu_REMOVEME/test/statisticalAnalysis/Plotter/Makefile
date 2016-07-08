files = $(wildcard src/*.cc)
OBJS = $(addsuffix .o,$(basename $(files)))

ROOTINC := $(shell root-config --cflags | sed -e 's/-I/-isystem /')
ROOTLIBDIR := $(shell root-config --libdir)
ROOTLIBS := $(shell root-config --glibs)

OPT = -O -Wall -fPIC -D_REENTRANT

#INC = -I.. -I$(ROOTSYS)/include
INC = -I.. $(ROOTINC)

LIBS = -L.. -lPlotter -L$(ROOTLIBDIR) $(ROOTLIBS)

.cc.o:
#	$(CXX) $(OPT) $(INC) -c $*.cc
	$(CXX) $(OPT) $(INC) -c -o $@ $<

all:
	@$(MAKE) compile; $(MAKE) ../libPlotter.so

compile: $(OBJS)

../libPlotter.so: $(OBJS)
	$(CXX) -shared -O $(OBJS) -o ../libPlotter.so

clean:
	rm $(OBJS) ../libPlotter.so *.C *.exe

