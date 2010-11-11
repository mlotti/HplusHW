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
# 11.11.2010/M.Kortelainen CMSSW_3_8_6 Moved the tau embedding tag here since it is needed for compilation


#TARGET="analysis"
#if [ "x$#" = "x1" ]; then
#    TARGET=$1
#fi
#echo "Checking out tags for $TARGET"

# Common
cvs co -r V06-01-04 DataFormats/PatCandidates
cvs co -r V08-00-29 PhysicsTools/PatAlgos
cvs up -r V08-00-27 PhysicsTools/PatAlgos/python/tools/coreTools.py
cvs up -r 1.30      PhysicsTools/PatAlgos/python/tools/tauTools.py
cvs co -r V00-02-24 PhysicsTools/SelectorUtils 
cvs co -r lumi2010-Oct12 RecoLuminosity/LumiDB
cvs co -r V01-04-00 FWCore/PythonUtilities

# PATTuple
#if [ "x$TARGET" = "xpattuple" ]; then
cvs co -r V00-03-13 RecoEgamma/ElectronIdentification
cvs co -r V00-02-01 ElectroWeakAnalysis/WENu
cvs co -r V00-24-00 RecoTauTag/Configuration
cvs co -r V00-24-00 RecoTauTag/RecoTau
cvs co -r 1.1 RecoTauTag/RecoTau/plugins/CaloRecoTauDiscriminationByCharge.cc
cvs co -r 1.2 RecoTauTag/RecoTau/plugins/CaloRecoTauDiscriminationByDeltaE.cc
cvs co -r 1.1 RecoTauTag/RecoTau/plugins/CaloRecoTauDiscriminationByFlightPathSignificance.cc
cvs co -r 1.1 RecoTauTag/RecoTau/plugins/CaloRecoTauDiscriminationByInvMass.cc
cvs co -r 1.1 RecoTauTag/RecoTau/plugins/CaloRecoTauDiscriminationByNProngs.cc
cvs co -r 1.1 RecoTauTag/RecoTau/plugins/CaloRecoTauDiscriminationByTauPolarization.cc
cvs co -r 1.3 RecoTauTag/RecoTau/plugins/CaloRecoTauDiscriminationByIsolation.cc
cvs co -r 1.1 RecoTauTag/RecoTau/plugins/PFRecoTauDiscriminationByDeltaE.cc
cvs co -r 1.1 RecoTauTag/RecoTau/plugins/PFRecoTauDiscriminationByFlightPathSignificance.cc
cvs co -r 1.1 RecoTauTag/RecoTau/plugins/PFRecoTauDiscriminationByInvMass.cc
cvs co -r 1.1 RecoTauTag/RecoTau/plugins/PFRecoTauDiscriminationByNProngs.cc
cvs co -r 1.1 RecoTauTag/RecoTau/plugins/PFRecoTauDiscriminationByTauPolarization.cc
cvs co -r 1.1 RecoTauTag/RecoTau/python/CaloRecoTauDiscriminationByCharge_cfi.py
cvs co -r 1.1 RecoTauTag/RecoTau/python/CaloRecoTauDiscriminationByDeltaE_cfi.py
cvs co -r 1.1 RecoTauTag/RecoTau/python/CaloRecoTauDiscriminationByFlightPathSignificance_cfi.py
cvs co -r 1.1 RecoTauTag/RecoTau/python/CaloRecoTauDiscriminationByInvMass_cfi.py
cvs co -r 1.1 RecoTauTag/RecoTau/python/CaloRecoTauDiscriminationByNProngs_cfi.py
cvs co -r 1.1 RecoTauTag/RecoTau/python/CaloRecoTauDiscriminationByTauPolarization_cfi.py
cvs co -r 1.1 RecoTauTag/RecoTau/python/PFRecoTauDiscriminationByDeltaE_cfi.py
cvs co -r 1.1 RecoTauTag/RecoTau/python/PFRecoTauDiscriminationByFlightPathSignificance_cfi.py
cvs co -r 1.1 RecoTauTag/RecoTau/python/PFRecoTauDiscriminationByInvMass_cfi.py
cvs co -r 1.1 RecoTauTag/RecoTau/python/PFRecoTauDiscriminationByNProngs_cfi.py
cvs co -r 1.1 RecoTauTag/RecoTau/python/PFRecoTauDiscriminationByTauPolarization_cfi.py
cvs co -r 1.1 RecoTauTag/RecoTau/python/CaloRecoTauDiscriminationForChargedHiggs_cfi.py
cvs co -r 1.2 RecoTauTag/RecoTau/python/PFRecoTauDiscriminationForChargedHiggs_cfi.py
cvs co -r 1.3 RecoTauTag/RecoTau/python/PFRecoTauDiscriminationByIsolationChargedPtSum_cfi.py
cvs up -r 1.2 RecoTauTag/RecoTau/plugins/BuildFile.xml
cvs co -r V00-00-07 TauAnalysis/MCEmbeddingTools
cvs co HiggsAnalysis/Skimming
rm HiggsAnalysis/Skimming/python/earlyDataInterestingEvents_cff.py
#fi

# Tau embedding
cvs co -r V00-00-07 TauAnalysis/MCEmbeddingTools
