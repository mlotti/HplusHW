import FWCore.ParameterSet.Config as cms

eventFilter = cms.Sequence()

# Tau selection
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTauFilter_cfi import *
#tauSelectionBase.rtauCut = cms.untracked.double(0.)
eventFilter *= hPlusTauPtrSelectorFilter

# MET selection
#from HiggsAnalysis.HeavyChHiggsToTauNu.HChMETFilter_cfi import *
#eventFilter *=

