#! /bin/csh -f
  if ($#argv != 1) then
        echo "Usage: $0 <pseudo-milticrab>"
        echo "Copies <pseudo-milticrab> from FNAL LPC machine locally"
        goto done
    endif

# Save command line args in variables
set MCRAB=$1

# set WORKPATH=/uscms_data/d3/aattikis/workspace/cmssw/CMSSW_8_0_30/src/HiggsAnalysis/NtupleAnalysis/src/FakeBMeasurement/work
set WORKPATH=/afs/cern.ch/user/a/attikis/scratch0/CMSSW_8_1_0/src/HiggsAnalysis/NtupleAnalysis/src/LimitCalc/work/limits2018
rsync --partial --progress -r ${MCRAB} attikis@lxplus.cern.ch:${WORKPATH}/.
