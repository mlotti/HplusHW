#!/bin/sh

set -e

# Tag list modification history
# 21.12.2011 M.Kortelainen CMSSW_4_2_8_patch7 Introduced the file for event filters
# 19.1.2012 M.Kortelainen CMSSW_4_4_2_patch9 Added tag for GenFilters
# 17.9.2012 M.Kortelainen CMSSW_4_4_4 Added tag for electron MVA ID
# 31.1.2013 M.Kortelainen CMSSW_4_4_5 PU jet ID
# 5.2.2013 M.Kortelainen CMSSW_4_4_5 Updated PU jet ID recipe

# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#ECAL_dead_cell_filter
# https://twiki.cern.ch/twiki/bin/view/CMS/SusyEcalMaskedCellSummary
cvs co -r Colin_TaggingMode_June30 JetMETAnalysis/ecalDeadCellTools

# https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJetID
# https://hypernews.cern.ch/HyperNews/CMS/get/JetMET/1417.html
cvs co -r V00-03-01 -d CMGTools/External UserCode/CMG/CMGTools/External
rm CMGTools/External/src/PileupJetIdAlgoSubStructure.cc
rm CMGTools/External/interface/PileupJetIdAlgoSubstructure.h
cvs up -r V00-02-10 CMGTools/External/src/classes.h
cvs up -r V00-02-10 CMGTools/External/src/classes_def.xml

# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Tracking_failure_filter
cvs co -r TrackingfailTagMode_18Oct11 -d SandBox/Skims UserCode/seema/SandBox/Skims
rm SandBox/Skims/python/RA2Objects_cff.py
rm SandBox/Skims/python/RA2Cleaning_cff.py

# https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentification
#
# The tag is checked out in the analysis checkoutTags (because of
# cut-based ID), but we can do the downloading of the xmls here.
#
# Downloads ~50 MB of xml, which compresses to ~8.5 MB with 'tar zcf'
if [ ! -e EGamma/EGammaAnalysisTools ]; then
    echo "ERROR: You should run HiggsAnalysis/HeavyChHiggsToTauNu/test/checkoutTags.sh first !"
    exit 1
fi
cd EGamma/EGammaAnalysisTools/data
rm -f *.xml # In case there are old files
cat download.url | xargs wget
cd ../../..

