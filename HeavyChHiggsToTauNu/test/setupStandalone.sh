# Script for setting up standalone environment (i.e. without CMSSW
# release area) for accessing the python libraries and scripts.
#
# Usage:
#
# In HiggsAnalysis/HeavyChHiggsToTauNu/test do
# source setupStandalone.sh

pwd=$PWD
if [ ! -e .python/HiggsAnalysis ]; then
    mkdir -p .python/HiggsAnalysis
    touch .python/HiggsAnalysis/__init__.py
fi
if [ ! -e .python/HiggsAnalysis/HeavyChHiggsToTauNu ]; then
    ln -s $PWD/../../HeavyChHiggsToTauNu/python .python/HiggsAnalysis/HeavyChHiggsToTauNu
    touch .python/HiggsAnalysis/HeavyChHiggsToTauNu/__init__.py
    for d in .python/HiggsAnalysis/HeavyChHiggsToTauNu/*; do
        if [ -d $d ]; then
            touch $d/__init__.py
        fi
    done
fi

if [ "x$PYTHONPATH" = "x" ]; then
    export PYTHONPATH=$PWD/.python
else
    export PYTHONPATH=$PWD/.python:$PYTHONPATH
fi

#export PATH=$PATH:$PWD/../scripts
export PATH=$PATH:$PWD/../../HeavyChHiggsToTauNu/scripts
export CMSSW_BASE=$PWD/../../../..
