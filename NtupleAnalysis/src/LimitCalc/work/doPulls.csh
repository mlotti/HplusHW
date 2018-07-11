#!/bin/csh
#====================================================================================================
# Before running the following script, make sure you have installed the CombineHarvester tools
#
# PREREQUISITES:
# cd $CMSSW_BASE/src
# git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
# cd CombineHarvester
# scram b -j 6
# 
#
# LAST USED:
# cd <datacard_dir>/<CombineResults>
# ../../.././doPulls.csh 500

# (The TXT and ROOT files can be found under the CombineResults_taujets_<date>_<time> folder inside your datacard folder
#
#
# USEFUL LINKS:
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/SWGuideNonStandardCombineUses#Nuisance_parameter_impacts
# http://cms-analysis.github.io/CombineHarvester/index.html
# https://www.gitbook.com/book/cms-hcomb/combine/details
#====================================================================================================

#===========================================================
# Ensure all script arguments are passed from command line
#===========================================================
if ($#argv != 1) then
    #echo "=== You must give exactly 3 arguments:"
    #echo "1 = Your datacard txt file,  e.g. combine_datacard_hplushadronic_m500.txt"
    #echo "2 = Your datacard root file, e.g. higgsCombineblinded_m500.AsymptoticLimits.mH500.root"
    #echo "3 = The mass point you want to examine, e.g. 500"
    #echo "\n=== For example:"
    #echo "./doPulls.csh combine_datacard_hplushadronic_m500.txt higgsCombineblinded_m500.AsymptoticLimits.mH500.root 500"
    echo "=== You must give exactly 1 argument; The mass point you want to examine, e.g. 500"
    echo "\n=== For example:"
    echo "./doPulls.csh 500"
    echo
    exit 1
endif

#===================
# Define Variables
#===================
#set DATACARD_TXT  = ${1}
#set DATACARD_ROOT = ${2}
#set MASS          = ${3}
set MASS          = ${1}
set DATACARD_TXT  = combine_datacard_hplushadronic_m${MASS}.txt  
set DATACARD_ROOT = higgsCombineblinded_m${MASS}.AsymptoticLimits.mH${MASS}.root
set SEED          = 123456
set BACKGROUND    = "Impacts_BkgOnly_m${MASS}.txt"
set SIGNAL        = "Impacts_SB_m${MASS}.txt"
set RMIN          = -10 #0
set RMAX          = +20

echo "=== Building workspace"
text2workspace.py $DATACARD_TXT -m $MASS -o $DATACARD_ROOT

echo "**********************"
echo "   Background Only    "
echo "**********************"

echo "=== Fit for each POI"
combineTool.py -M Impacts -d $DATACARD_ROOT -m $MASS --doInitialFit --robustFit 1 -t -1 --expectSignal 0 --rMin $RMIN --rMax $RMAX --expectSignalMass $MASS --seed $SEED > $BACKGROUND

echo "=== Fit scan for each nuisance parameter"
combineTool.py -M Impacts -d $DATACARD_ROOT -m $MASS --robustFit 1 --doFits -t -1 --expectSignal 0 --rMin $RMIN --rMax $RMAX --expectSignalMass $MASS --parallel 8 --seed $SEED >> $BACKGROUND

echo "=== Collect the output and write results into a json file"
combineTool.py -M Impacts -d $DATACARD_ROOT -m $MASS -t -1 -o impacts_BkgAsimov_$MASS.json --seed $SEED >> $BACKGROUND

echo "=== Plot Impacts"
plotImpacts.py -i impacts_BkgAsimov_$MASS.json -o impacts_BkgAsimov_$MASS >> $BACKGROUND

echo "**********************"
echo " Signal + Background  "
echo "**********************"

echo "=== Fit for each POI"
combineTool.py -M Impacts -d $DATACARD_ROOT -m $MASS --doInitialFit --robustFit 1 -t -1 --expectSignal 1 --rMin $RMIN --rMax $RMAX --seed $SEED > $SIGNAL

echo "=== Fit scan for each nuisance parameter"
combineTool.py -M Impacts -d $DATACARD_ROOT -m $MASS --robustFit 1 --doFits -t -1 --expectSignal 1 --rMin $RMIN --rMax $RMAX --parallel 8 --seed $SEED >> $SIGNAL

echo "=== Collect the output and write results into a json file"
combineTool.py -M Impacts -d $DATACARD_ROOT -m $MASS -t -1 -o impacts_SBAsimov_$MASS.json --seed $SEED >> $SIGNAL

echo "=== Plot Impacts"
plotImpacts.py -i impacts_SBAsimov_$MASS.json -o impacts_SBAsimov_$MASS >> $SIGNAL
