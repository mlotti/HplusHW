#!/bin/bash
#====================================================================================================
# DESCRIPTION:
# 
#
#
# LAST USED:
# ./GoF.csh combine_datacard_hplushadronic_m500.txt
#
# USEFUL LINKS:
#
#
#====================================================================================================

#====================================================================================================
# Ensure all script arguments are passed from command line
#====================================================================================================
if [ $# -eq 0 ]
then
    echo "=== You must give exactly 1 argument; the datacard txt file name. For example:"
    echo "./GoF.csh 500"
    echo
    exit 1
fi

#====================================================================================================
# Define Variables
#====================================================================================================
nToys=1000
nJobs=50
queue="8nm"
toysPerJob=$((nToys/nJobs))
datacard="combine_datacard_hplushadronic_m${1}.txt"

echo "=== Run GoF for $nToys toys over $nJobs for card $1 (#toys per job = $toysPerJob)"

for (( t=1; t<=$nJobs; t++ ))
do
    echo "=== Submit job for toys $t/$nJobs"
    combineTool.py -m ${1} -M GoodnessOfFit --algorithm saturated ${datacard} -t $toysPerJob --job-mode lxbatch --sub-opts="-q 8nm" --task-name $t -n toys$t --seed "$((123456*$t))"
done


echo "=== Run job on data:"
combineTool.py -m ${1} -M GoodnessOfFit --algorithm saturated ${datacard} -t 0 -n Data
