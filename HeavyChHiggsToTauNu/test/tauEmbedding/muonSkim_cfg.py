import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"
#dataVersion = "38X"
#dataVersion = "data" # this is for collision data 

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion
options.doPat=1

print "Assuming data is ", dataVersion
dataVersion = DataVersion(dataVersion) # convert string to object

process = cms.Process("MUONSKIM")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    #duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
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

from PhysicsTools.PatAlgos.tools.coreTools import removeSpecificPATObjects, removeCleaning
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPat
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection import addDataSelection

if options.doPat != 0:
    process.collisionDataSelection = cms.Sequence()
    if dataVersion.isData():
        process.collisionDataSelection = addDataSelection(process, dataVersion, trigger)
    
    process.patSequence = addPat(process, dataVersion, doPatTrigger=False, doTauHLTMatching=False,
                                 doPatTaus=False, doPatElectronID=False)
    removeSpecificPATObjects(process, ["Photons"], False)
    removeCleaning(process, False)    
    process.patMuons.embedTrack = False # In order to avoid transient references and generalTracks is available anyway

    process.selectionSequence = cms.Sequence(
        process.collisionDataSelection * 
        process.patSequence
    )

# Override the outputCommands here, since PAT modifies it
process.out.outputCommands = cms.untracked.vstring(
    "keep *",
    "drop *_MEtoEDMConverter_*_*", # drop DQM histos
    "drop *_*_*_MUONSKIM",
    "keep *_selectedPatMuons_*_MUONSKIM",
    "keep *_tauEmbeddingMuons_*_MUONSKIM",
    "keep edmMergeableCounter_*_*_MUONSKIM", # in lumi block
)

#process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelection_cff")
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF_cff")
process.selectionSequence *= process.muonSelectionSequence
process.muonTrigger.hltResults.setProcessName(dataVersion.getTriggerProcess())
process.muonTrigger.triggerConditions = cms.vstring(trigger)

process.path = cms.Path(
    process.selectionSequence
)
process.endPath = cms.EndPath(
    process.out
)

#process.counters = cms.EDAnalyzer("HPlusEventCountAnalyzer",
#    printMainCounter = cms.untracked.bool(True),
#    printAvailableCounters = cms.untracked.bool(True),
#)
#process.path *= process.counters
