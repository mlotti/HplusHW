import FWCore.ParameterSet.Config as cms

process = cms.Process("Validation")

dataTier = "PATTuple"
#dataTier = "AOD"

#dataVersion = "39Xredigi"
#dataVersion = "311Xredigi"
#dataVersion = "39Xdata"
#dataVersion = "38XredigiPU"
dataVersion = "42Xmc"

#trigger = "HLT_SingleIsoTau20_Trk15_MET25_v4"
trigger = "HLT_IsoPFTau35_Trk20_MET45"

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
#        'rfio:/castor/cern.ch/user/s/slehti/HiggsAnalysisData/test_H120_100_1_08t_RAW_RECO.root'
#	'file:/tmp/slehti/test_H120_100_1_08t_RAW_RECO.root'
#	dataVersion.getAnalysisDefaultFileCastor()
#	dataVersion.getPatDefaultFileCastor()
	'file:/tmp/slehti/TTJets_TuneZ2_Summer11_pattuple_266_1_at8.root'
    )
)

#trigger = "HLT_IsoPFTau35_Trk20_MET45_v1"
#process.source.fileNames = ["/store/data/Run2011A/Tau/AOD/PromptReco-v1/000/161/078/D8D00F2A-0856-E011-8826-0019DB29C614.root"]
#process.source.fileNames = ["/store/data/Run2011A/Tau/AOD/PromptReco-v1/000/160/406/A4437138-604F-E011-B629-0030487CD77E.root"]
#process.source.fileNames = [
#    "/store/data/Run2011A/Tau/AOD/PromptReco-v1/000/160/499/9CBF366F-9450-E011-AE5E-0030487CD162.root",
#    "/store/data/Run2011A/Tau/AOD/PromptReco-v1/000/160/577/6CB966ED-8951-E011-814F-0030487A1990.root"
#    ]

#trigger = "HLT_QuadJet40_IsoPFTau40_v1"
#process.source.fileNames = ["/store/data/Run2011A/TauPlusX/AOD/PromptReco-v1/000/161/217/9808B164-F756-E011-976A-001D09F25393.root"]

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

process.load("HiggsAnalysis.Validation.PFTauChHadronCandidateValidation_cfi")
process.load("HiggsAnalysis.Validation.PrimaryVertexValidation_cfi")
process.load("HiggsAnalysis.Validation.TauTriggerEfficiencyValidation_cfi")

#if "HLT_SingleIsoTau20_Trk15_MET25" in trigger:
#    pass
#elif "HLT_IsoPFTau35_Trk20_MET45" in trigger:
#    process.L2TauMET.triggerBit = trigger
#    process.L2TauMET.hltPathFilter.setModuleLabel("hltFilterL2EtCutSingleIsoPFTau35Trk20MET45")
#
#    process.L3TauMET.triggerBit = trigger
#    process.L3TauMET.hltPathFilter.setModuleLabel("hltFilterSingleIsoPFTau35Trk20LeadTrackPt20")
#    process.L3TauMETnoHLTFilter.hltPathFilter.setModuleLabel("hltFilterSingleIsoPFTau35Trk20LeadTrackPt20")
#
#    process.L3TauMETIsolation = process.L3TauMET.clone()
#    process.L3TauMETIsolation.hltPathFilter.setModuleLabel("hltFilterSingleIsoPFTau35Trk20MET45LeadTrack20MET45IsolationL1HLTMatched")
#    process.L3TauMETIsolationnoHLTFilter = process.L3TauMETIsolation.clone()
#    process.L3TauMETIsolationnoHLTFilter.triggerBit = ""
#    process.TriggerValidation *= (process.L3TauMETIsolation * process.L3TauMETIsolationnoHLTFilter)
#
#    process.TauTriggerEfficiencyValidation.triggerBit = trigger
#    process.TauTriggerEfficiencyValidation.hltPathFilter = cms.InputTag("hltFilterSingleIsoPFTau35Trk20MET45LeadTrack20MET45IsolationL1HLTMatched", "", dataVersion.getTriggerProcess())
#    
#
#elif "HLT_QuadJet40_IsoPFTau40" in trigger:
#    process.L3TauMET.triggerBit = trigger
#    process.L3TauMET.hltPathFilter.setModuleLabel("hltQuadJet40IsoPFTau40")
#    process.L3TauMETnoHLTFilter.hltPathFilter.setModuleLabel("hltQuadJet40IsoPFTau40")
#
#    process.TriggerValidation.remove(process.L2TauMET)
#
#    process.TauTriggerEfficiencyValidation.triggerBit = trigger
#    process.TauTriggerEfficiencyValidation.hltPathFilter = cms.InputTag("hltQuadJet40IsoPFTau40", "", dataVersion.getTriggerProcess())
#
#else:
#    raise Exception("Unsupported trigger bit %s" % trigger)


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
####        process.TauMomentumValidation+
        process.GeneratorValidation+
#### FIXME        process.TriggerValidation+
        process.endOfProcess
    )

if dataTier == "AOD":
    process.p = cms.Path(
	process.PFTauValidation+
        process.PrimaryVertexValidation+
        process.GeneratorValidation+
        process.TriggerValidation+
	process.TauTriggerEfficiencyValidation+
        process.endOfProcess
    )
