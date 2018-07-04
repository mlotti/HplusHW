#!/bin/csh

#====================================================================================================
# Before running the following script, make sure you have installed the Combine tool as described in [1]
#
# setenv SCRAM_ARCH slc6_amd64_gcc530
# cmsrel CMSSW_8_1_0
# cd CMSSW_8_1_0/src 
# cmsenv
# git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit 
# cd HiggsAnalysis/CombinedLimit
# cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
# git fetch origin
# git checkout v7.0.9 -b v7.0.9
# scramv1 b clean; scramv1 b # always make a clean build
#
# In order to run this script cd to the CombineResults directory inside the datacard:
# cd <datacards_*/CombineResults*>
# 
# Copy the diffNuisances.py file
# wget https://raw.githubusercontent.com/cms-analysis/HiggsAnalysis-CombinedLimit/master/test/diffNuisances.py
#
# The closure checks done with this scripts are described in the Higgs PAG preapproval TWiki [2]
#
# Last Used (default seed):
# cd <datacards_*/CombineResults*>
# ../../.././doClosureChecks.csh 500
#
#
# Relevant links:
# [1] https://cms-hcomb.gitbooks.io/combine/content/part1/index.html#combine-tool
# [2] https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/HiggsPAGPreapprovalChecks
#====================================================================================================

#===========================================================
# Ensure all script arguments are passed from command line
#===========================================================
if ($#argv < 1) then
    echo "=== You must give the mass point you want to examine, e.g. 500"
    echo "\n=== For example:"
    echo "./doClosureChecks.csh 500"
    echo
    exit 1
endif

# Set default random seed
if ($#argv != 2) then
        set SEED = 123456
else
        set SEED = $2
endif

#===================
# Define Variables
#===================
set MASS          = ${1}
set MINOS         = "poi" # [Options: "all" "poi" "none"]
set RMIN          = 0
set RMAX          = 20
set NUISANCES     = "diffNuisances.py"
set DATACARD_TXT  = "combine_datacard_hplushadronic_m${1}.txt"
set DATACARD_ROOT = "combine_datacard_hplushadronic_m${1}.root"
set FILE          = "ClosureChecks_m${1}.txt"
set NEWLINE       = "\n======================================================================================================="
set LINE          = "======================================================================================================="

echo $NEWLINE >> $FILE
echo " Building workspace" >> $FILE
echo $LINE >> $FILE
text2workspace.py $DATACARD_TXT >> $FILE

echo $NEWLINE>> $FILE
echo "Step 1) Run combine to produce a background-only Asimov toy and fit it. The result of the fit should be r=0" >> $FILE
echo $LINE >> $FILE
# combine -M MaxLikelihoodFit -t -1 --expectSignal 0 $DATACARD_ROOT >> $FILE #obsolete (30 May 2018)
combine -M FitDiagnostics -t -1 --expectSignal 0 --rMin $RMIN --rMax $RMAX $DATACARD_ROOT --seed $SEED --minos $MINOS >> $FILE

echo $NEWLINE >> $FILE
echo "Step 2) Run diffNuisances.py" >> $FILE
echo $LINE >> $FILE
if ( -f $NUISANCES ) then
    echo " Nuisances script found"
else
    echo " Nuisances script not found. Dowloading it with wget"
    wget https://raw.githubusercontent.com/cms-analysis/HiggsAnalysis-CombinedLimit/master/test/$NUISANCES
endif
python diffNuisances.py -a fitDiagnostics.root -g pulls_BkgAsimov_m${1}.root >> $FILE
#python diffNuisances.py -a fitDiagnostics.root -g pulls_BkgAsimov_m${1}.root --absolute >> $FILE

echo $NEWLINE >> $FILE
echo "Step 3) Run combine to produce a signal+background Asimov toy and fit it. The result of the fit should be r=1" >> $FILE
echo $LINE >> $FILE
#combine -M MaxLikelihoodFit -t -1 --expectSignal 1 $DATACARD_ROOT --seed $SEED >> $FILE #obsolete (30 May 2018)
combine -M FitDiagnostics -t -1 --expectSignal 1 --rMin $RMIN --rMax $RMAX $DATACARD_ROOT --seed $SEED --minos $MINOS >> $FILE

echo $NEWLINE >> $FILE
echo "Step 4) Run diffNuisances.py" >> $FILE
echo $LINE >> $FILE
python diffNuisances.py -a fitDiagnostics.root -g pulls_SBAsimov_m${1}.root >> $FILE
#python diffNuisances.py -a fitDiagnostics.root -g pulls_SBAsimov_m${1}.root --absolute >> $FILE

echo $NEWLINE >> $FILE
echo "DONE" >> $FILE
echo $LINE >> $FILE

