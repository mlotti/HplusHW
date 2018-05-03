#!/bin/csh
#====================================================================================================
# Before running the following script, make sure you have installed the CombineHarvester tools
#
# cd $CMSSW_BASE/src
# git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
# cd CombineHarvester
# scram b -j 6
# 
# Last Used:
# 
# ./doPulls.csh combine_datacard_hplushadronic_m500.txt higgsCombineblinded_m500.AsymptoticLimits.mH500.root 500
#
# The txt and root files can be found under the CombineResults_taujets_<date>_<time> folder inside your datacard folder
#
# Relevant links:
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/SWGuideNonStandardCombineUses#Nuisance_parameter_impacts
# http://cms-analysis.github.io/CombineHarvester/index.html
# https://www.gitbook.com/book/cms-hcomb/combine/details
#====================================================================================================

#===========================================================
# Ensure all script arguments are passed from command line
#===========================================================
if ($#argv != 3) then
    echo "=== You must give exactly 3 arguments:"
    echo "1 = Your datacard txt file,  e.g. combine_datacard_hplushadronic_m500.txt"
    echo "2 = Your datacard root file, e.g. higgsCombineblinded_m500.AsymptoticLimits.mH500.root"
    echo "3 = The mass point you want to examine, e.g. 500"
    echo "\n=== For example:"
    echo "./doPulls.csh combine_datacard_hplushadronic_m500.txt higgsCombineblinded_m500.AsymptoticLimits.mH500.root 500"
    echo
    exit 1
endif


#===================
# Define Variables
#===================
set DATACARD_TXT  = ${1}
set DATACARD_ROOT = ${2}
set MASS          = ${3}

echo "=== Building workspace"
text2workspace.py $DATACARD_TXT -m $MASS -o $DATACARD_ROOT

echo "=== Fit for each POI"
combineTool.py -M Impacts -d $DATACARD_ROOT -m $MASS --doInitialFit --robustFit 1 -t -1 --expectSignal=1.0 --expectSignalMass=$MASS

echo "=== Fit scan for each nuisance parameter"
combineTool.py -M Impacts -d $DATACARD_ROOT -m $MASS --robustFit 1 --doFits -t -1 --expectSignal=1.0 --expectSignalMass=$MASS --parallel 8

echo "=== Collect the output and write results into a json file"
combineTool.py -M Impacts -d $DATACARD_ROOT -m $MASS -t -1 -o impacts_$MASS.json

echo "=== Plot Impacts"
plotImpacts.py -i impacts_$MASS.json -o impacts$MASS
