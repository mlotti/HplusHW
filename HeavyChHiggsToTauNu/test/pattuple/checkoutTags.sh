#!/bin/sh

set -e

# Tag list modification history
# 21.12.2011 M.Kortelainen CMSSW_4_2_8_patch7 Introduced the file for event filters
# 19.1.2012 M.Kortelainen CMSSW_4_4_2_patch9 Added tag for GenFilters

# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#ECAL_dead_cell_filter
# https://twiki.cern.ch/twiki/bin/view/CMS/SusyEcalMaskedCellSummary
cvs co -r Colin_TaggingMode_June30 JetMETAnalysis/ecalDeadCellTools

# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Tracking_failure_filter
cvs co -r TrackingfailTagMode_18Oct11 -d SandBox/Skims UserCode/seema/SandBox/Skims
rm SandBox/Skims/python/RA2Objects_cff.py
rm SandBox/Skims/python/RA2Cleaning_cff.py

addpkg GeneratorInterface/GenFilters CMSSW_4_2_8_patch7 # for some reason 44x has older tag than 4_2_8_patch7