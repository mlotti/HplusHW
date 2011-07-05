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

# Jet selection
from HiggsAnalysis.HeavyChHiggsToTauNu.HChJetFilter_cfi import *
jetSelectionFilter = hPlusJetPtrSelectorFilter.clone()
eventFilter *= jetSelectionFilter

# BTagging
from HiggsAnalysis.HeavyChHiggsToTauNu.HChBTaggingFilter_cfi import *
btagSelectionFilter = hPlusBTaggingPtrSelectorFilter.clone(
    jetSrc = "jetSelectionFilter"
)
eventFilter *= btagSelectionFilter
