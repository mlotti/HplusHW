import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

dataVersion = "42Xmc"
#dataVersion = "42Xdata"

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion
# ALWAYS run PAT, and trigger also MC
options.doPat=1
options.triggerMC = 1

print "Assuming data is ", dataVersion
dataVersion = DataVersion(dataVersion) # convert string to object

process = cms.Process("MUONSKIM")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        #dataVersion.getPatDefaultFileCastor()
        dataVersion.getPatDefaultFileMadhatter()
    )
)

################################################################################

trigger = options.trigger
# Default trigger (for MC)
if len(trigger) == 0:
    trigger = "HLT_Mu20_v8" # Fall1; other HLT_Mu40_v6 or HLT_Mu40_eta2p1_v1

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
del process.TFileService

# Output module
process.out = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring("PFlowMuonsPath", "PFlowCHSMuonsPath")
    ),
    fileName = cms.untracked.string('skim.root'),
    outputCommands = cms.untracked.vstring()
)

process.selectionSequence = cms.Sequence()

from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
patArgs = {"doTauHLTMatching": False,
           }
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, patArgs=patArgs,
                                                            doHBHENoiseFilter=False, # Only save the HBHE result to event, don't filter
)
# In order to avoid transient references and generalTracks is available anyway
if hasattr(process, "patMuons"):
    process.patMuonsPFlow.embedTrack = False
    process.patMuonsPFlowChs.embedTrack = False

# Override the outputCommands here, since PAT modifies it
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.HChEventContent_cff")
process.out.outputCommands = cms.untracked.vstring(
    "keep *",
    "drop *_MEtoEDMConverter_*_*", # drop DQM histos
    "drop *_*_*_MUONSKIM",
)

import re
name_re = re.compile("_\*$")
process.out.outputCommands.extend([name_re.sub("_MUONSKIM", x) for x in process.HChEventContent.outputCommands])

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF as muonSelection
process.muonSelectionSequencePFlow = muonSelection.addMuonSelectionForEmbedding(process, "PFlow")
process.PFlowMuonsPath = cms.Path(
    process.commonSequence *
    process.muonSelectionSequencePFlow
)

process.muonSelectionSequencePFlowCHS = muonSelection.addMuonSelectionForEmbedding(process, "PFlowCHS")
process.PFlowCHSMuonsPath = cms.Path(
    process.commonSequence *
    process.muonSelectionSequencePFlowCHS
)

process.endPath = cms.EndPath(
    process.out
)

#process.counters = cms.EDAnalyzer("HPlusEventCountAnalyzer",
#    printMainCounter = cms.untracked.bool(True),
#    printAvailableCounters = cms.untracked.bool(True),
#)
#process.path *= process.counters
