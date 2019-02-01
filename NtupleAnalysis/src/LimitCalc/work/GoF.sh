#!/bin/bash
#====================================================================================================
# DESCRIPTION:
# Used to conduct goodness-of-fit test which can  can be used to evaluate how compatible
# the observed data are with the model PDF (Probability Distribution Function). 
# The script can be run specifying the signal mass point (first script argumant)
# and an algorithm (second script argument) to deterimne the goodness-of-fit indicator for that
# algorithm and the data. The procedure is to first run on many toy MC datasets to determine the
#  distribution of the goodness-of-fit indicator and the run on the real data to be able to compare.
#
# When computing the goodness of fit, by default the signal strength is left floating in the fit, so 
# that the measure is independent from the presence or absence of a signal. It is possible to instead
# keep it fixed to some value by passing the option --fixedSignalStrength=<value>.
#
# The following algorithms are supported:
# 1) saturated: Compute a goodness-of-fit measure for binned fits based on the saturated model method, 
# as prescribed by the StatisticsCommittee (http://www.physics.ucla.edu/~cousins/stats/cousins_saturated.pdf).
# This quantity is similar to a chi-square, but can be computed for an arbitrary combination of binned 
# channels with arbitrary constraints.
#
# 2) KS: Compute a goodness-of-fit measure for binned fits using the Kolmogorov-Smirnov test. It is based
# on the highest difference between the Cumulative Distribution Function (CDF) and the empirical distribution
# function of any bin.
#
# 3) AD: Compute a goodness-of-fit measure for binned fits using the Anderson-Darling test. It is based 
# on the integral of the difference between the cumulative distribution function and the empirical distribution 
# function over all bins. It also gives the tail ends of the distribution a higher weighting.
#
#
# EXAMPLES:
# ./GoF.sh 500 saturated
# ./GoF.sh 500 AD
# ./GoF.sh 500 KS
#
#
# LAST USED:
# ./GoF.sh 180 saturated && ./GoF.sh 180 KS && ./GoF.sh 180 AD
#
#
# USEFUL LINKS:
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideHiggsAnalysisCombinedLimit#Goodness_of_fit_tests
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
jobMode=condor # interactive,script,lxbatch,SGE,condor,crab3 (NOTE: LXBATCH is decommissioned)

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
    combineTool.py -m ${1} -M GoodnessOfFit --algorithm ${algorithm} ${datacard} -t $toysPerJob --job-mode $jobMode --sub-opts="-q 8nm" --task-name $t -n toys$t --seed "$((123456*$t))"
done

echo "=== Run job on data:(`pwd`)"
combineTool.py -m ${1} -M GoodnessOfFit --algorithm ${algorithm} ${datacard} -t 0 -n Data
cd ..

echo "=== Done"