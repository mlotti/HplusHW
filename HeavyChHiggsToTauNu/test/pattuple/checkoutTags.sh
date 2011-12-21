#!/bin/sh

set -e

# Tag list modification history
# 21.12.2011 M.Kortelainen CMSSW_4_2_8_patch7 Introduced the file for event filters

# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFilters#ECAL_dead_cell_filter
# https://twiki.cern.ch/twiki/bin/view/CMS/SusyEcalMaskedCellSummary
cvs co -r Colin_TaggingMode_June30 JetMETAnalysis/ecalDeadCellTools

