#!/bin/bash
#====================================================================================================
# DESCRIPTION:
# 
#
# EXAMPLES:
# ./GoF.sh 500 saturated
# ./GoF.sh 500 AD
# ./GoF.sh 500 KS
#
#
# LAST USED:
# ./GoF.sh 180 saturated && ./GoF.sh 180 KS && ./GoF.sh 180 KS
#
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
    echo "./GoF.csh 500 saturated"
    echo
    exit 1
fi

if [ "${2}" != "saturated" ] && [ "${2}" != "KS" ]  && [ "${2}" != "AD" ]
then
    echo "=== Invalid algorith \"${2}\". Please select between \"saturated\", \"KS\", and \"AD\"."
    exit 1
fi


#====================================================================================================
# Define Variables
#====================================================================================================
nToys=10000
nJobs=50
queue="8nm"
toysPerJob=$((nToys/nJobs))
datacard="combine_datacard_hplushadronic_m${1}.txt"
rootfile="combine_histograms_hplushadronic_m${1}.root"
algorithm=${2} # "saturated", "KS" (Kolmogorov-Smirnov), AD (Anderson-Darling)
dirname="GoF_${algorithm}"

echo "=== Run GoF for $nToys toys over $nJobs for card $1 (#toys per job = $toysPerJob)"

if [ -d ${dirname} ]; then
    cp ${datacard} ${dirname}/.
    cp ${rootfile} ${dirname}/.
    cd ${dirname}
    #ls -lt
else
    mkdir ${dirname}
    cp ${datacard} ${dirname}/.
    cp ${rootfile} ${dirname}/.
    cd ${dirname}
    #ls -lt
fi

# For-loop: All jobs
echo "=== Submit job for toys (`pwd`)"
for (( t=1; t<=$nJobs; t++ ))
do
    echo "=== Submit job for toys $t/$nJobs"
    combineTool.py -m ${1} -M GoodnessOfFit --algorithm ${algorithm} ${datacard} -t $toysPerJob --job-mode lxbatch --sub-opts="-q 8nm" --task-name $t -n toys$t --seed "$((123456*$t))"
done

echo "=== Run job on data:(`pwd`)"
combineTool.py -m ${1} -M GoodnessOfFit --algorithm ${algorithm} ${datacard} -t 0 -n Data
cd ..

echo "=== Done"