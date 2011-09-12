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

# Lepton vetoes
from HiggsAnalysis.HeavyChHiggsToTauNu.HChGlobalElectronVetoFilter_cfi import *
eVetoFilter = hPlusGlobalElectronVetoFilter.clone()
eventFilter *= eVetoFilter
from HiggsAnalysis.HeavyChHiggsToTauNu.HChGlobalMuonVetoFilter_cfi import *
muVetoFilter = hPlusGlobalMuonVetoFilter.clone()
eventFilter *= muVetoFilter

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
