#!/bin/sh

ARGS=""

if [ "x$#" = "x0" ]; then
    echo "Usage:"
    echo "  hplusEventContent.sh file.root"
    echo
elif [ "x$#" = "x1" ]; then
    ARGS="inputFiles=$1"
else
    ARGS=$*
fi

CFG=$CMSSW_BASE/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/eventContentAnalyzer_cfg.py
cmsRun $CFG $ARGS
