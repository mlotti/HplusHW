import FWCore.ParameterSet.Config as cms

process = cms.Process("Validation")

#dataTier = "PATTuple"
dataTier = "AOD"

#dataVersion = "39Xredigi"
dataVersion = "311Xredigi"
#dataVersion = "39Xdata"
#dataVersion = "38XredigiPU"

# Command line arguments (options) and DataVersion object
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion
options, dataVersion = getOptionsDataVersion(dataVersion)
print dataVersion.getTriggerProcess()

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#        'rfio:/castor/cern.ch/user/s/slehti/HiggsAnalysisData/test_H120_100_1_08t_RAW_RECO.root'
#	'file:/tmp/slehti/test_H120_100_1_08t_RAW_RECO.root'
#	dataVersion.getAnalysisDefaultFileCastor()
	dataVersion.getPatDefaultFileCastor()
    )
)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000

process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load("HiggsAnalysis.Validation.TauMomentumValidation_cff")
process.load("HiggsAnalysis.Validation.GeneratorValidation_cff")
process.load("HiggsAnalysis.Validation.TriggerValidation_cff")
process.L2TauMET.triggerResults.setProcessName(dataVersion.getTriggerProcess())
process.L2TauMET.hltPathFilter.setProcessName(dataVersion.getTriggerProcess())
process.L3TauMET.triggerResults.setProcessName(dataVersion.getTriggerProcess())
process.L3TauMET.hltPathFilter.setProcessName(dataVersion.getTriggerProcess())
process.L3TauMETnoHLTFilter.triggerResults.setProcessName(dataVersion.getTriggerProcess())
process.L3TauMETnoHLTFilter.hltPathFilter.setProcessName(dataVersion.getTriggerProcess())
#process.TriggerTauValidation.triggerResults = cms.InputTag("TriggerResults","",dataVersion.getTriggerProcess())
#process.TriggerTauValidation.hltPathFilter  = cms.InputTag("hltFilterL3TrackIsolationSingleIsoTau35Trk15MET25","",dataVersion.getTriggerProcess())

ANALYSISEventContent = cms.PSet(
    outputCommands = cms.untracked.vstring('keep *_*_*_Validation')
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('output.root'),
    outputCommands = ANALYSISEventContent.outputCommands
)

process.endPath = cms.EndPath(
    process.out
)

if dataTier == "PATTuple":
    process.p = cms.Path(
        process.TauMomentumValidation+
        process.GeneratorValidation+
        process.TriggerValidation+
        process.endOfProcess
    )

process.load("HiggsAnalysis.Validation.PFTauChHadronCandidateValidation_cfi")
process.load("HiggsAnalysis.Validation.PrimaryVertexValidation_cfi")
process.load("HiggsAnalysis.Validation.TauTriggerEfficiencyValidation_cfi")

if dataTier == "AOD":
    process.p = cms.Path(
	process.PFTauValidation+
        process.PrimaryVertexValidation+
        process.GeneratorValidation+
        process.TriggerValidation+
	process.TauTriggerEfficiencyValidation+
        process.endOfProcess
    )
