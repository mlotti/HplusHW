#!/bin/sh

set -e

# Tag list modification history
# 21.12.2011 M.Kortelainen CMSSW_4_2_8_patch7 Introduced the file for event filters

# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#ECAL_dead_cell_filter
# https://twiki.cern.ch/twiki/bin/view/CMS/SusyEcalMaskedCellSummary
cvs co -r Colin_TaggingMode_June30 JetMETAnalysis/ecalDeadCellTools

# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#Tracking_failure_filter
cvs co -r TrackingfailTagMode_18Oct11 -d SandBox/Skims UserCode/seema/SandBox/Skims
rm SandBox/Skims/RA2Objects_cff.py
rm SandBox/Skims/RA2Cleaning_cff.py