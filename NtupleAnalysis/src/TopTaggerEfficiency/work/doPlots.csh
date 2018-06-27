#!/bin/csh

#================================================================================================
# Ensure all script arguments are passed from command line
#================================================================================================
if ($#argv != 1) then
    echo "=== You must give exactly 1 argument:"
    echo "1=PSEUDO_MCRAB_DIR"
    echo "\n=== For example:"
    echo "./doPlots.csh /uscms_data/d3/mkolosov/workspace/pseudo-multicrab/TopTaggerEfficiency/TopTaggerEfficiency_180608_194156_massCut300_All"
    echo
    exit 1
endif

#================================================================================================ 
# Define variables                                                                                                                   
#================================================================================================
set INITIAL = `echo $USER | cut -c1-1`
set PSEUDO_MCRAB_DIR = ${1}

./plot_EfficiencySystTop.py -m $PSEUDO_MCRAB_DIR --type showerScales
./plot_EfficiencySystTop.py -m $PSEUDO_MCRAB_DIR --type highPtRadiation
./plot_EfficiencySystTop.py -m $PSEUDO_MCRAB_DIR --type mTop
./plot_EfficiencySystTop.py -m $PSEUDO_MCRAB_DIR --type partonShower
./plot_EfficiencySystTop.py -m $PSEUDO_MCRAB_DIR --type evtGen

./mergeJSONs.py
