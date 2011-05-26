import FWCore.ParameterSet.Config as cms

eventFilter = cms.Sequence()

# Tau selection
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTauFilter_cfi import *
tauSelectionFilter = hPlusTauPtrSelectorFilter.clone()
tauSelectionFilter.tauSelection.rtauCut = cms.untracked.double(0.)
eventFilter *= tauSelectionFilter

# MET selection
from HiggsAnalysis.HeavyChHiggsToTauNu.HChMETFilter_cfi import *
metSelectionFilter = hPlusMETPtrSelectorFilter.clone()
eventFilter *= metSelectionFilter

