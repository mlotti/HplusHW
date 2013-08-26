#!/bin/sh

ARGS=""

if [ "x$#" = "x0" ]; then
    echo "Usage:"
    echo "  hplusHltTable.sh file.root"
    echo "  hplusHltTable.sh inputFiles=file.root hltProcess=HLTPROCESSNAME"
    echo
    echo "Use the latter form if the HLT process name is something else than HLT"
elif [ "x$#" = "x1" ]; then
    ARGS="inputFiles=$1"
else
    ARGS=$*
fi

CFG=$CMSSW_BASE/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/hltTableAnalyzer_cfg.py
cmsRun $CFG $ARGS | fgrep -v Initiating | fgrep -v Successfully | fgrep -v Closed
