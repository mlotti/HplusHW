.PHONY: all test clean cleanAll

all:
	$(MAKE) -C ../../..

test:
	$(MAKE) -C ../../.. test

DIRTMP := $(dir $(PWD))
export SUBDIRECTORY := $(shell basename $(DIRTMP))
clean:
	$(MAKE) -C ../../../ cleanSubdirectory

cleanAll:
	$(MAKE) -C ../../../ clean
