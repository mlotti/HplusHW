#!/bin/sh

ARGS=""

if [ "x$#" = "x0" -o "x$#" = "x1" ]; then
    echo "Usage:"
    echo "  hplusHaddEdm.sh output.root input1.root [input2.root ...]"
    exit 1
fi

ARGS="outputFile=$1"
I=0
for ARG in $@; do
    if [ "x$I" != "x0" ]; then
        ARGS+=" inputFiles=$ARG"
    fi
    I=1
done
#echo $ARGS


CFG=$CMSSW_BASE/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/merge/merge_cfg.py
#cmsRun $CFG $ARGS | fgrep -v Initiating | fgrep -v Successfully | fgrep -v Closed
cmsRun $CFG $ARGS
