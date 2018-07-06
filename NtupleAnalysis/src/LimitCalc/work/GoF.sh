#!/bin/bash

nToys=1000
nJobs=50
queue="8nh"


echo "Run GoF for $nToys toys over $nJobs for card $1"

toysPerJob=$((nToys/nJobs))
echo $toysPerJob




for (( t=1; t<=$nJobs; t++ ))
do  

   combineTool.py -M GoodnessOfFit --algorithm saturated $1 -t $toysPerJob --job-mode lxbatch --sub-opts="-q 8nh" --task-name $t -n toys$t --seed "$((123456*$t))"

done



echo "Run goF on data"

combineTool.py -M GoodnessOfFit --algorithm saturated $1 -t 0  -n Data
