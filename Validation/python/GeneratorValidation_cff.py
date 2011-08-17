import FWCore.ParameterSet.Config as cms

from HiggsAnalysis.Validation.GeneratorTauValidation_cfi import *
from HiggsAnalysis.Validation.GeneratorMassValidation_cfi import *

GeneratorValidation = cms.Sequence(
	generatorTauValidation *
	generatorMassValidation
)
