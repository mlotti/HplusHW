#!/bin/sh

cmsRun ../muonTagProbeAnalyzer_cfg.py trigger=isHLTMu20 > Mu20.txt 2>&1 &
cmsRun ../muonTagProbeAnalyzer_cfg.py trigger=isHLTMu24 > Mu24.txt 2>&1 &
cmsRun ../muonTagProbeAnalyzer_cfg.py trigger=isHLTMu30 > Mu30.txt 2>&1 &
cmsRun ../muonTagProbeAnalyzer_cfg.py trigger=isHLTMu40 > Mu40.txt 2>&1 &
cmsRun ../muonTagProbeAnalyzer_cfg.py trigger=isHLTMu40eta2p1 > Mu40eta2p1.txt 2>&1 &

cmsRun ../muonTagProbeAnalyzer_cfg.py mc=1 > DY.txt 2>&1 &

for job in $(jobs -p); do
    echo "Waiting for job $job"
    wait $job
done
