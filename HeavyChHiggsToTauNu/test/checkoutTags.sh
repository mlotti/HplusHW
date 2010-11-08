#!/bin/sh

# Tag list modification history
# 7.7.2010/S.Lehti CMSSW_3_6_3
# 9.8.2010/M.Kortelainen CMSSW_3_7_0_patch_3
# 21.9.2010/S.Lehti CMSSW_3_8_4
# 27.9.2010/M.Kortelainen CMSSW_3_8_4_patch2
# 29.9.2010/S.Lehti CMSSW_3_8_4_patch2 (discriminators moved under RecoTau)
# 15.10.2010/S.Lehti CMSSW_3_8_5 (discriminators moved under RecoTau)
# 19.10.2010/M.Kortelainen CMSSW_3_8_5 (lumi tag update)
# 21.10.2010/M.Kortelainen CMSSW_3_8_5_patch2 (Updated PatAlgos tag, added revision numbers for files)
# 28.10.2010/M.Kortelainen CMSSW_3_8_5_patch3 (Electron ID and additional PAT tags from the release notes)
# 2.11.2010/M.Kortelainen CMSSW_3_8_5_patch3 (tag for filterJSON.py etc. scripts) 
# 8.11.2010/S.Lehti CMSSW_3_8_6 (New tau software and HPS + Tanc)


#TARGET="analysis"
#if [ "x$#" = "x1" ]; then
#    TARGET=$1
#fi
#echo "Checking out tags for $TARGET"

# Common
cvs co -r V06-01-04 DataFormats/PatCandidates
cvs co -r V08-01-09 PhysicsTools/PatAlgos
#cvs up -r V08-00-27 PhysicsTools/PatAlgos/python/tools/coreTools.py
#cvs up -r 1.30      PhysicsTools/PatAlgos/python/tools/tauTools.py
cvs co -r V00-02-24 PhysicsTools/SelectorUtils 
cvs co -r lumi2010-Oct12 RecoLuminosity/LumiDB
cvs co -r V01-04-00 FWCore/PythonUtilities

# PATTuple
#if [ "x$TARGET" = "xpattuple" ]; then
cvs co -r V00-03-13 RecoEgamma/ElectronIdentification
cvs co -r V00-02-01 ElectroWeakAnalysis/WENu
cvs co -r V01-00-00 DataFormats/TauReco
cvs co -r V01-00-01 RecoTauTag/Configuration
cvs co -r V01-00-05 RecoTauTag/RecoTau
cvs co -r V01-00-00 RecoTauTag/TauTagTools
cvs co HiggsAnalysis/Skimming
rm HiggsAnalysis/Skimming/python/earlyDataInterestingEvents_cff.py
addpkg -f ~friis/public/tau_tags.txt
#fi
