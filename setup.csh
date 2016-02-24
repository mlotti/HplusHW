# Script for setting up standalone environment (i.e. without CMSSW
# release area) for accessing the python libraries and scripts.
#
# Usage:
#
# In HiggsAnalysis do
# source setup.csh

# Note: tested so far LOCATION="" and LOCATION="jade"

if ( $?HIGGSANALYSIS_BASE ) then
    echo "Standalone environment already loaded"
    exit
endif

set LOCATION=""
if ( $?CMSSW_BASE ) then
    set LOCATION="CMSSW"
endif

# detect lxplus and jade
if ( $LOCATION == "" ) then
    if (`hostname` =~ "lxplus"* ) then
        set LOCATION="lxplus"
    else if (`hostname` =~ "jade"* ) then
	set LOCATION="jade"
    endif
endif

setenv HIGGSANALYSIS_BASE $PWD

if ( $LOCATION == "lxplus" ) then
#    echo "Sourcing lxplus environments for gcc 4.8 and ROOT 5.34"
    echo "Sourcing lxplus environments for gcc 4.8 and ROOT 6.02"
    source /afs/cern.ch/sw/lcg/contrib/gcc/4.8/x86_64-slc6-gcc48-opt/setup.csh

#    setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.23/x86_64-slc6-gcc48-opt/root
#    setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/6.02.05/x86_64-slc6-gcc48-opt/root
    setenv ROOTSYS /afs/cern.ch/sw/lcg/app/releases/ROOT/6.04.00/x86_64-slc6-gcc48-opt/root

    setenv LD_LIBRARY_PATH "${ROOTSYS}/lib:${LD_LIBRARY_PATH}"
    setenv PATH "${ROOTSYS}/bin:${PATH}"

    if ($?PYTHONPATH) then
        setenv PYTHONPATH "$ROOTSYS/lib:$PYTHONPATH"
    else
        setenv PYTHONPATH "$ROOTSYS/lib"
    endif 
#    pushd $ROOTSYS >/dev/null 
#    source bin/thisroot.csh
#    popd >/dev/null
endif

set LD_LIBRARY_PATH_APPEND=""
if ( $LOCATION == "jade" ) then
    # Hand-picked from CMSSW_7_4_0_pre6 slc6_amd64_gcc491
    # To update
    # - create a developer area (cmsrel)
    # - source the environment (cmsenv)
    # - look the new paths with 'scram tool list' and 'scram tool info'

    # scram tool info gcc-cxxcompiler
    set GCC_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms

    # scram tool info root_interface
#    setenv ROOTSYS /cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/root/5.34.22-cms2
    setenv ROOTSYS /cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/root/6.02.00-cms4

    # scram tool info xrootd
    set XROOTD_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/xrootd/4.0.4

    # scram tool info xz
    set XZ_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/xz/5.0.3__5.1.2alpha-cms

    # scram tool info python
    set PYTHON_BASE=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/python/2.7.6-cms

    set LD_LIBRARY_PATH_APPEND=$ROOTSYS/lib:$GCC_BASE/lib64:$GCC_BASE/lib:$XROOTD_BASE/lib:$XZ_BASE/lib:$PYTHON_BASE/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/libjpg/8b-cms/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/libpng/1.6.16/lib

    setenv PATH $ROOTSYS/bin:$GCC_BASE/bin:$XROOTD_BASE/bin:$PATH

    if ($?PYTHONPATH) then
	setenv PYTHONPATH "$ROOTSYS/lib:$PYTHONPATH"
    else
	setenv PYTHONPATH "$ROOTSYS/lib"
    endif
#    pushd $ROOTSYS >/dev/null
#    source bin/thisroot.csh
#    popd >/dev/null
endif

set LD_LIBRARY_PATH_APPEND="$HIGGSANALYSIS_BASE/NtupleAnalysis/lib:${LD_LIBRARY_PATH_APPEND}"
if ( ! $?LD_LIBRARY_PATH ) then
    setenv LD_LIBRARY_PATH "${LD_LIBRARY_PATH_APPEND}"
else
    setenv LD_LIBRARY_PATH "${LD_LIBRARY_PATH_APPEND}:${LD_LIBRARY_PATH}"
endif
if ( $LOCATION == "CMSSW" ) then
    if ( ! $?CMSSW_BASE || ! -e $CMSSW_BASE/python/HiggsAnalysis/NtupleAnalysis ) then
        ln -s $HIGGSANALYSIS_BASE/NtupleAnalysis/python $CMSSW_BASE/python/HiggsAnalysis/NtupleAnalysis
    endif

endif

# Need to create the following also on lxplus for limit calculation
if ( ! -e .python/HiggsAnalysis ) then
    mkdir -p .python/HiggsAnalysis
    touch .python/HiggsAnalysis/__init__.py
endif
foreach DIR ( NtupleAnalysis HeavyChHiggsToTauNu )
    if ( ! -e .python/HiggsAnalysis/$DIR ) then
        ln -s $HIGGSANALYSIS_BASE/$DIR/python .python/HiggsAnalysis/$DIR
        touch .python/HiggsAnalysis/$DIR/__init__.py
        foreach d ( .python/HiggsAnalysis/$DIR/* )
            if ( -d $d ) then
                touch $d/__init__.py
            endif
        end
    endif
end
foreach DIR ( `ls NtupleAnalysis/src` )
    if ( ! -e .python/HiggsAnalysis/$DIR && -e $HIGGSANALYSIS_BASE/NtupleAnalysis/src/$DIR/python ) then
        ln -s $HIGGSANALYSIS_BASE/NtupleAnalysis/src/$DIR/python .python/HiggsAnalysis/$DIR
        touch .python/HiggsAnalysis/$DIR/__init__.py
        foreach d ( .python/HiggsAnalysis/$DIR/* )
            if ( -d $d ) then
                touch $d/__init__.py
            endif
        end
    endif
end

if ( -z PYTHONPATH ) then
    setenv PYTHONPATH "${PWD}/.python"
else
    setenv PYTHONPATH "${PWD}/.python:${PYTHONPATH}"
endif

setenv PATH "${HIGGSANALYSIS_BASE}/HeavyChHiggsToTauNu/scripts:${HIGGSANALYSIS_BASE}/NtupleAnalysis/scripts:${PATH}"

# Install externals if necessary
sh +x installexternals.sh

# echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
# echo "!" 
# echo "! This file needs to be updated, please see setup.sh for an example"
# echo "!" 
# echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
# 
# 
# #set pwd $PWD
# if( ! -e .python) then
#     mkdir -p .python
# endif
# if( ! -e .python/HiggsAnalysis) then
#     mkdir -p .python/HiggsAnalysis
#     touch .python/HiggsAnalysis/__init__.py
# endif
# if( ! -e .python/HiggsAnalysis/HeavyChHiggsToTauNu) then
#     ln -s ${PWD}/../../HeavyChHiggsToTauNu/python .python/HiggsAnalysis/HeavyChHiggsToTauNu
#     touch .python/HiggsAnalysis/HeavyChHiggsToTauNu/__init__.py
#     foreach d (.python/HiggsAnalysis/HeavyChHiggsToTauNu/*)
#         if(  -d $d ) touch $d/__init__.py
#     end
# endif
# 
# if( ${?PYTHONPATH} ) then
#     setenv PYTHONPATH ${PWD}/.python:${PYTHONPATH}
# else
#     setenv PYTHONPATH ${PWD}/.python
# endif
# 
# setenv PATH ${PATH}:${PWD}/../../HeavyChHiggsToTauNu/scripts
# setenv HIGGSANALYSIS_BASE ${PWD}/../..
