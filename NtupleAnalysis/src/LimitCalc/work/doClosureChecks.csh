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
# git checkout v7.0.8 -v v7.0.8
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
# Last Used:
# ./doClosureChecks.csh 500
#
# Relevant links:
# [1] https://cms-hcomb.gitbooks.io/combine/content/part1/index.html#combine-tool
# [2] https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/HiggsPAGPreapprovalChecks
#====================================================================================================

#===========================================================
# Ensure all script arguments are passed from command line
#===========================================================
if ($#argv != 1) then
    echo "=== You must give the mass point you want to examine, e.g. 500"
    echo "\n=== For example:"
    echo "./doClosureChecks.csh 500"
    echo
    exit 1
endif

#===================
# Define Variables
#===================
set MASS          = ${1}
set DATACARD_TXT  = "combine_datacard_hplushadronic_m${1}.txt"
set DATACARD_ROOT = "combine_datacard_hplushadronic_m${1}.root"

echo "----------------------------------"
echo " Building workspace"
echo "----------------------------------"
text2workspace.py $DATACARD_TXT

echo "-----------------------------------------------------------------------------------------------------------"
echo " Run combine to produce a background-only Asimob toy and fit it. The result of the fit should be r=0"
echo "-----------------------------------------------------------------------------------------------------------"
combine -M MaxLikelihoodFit -t -1 --expectSignal 0 $DATACARD_ROOT

echo "----------------------------------"
echo " Run diffNuisances.py"
echo "----------------------------------"
python diffNuisances.py -a fitDiagnostics.root -g plots.root

echo "-----------------------------------------------------------------------------------------------------------"
echo " Run combine to produce a signal+background Asimov toy and fit it. The result of the fit should be r=1"
echo "-----------------------------------------------------------------------------------------------------------"
combine -M MaxLikelihoodFit -t -1 --expectSignal 1 $DATACARD_ROOT

echo "----------------------------------"
echo " Run diffNuisances.py"
echo "----------------------------------"
python diffNuisances.py -a fitDiagnostics.root -g plots.root

echo "----------------------------------"
echo "End of script"
echo "----------------------------------"

