##########################
#
# Overall configuration
#
##########################

ifeq "$(HIGGSANALYSIS_BASE)" ""
$(error $$HIGGSANALYSIS_BASE is not defined, please do first 'cd ..; source setup.(c)sh; cd NtupleAnalysis')
endif
BASEDIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# Source code directory
SRCDIR := $(BASEDIR)/src

# Include files
INC := -I$(SRCDIR) -I$(BASEDIR)/external -I$(HIGGSANALYSIS_BASE)

# Directory where to put objects and dependency files
OBJDIR := $(BASEDIR)/obj

# Directory where to put the resulting library
LIBDIR := $(BASEDIR)/lib

# Directory where the tests are
TESTDIR := $(BASEDIR)/test

# ROOT
ROOTINC := $(shell root-config --cflags)
#ROOTLIBDIR := $(shell root-config --libdir)
ROOTLIBS := $(shell root-config --glibs)

# Compile flags
CXXFLAGS := -O2 -Wall -Wno-unused-local-typedefs -fPIC -D_REENTRANT $(ROOTINC) $(INC)
CXXEXTRAFLAGS := 

GCC_NEED_ZX := $(shell expr `gcc -dumpversion | cut -f2 -d.` \<= 6)
ifeq "$(GCC_NEED_ZX)" "1"
    CXXFLAGS += -std=c++0x
else
    CXXFLAGS += -std=c++11
endif

# Link flags
LDFLAGS := $(ROOTLIBS) -lProof -lGenVector -lTreePlayer -Llib

# Debugging
ifeq "$(DEBUG)" "yes"
CXXFLAGS += -g
LDFLAGS += -g
endif

# Platform dependent flags
HOST=$(shell hostname)
ifeq "$(findstring lxplus,$(HOST))" "lxplus"
CXXEXTRAFLAGS += -D HOST_LXPLUS
endif

#GIT_COMMIT_ID := $(shell git rev-parse HEAD)

##########################
#
# Default target
#
##########################

default: build

##########################
#
# Source files and target
#
##########################

ALL_DEPENDS :=

