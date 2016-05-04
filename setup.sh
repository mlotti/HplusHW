# Script for setting up standalone environment (i.e. without CMSSW
# release area) for accessing the python libraries and scripts.
#
# Usage:
#
# In HiggsAnalysis do
# source setup.sh


if [ "x$HIGGSANALYSIS_BASE" != "x" ]; then
    echo "Standalone environment already loaded"
    return
fi

LOCATION=""
if [ "x$CMSSW_BASE" != "x" ]; then
    LOCATION="CMSSW"
fi
# detect lxplus and jade
if [ "x$LOCATION" = "x" ]; then
    case "$HOSTNAME" in
        lxplus*) LOCATION="lxplus";;
        jade*) LOCATION="jade";;
    esac
fi

if [ "x$LOCATION" = "xlxplus" ]; then
#    echo "Sourcing lxplus environments for gcc 4.8 and ROOT 5.34"
    echo "Sourcing lxplus environments for gcc 4.8 and ROOT 6.02"
    source /afs/cern.ch/sw/lcg/contrib/gcc/4.8/x86_64-slc6-gcc48-opt/setup.sh

#    pushd /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.23/x86_64-slc6-gcc48-opt/root >/dev/null 
#    pushd /afs/cern.ch/sw/lcg/app/releases/ROOT/6.02.52/x86_64-slc6-gcc48-opt/root >/dev/null 
    pushd /afs/cern.ch/sw/lcg/app/releases/ROOT/6.04.00/x86_64-slc6-gcc48-opt/root >/dev/null
    source bin/thisroot.sh
    popd >/dev/null
fi

LD_LIBRARY_PATH_APPEND=""
if [ "x$LOCATION" = "xjade" ]; then
    # Hand-picked from CMSSW_7_4_0_pre6 slc6_amd64_gcc491
    # To update
    # - create a developer area (cmsrel)
    # - source the environment (cmsenv)
    # - look the new paths with 'scram tool list' and 'scram tool info'

    # scram tool info gcc-cxxcompiler
    GCC_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms

    # scram tool info root_interface
    #export ROOTSYS=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/root/5.34.22-cms2
    export ROOTSYS=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/root/6.02.00-cms4

    # scram tool info xrootd
    XROOTD_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/xrootd/4.0.4

    # scram tool info xz
    XZ_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/xz/5.0.3__5.1.2alpha-cms

    # scram tool info python
    PYTHON_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/python/2.7.6-cms

    LD_LIBRARY_PATH_APPEND=$GCC_BASE/lib64:$GCC_BASE/lib:$XROOTD_BASE/lib:$XZ_BASE/lib:$PYTHON_BASE/lib

    export PATH=$GCC_BASE/bin:$XROOTD_BASE/bin:$PATH

    pushd $ROOTSYS >/dev/null
    source bin/thisroot.sh
    popd >/dev/null
fi

export HIGGSANALYSIS_BASE=$PWD
LD_LIBRARY_PATH_APPEND=$HIGGSANALYSIS_BASE/NtupleAnalysis/lib:$LD_LIBRARY_PATH_APPEND

if [ "x$LD_LIBRARY_PATH" = "x" ]; then
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH_APPEND
else
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH_APPEND:$LD_LIBRARY_PATH
fi

export PPATHPREFIX=.python
if [ "x$LOCATION" = "xCMSSW" ]; then
    if [ ! -e $CMSSW_BASE/python/HiggsAnalysis/NtupleAnalysis ]; then
        ln -s $HIGGSANALYSIS_BASE/NtupleAnalysis/python $CMSSW_BASE/python/HiggsAnalysis/NtupleAnalysis
    fi
    PPATHPREFIX = "$CMSSW_BASE/python"
fi

# Need to create the following also on lxplus for limit calculation
if [ ! -e $PPATHPREFIX/HiggsAnalysis ]; then
    mkdir -p $PPATHPREFIX/HiggsAnalysis
    touch $PPATHPREFIX/HiggsAnalysis/__init__.py
fi
for DIR in NtupleAnalysis HeavyChHiggsToTauNu; do
    if [ ! -e $PPATHPREFIX/HiggsAnalysis/$DIR ]; then
        ln -s $HIGGSANALYSIS_BASE/$DIR/python $PPATHPREFIX/HiggsAnalysis/$DIR
        touch $PPATHPREFIX/HiggsAnalysis/$DIR/__init__.py
        for d in $PPATHPREFIX/HiggsAnalysis/$DIR/*; do
            if [ -d $d ]; then
                touch $d/__init__.py
            fi
        done
    fi
done
for DIR in `ls NtupleAnalysis/src` ; do
    if [[ ! -e $PPATHPREFIX/HiggsAnalysis/$DIR ]] && [[ -e $HIGGSANALYSIS_BASE/NtupleAnalysis/src/$DIR/python ]]; then
        ln -s $HIGGSANALYSIS_BASE/NtupleAnalysis/src/$DIR/python $PPATHPREFIX/HiggsAnalysis/$DIR
        touch $PPATHPREFIX/HiggsAnalysis/$DIR/__init__.py
        for d in $PPATHPREFIX/HiggsAnalysis/$DIR/*; do
            if [ -d $d ]; then
                touch $d/__init__.py
            fi
        done
    fi
done

if [ "x$PYTHONPATH" = "x" ]; then
    export PYTHONPATH=$PWD/.python
else
    export PYTHONPATH=$PWD/.python:$PYTHONPATH
fi

export PATH=$HIGGSANALYSIS_BASE/HeavyChHiggsToTauNu/scripts:$HIGGSANALYSIS_BASE/NtupleAnalysis/scripts:$PATH

# Install externals if necessary
sh +x installexternals.sh
