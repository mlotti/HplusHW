#!/bin/sh

set -e

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
# 12.11.2010/M.Kortelainen CMSSW_3_8_6 Removed the tau embedding tag (added workaround)
# 9.12.2010/M.Kortelainen CMSSW_3_8_7 Updated PAT tags to latest recipe, updated lumi tag
# 27.12.2010/M.Kortelainen CMSSW_3_9_7 Updated tags to latest recipes
# 12.1.2011/M.Kortelainen CMSSW_3_9_7 Added HPS+TaNC tags
# 18.1.2011/M.Kortelainen CMSSW_3_9_7 Update PFRecoTauDiscriminationByInvMass.cc
# 19.1.2011/M.Kortelainen CMSSW_3_9_7 Updated the tau tags
# 16.2.2011/M.Kortelainen CMSSW_3_9_7 Mechanism to not to take HPS+TaNC tags
# 17.2.2011/M.Kortelainen CMSSW_3_9_7 Updated lumi tag 
# 24.2.2011/M.Kortelainen CMSSW_3_11_1_patch2 Taking into account what is included in the release
# 17.3.2011/M.Kortelainen CMSSW_3_9_7 Suffering from HiggsAnalysis/Skimming being checked out without a tag...
# 18.3.2011/M.Kortelainen CMSSW_3_9_9_patch1 Updated PAT tags for trigger
# 21.3.2011/M.Kortelainen CMSSW_4_1_3 Still suffering from HiggsAnalysis/Skimming...
# 21.3.2011/M.Kortelainen CMSSW_3_9_9_patch1 Updated pfTools.py
# 23.3.2011/M.Kortelainen CMSSW_4_1_3 Updated PAT tags for the latest recipe for 41X, removed HPS+TaNC tags as it is in AOD
# 23.3.2011/M.Kortelainen CMSSW_4_1_3 Updated PAT tags
# 24.3.2011/M.Kortelainen CMSSW_4_1_3_patch2 Updated PAT tags
# 1.4.2011/M.Kortelainen CMSSW_4_1_3_patch3 Updated tau and PAT tags to the latest recipe for 41X
# 4.4.2011/M.Kortelainen CMSSW_4_1_4 Updated tags for the new release, 
# 27.4.2011/M.Kortelainen CMSSW_4_1_4 Updated tau tags for the latest recipe for 41X
# 28.4.2011/M.Kortelainen CMSSW_4_1_5 Updated PAT tags for the latest recipe from Michal Bluj
# 3.5.2011/M.Kortelainen CMSSW_4_1_5 Minor tau tag update thanks to Mike Bachtis
# 4.5.2011/M.Kortelainen CMSSW_4_1_5 Checkout JEC sqlite file
# 4.5.2011/M.Kortelainen CMSSW_4_1_5 Updated tau tags

# addpkg requires cmsenv
eval $(scram runtime -sh)

# PAT
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePATReleaseNotes41X

# Tau+PAT
# https://hypernews.cern.ch/HyperNews/CMS/get/tauid/83/1/1/1/1.html
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePFTauID#Recommended_tags_for_2011_data_t
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideTauAnalysis#CMSSW_4_1_X_NOTE_Experimental_ve
#
# Tau
cvs co -r V01-00-07-01   DataFormats/TauReco
cvs co -r V01-00-27      RecoTauTag/Configuration
cvs co -r V01-00-33-04   RecoTauTag/RecoTau
cvs co -r V01-00-12      RecoTauTag/TauTagTools
# PAT
# PAT taked form 42X (V08-06-21 [part of CMSSW_4_2_1]), 
# PF2PAT from the 4_1_5 release
cvs co -r V06-04-08      DataFormats/PatCandidates
cvs co -r V04-07-02      PhysicsTools/PFCandProducer
cvs co -r V08-06-21      PhysicsTools/PatAlgos
# patches
patch -p0 < HiggsAnalysis/HeavyChHiggsToTauNu/test/PhysicsTools_PatAlgos_V08-06-21.patch
patch -p0 < HiggsAnalysis/HeavyChHiggsToTauNu/test/PhysicsTools_PFCandProducer_V04-07-02.patch

# Electron ID
# https://twiki.cern.ch/twiki/bin/view/CMS/SimpleCutBasedEleID
cvs co -r V00-03-01 ElectroWeakAnalysis/WENu

# Higgs skimms
cvs co HiggsAnalysis/Skimming
rm HiggsAnalysis/Skimming/python/earlyDataInterestingEvents_cff.py

# JEC
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#JetEnCor2010
cvs co -d HiggsAnalysis/HeavyChHiggsToTauNu/data UserCode/KKousour/data/Jec10V3.db