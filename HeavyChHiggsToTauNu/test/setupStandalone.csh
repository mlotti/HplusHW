# Script for setting up standalone environment (i.e. without CMSSW
# release area) for accessing the python libraries and scripts.
#
# Usage:
#
# In HiggsAnalysis/HeavyChHiggsToTauNu/test do
# source setupStandalone.csh

#set pwd $PWD
if( ! -e .python) then
    mkdir -p .python
endif
if( ! -e .python/HiggsAnalysis) then
    mkdir -p .python/HiggsAnalysis
    touch .python/HiggsAnalysis/__init__.py
endif
if( ! -e .python/HiggsAnalysis/HeavyChHiggsToTauNu) then
    ln -s ${PWD}/../../HeavyChHiggsToTauNu/python .python/HiggsAnalysis/HeavyChHiggsToTauNu
    touch .python/HiggsAnalysis/HeavyChHiggsToTauNu/__init__.py
    foreach d (.python/HiggsAnalysis/HeavyChHiggsToTauNu/*)
        if(  -d $d ) touch $d/__init__.py
    end
endif

if( ${?PYTHONPATH} ) then
    setenv PYTHONPATH ${PYTHONPATH}:${PWD}/.python
else
    setenv PYTHONPATH ${PWD}/.python
endif

setenv PATH ${PATH}:${PWD}/../../HeavyChHiggsToTauNu/scripts
setenv CMSSW_BASE ${PWD}/../../../..
