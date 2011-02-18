import FWCore.ParameterSet.Config as cms

from HiggsAnalysis.Validation.GeneratorTauValidation_cfi import *

GeneratorValidation = cms.Sequence(
	generatorTauValidation
)
