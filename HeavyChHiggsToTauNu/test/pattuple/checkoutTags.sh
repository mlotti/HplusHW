#!/bin/sh

set -e

# Tag list modification history
# 21.12.2011 M.Kortelainen CMSSW_4_2_8_patch7 Introduced the file for event filters
# 19.1.2012 M.Kortelainen CMSSW_4_4_2_patch9 Added tag for GenFilters
# 17.9.2012 M.Kortelainen CMSSW_4_4_4 Added tag for electron MVA ID

# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#ECAL_dead_cell_filter
# https://twiki.cern.ch/twiki/bin/view/CMS/SusyEcalMaskedCellSummary
cvs co -r Colin_TaggingMode_June30 JetMETAnalysis/ecalDeadCellTools

# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Tracking_failure_filter
cvs co -r TrackingfailTagMode_18Oct11 -d SandBox/Skims UserCode/seema/SandBox/Skims
rm SandBox/Skims/python/RA2Objects_cff.py
rm SandBox/Skims/python/RA2Cleaning_cff.py

# https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentification
# Downloads ~50 MB of xml, which compresses to ~8.5 MB with 'tar zcf'
cvs co -r V00-00-16 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
cd EGamma/EGammaAnalysisTools/data
rm -f *.xml # In case there are old files
cat download.url | xargs wget
cd ../../..
rm EGamma/EGammaAnalysisTools/test/ElectronIsoAnalyzer.cc # Get rid of compilation error