FILES_SRC := $(wildcard $(SRCDIR)/*/src/*.cc)
#FILES_HEADER := $(wildcard $(SRCDIR)/*/interface/*.h)
LIBNAMESHORT := HPlusAnalysis
LIBNAME := lib$(LIBNAMESHORT).so

##########################
#
# Dictionary sources
#
##########################

FILES_LINKDEF := $(wildcard $(SRCDIR)/*/src/*Linkdef.h)
FILES_DICT := $(patsubst $(SRCDIR)%,$(OBJDIR)%,$(subst Linkdef.h,Dict.cc,$(FILES_LINKDEF)))
FILES_DICTHEAD := $(FILES_DICT:.cc=.h)
FILES_SRC += $(FILES_DICT)

##########################
#
# Test sources and executable
#
##########################

TEST_MAIN := $(TESTDIR)/main
TEST_SRC := $(wildcard $(TESTDIR)/*.cc)
TEST_OBJ := $(patsubst $(BASEDIR)%,$(OBJDIR)%,$(TEST_SRC:.cc=.o))
TEST_DEP := $(TEST_OBJ:.o=.d)
ALL_DEPENDS += $(TEST_DEP)

test: $(TEST_MAIN)
	@./test/runTests.sh

##########################
#
# Object and dependency files
#
##########################

FILES_OBJ := $(patsubst $(SRCDIR)%,$(OBJDIR)%,$(FILES_SRC:.cc=.o))
FILES_DEP := $(FILES_OBJ:.o=.d)
ALL_DEPENDS += $(FILES_DEP)
LIBPATH := $(LIBDIR)/$(LIBNAME)

build: $(LIBPATH)

##########################
#
# Targets
#
##########################

.PHONY: all build test default clean

all: build test
all: ;

CLEAN_FILES := $(FILES_OBJ) $(ALL_DEPENDS) $(LIBPATH) $(FILES_DICT) $(FILES_DICTHEAD) $(TEST_OBJ) $(TEST_MAIN)

clean:
	rm -f $(CLEAN_FILES)

# GNU Make's own filter function is too limited
# http://stackoverflow.com/questions/6145041/makefile-filter-out-strings-containing-a-character
FILTER = $(foreach v,$(2),$(if $(findstring $(1),$(v)),$(v),))
cleanSubdirectory:
	rm -f $(call FILTER,$(SUBDIRECTORY),$(CLEAN_FILES))

# Include dependency information
-include $(ALL_DEPENDS)

# Compilation rule
# $(OBJDIR)/%.o: $(SRCDIR)/%.cc
# 	@[ -d $(@D) ] || mkdir -p $(@D)
# 	$(CXX) $(CXXFLAGS) -c $< -o $@ -MMD
# 	@cp $(OBJDIR)/$*.d $(OBJDIR)/$*.d.tmp; \
# 	  sed 's#\($(OBJDIR)/$*\)\.o[ :]*#\1.o \1.d : #g' < $(OBJDIR)/$*.d.tmp > $(OBJDIR)/$*.d; \
# 	  sed -e 's/#.*//' -e 's/^[^:]*: *//' -e 's/ *\\$$//' \
# 	      -e '/^$$/ d' -e 's/$$/ :/' -e 's/ *//' < $(OBJDIR)/$*.d.tmp >> $(OBJDIR)/$*.d; \
# 	  rm $(OBJDIR)/$*.d.tmp

define BUILD_template
$(1)/%.o: $(2)/%.cc
	@[ -d $$(@D) ] || mkdir -p $$(@D)
	$(CXX) $(CXXFLAGS) $(CXXEXTRAFLAGS) -c $$< -o $$@ -MMD
	@cp $(1)/$$*.d $(1)/$$*.d.tmp; \
	  sed 's#\($(1)/$$*\)\.o[ :]*#\1.o \1.d : #g' < $(1)/$$*.d.tmp > $(1)/$$*.d; \
	  sed -e 's/#.*//' -e 's/^[^:]*: *//' -e 's/ *\\$$$$//' \
	      -e '/^$$$$/ d' -e 's/$$$$/ :/' -e 's/ *//' < $(1)/$$*.d.tmp >> $(1)/$$*.d; \
	  rm $(1)/$$*.d.tmp
	@cp $(OBJDIR)/Framework/src/*.pcm $(LIBDIR)/.	
endef
$(eval $(call BUILD_template,$(OBJDIR),$(SRCDIR)))
$(eval $(call BUILD_template,$(OBJDIR)/test,$(TESTDIR)))

# Link rule
$(LIBPATH): $(FILES_OBJ) $(LIBDIR)
	$(CXX) $(FILES_OBJ) $(LDFLAGS) -shared -o $@

# in case the directory doesn't exist...
$(LIBDIR):
	mkdir $@

# Dictionary rule
# rootcint does not like -std=c++11
define DICT_template
$(1)_DICT := $$(patsubst $(SRCDIR)%,$(OBJDIR)%,$$(subst Linkdef.h,Dict.cc,$(1)))
$(1)_CLASSES := $$(shell fgrep //HPlus $(1) | sed -e 's|//HPlus||')
$(1)_HEADERPATH := $$(patsubst %src/,%interface/,$$(dir $(1)))
$(1)_HEADERS := $$(patsubst %,$$($(1)_HEADERPATH)%.h,$$($(1)_CLASSES))
$$($(1)_DICT): $$($(1)_HEADERS) $(1)
	rootcint -f $$@ -c $(filter-out -std=c++11,$(CXXFLAGS)) -p $$(patsubst $(SRCDIR)/%,%,$$^)
endef
$(foreach linkdef,$(FILES_LINKDEF),$(eval $(call DICT_template,$(linkdef))))

#obj/Framework/src/FrameworkDict.cc: src/Framework/interface/SelectorImp.h src/Framework/src/FrameworkLinkdef.h
#	rootcint -f $@ -c $(filter-out -std=c++11,$(CXXFLAGS)) -p $(patsubst src/%,%,$^)

# Test rule
$(TEST_MAIN): $(TEST_OBJ) $(LIBPATH)
	$(CXX) $(TEST_OBJ) $(LDFLAGS) -l$(LIBNAMESHORT) -o $@

