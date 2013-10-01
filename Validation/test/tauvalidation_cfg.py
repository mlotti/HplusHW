import FWCore.ParameterSet.Config as cms

process = cms.Process("Validation")

#dataTier = "PATTuple"
dataTier = "AOD"

dataVersion = "53XmcS10"

# Command line arguments (options) and DataVersion object
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion
options, dataVersion = getOptionsDataVersion(dataVersion)
print dataVersion.getTriggerProcess()

if len(options.trigger) > 0:
    trigger = options.trigger

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#	dataVersion.getAnalysisDefaultFileMadhatter()
#	dataVersion.getAnalysisDefaultFileCastor()
#	dataVersion.getPatDefaultFileCastor()
#	"file:/tmp/slehti/TTJets_Summer12_pattuple_569_1_JMF.root"
	'/store/mc/Summer12_DR53X/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/AODSIM/PU_S10_START53_V7A-v1/0002/BE96A186-2AD4-E111-B6C6-003048673FEA.root'
    )
)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000

process.load("HiggsAnalysis.Validation.GeneratorTauValidation_cfi")
process.load('Configuration/StandardSequences/EndOfProcess_cff')

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

process.p = cms.Path(
    process.generatorTauValidation+
    process.endOfProcess
)
