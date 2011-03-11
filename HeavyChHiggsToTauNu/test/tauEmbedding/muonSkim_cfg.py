import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

#dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"
#dataVersion = "38X"
dataVersion = "39Xredigi"

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion
options.doPat=1

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
if len(trigger) == 0:
    trigger = "HLT_Mu9"

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
del process.TFileService

# Output module
process.out = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring("path")
    ),
    fileName = cms.untracked.string('skim.root'),
    outputCommands = cms.untracked.vstring()
)

process.selectionSequence = cms.Sequence()

from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
patArgs = {"doTauHLTMatching": False,
           "doPatTaus": False
           }
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, patArgs=patArgs)
# In order to avoid transient references and generalTracks is available anyway
if hasattr(process, "patMuons"):
    process.patMuons.embedTrack = False

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

#process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelection_cff")
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF_cff")
process.muonTrigger.hltResults.setProcessName(dataVersion.getTriggerProcess())
process.muonTrigger.triggerConditions = cms.vstring(trigger)

process.path = cms.Path(
    process.commonSequence *
    process.muonSelectionSequence
)
process.endPath = cms.EndPath(
    process.out
)

#process.counters = cms.EDAnalyzer("HPlusEventCountAnalyzer",
#    printMainCounter = cms.untracked.bool(True),
#    printAvailableCounters = cms.untracked.bool(True),
#)
#process.path *= process.counters
