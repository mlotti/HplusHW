import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions

#dataVersion = "35X"
#dataVersion = "35Xredigi"
#dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"
dataVersion = "data" # this is for collision data 

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion

print "Assuming data is ", dataVersion

# Create Process
process = cms.Process("HChPatTuple")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

# Global tag
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
if dataVersion == "data":
    process.GlobalTag.globaltag = cms.string("GR_R_38X_V13::All")
else:
    process.GlobalTag.globaltag = cms.string("START38_V9::All")

# Source
process.source = cms.Source('PoolSource',
  duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
  fileNames = cms.untracked.vstring(
    "/store/mc/Summer10/WJets_7TeV-madgraph-tauola/AODSIM/START36_V9_S09-v1/0046/FEFEE1D1-F17B-DF11-B911-00304867C16A.root"
  )
)
if dataVersion == "data":
    process.source.fileNames = cms.untracked.vstring(
        "/store/data/Run2010A/JetMETTau/RECO/Jul16thReReco-v1/0049/FE36C9D8-3891-DF11-829E-00261894395F.root"
    ) 

# Load common stuff
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
del process.TFileService

# In case of data, add trigger
from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter
process.triggerSequence = cms.Sequence()
if dataVersion == "data":
    process.TriggerFilter = triggerResultsFilter.clone()
    process.TriggerFilter.hltResults = cms.InputTag("TriggerResults", "", "HLT")
    process.TriggerFilter.l1tResults = cms.InputTag("")
    #process.TriggerFilter.throw = cms.bool(False) # Should it throw an exception if the trigger product is not found
    process.TriggerFilter.triggerConditions = cms.vstring("HLT_SingleLooseIsoTau20")
    process.allEvents = cms.EDProducer("EventCountProducer")
    process.passedTrigger = cms.EDProducer("EventCountProducer")
    process.triggerSequence *= process.allEvents
    process.triggerSequence *= process.TriggerFilter
    process.triggerSequence *= process.passedTrigger

# Output module
process.out = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring("path")
    ),
    fileName = cms.untracked.string('pattuple.root'),
    outputCommands = cms.untracked.vstring(
        "drop *",
        "keep edmTriggerResults_*_*_*",
        "keep triggerTriggerEvent_*_*_*",
        "keep edmMergeableCounter_*_*_*"
    )
)

# Add PAT sequences
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import *
process.s = addPat(process, dataVersion)

if dataVersion == "data":
    process.out.outputCommands.extend(["drop recoGenJets_*_*_*"])
else:
    process.out.outputCommands.extend([
            "keep *_genParticles_*_*",
            "keep GenEventInfoProduct_*_*_*",
            "keep GenRunInfoProduct_*_*_*"
            ])

# Create paths
process.path    = cms.Path(
    process.triggerSequence * # this is supposed to be empty for MC
    process.s 
)
process.outpath = cms.EndPath(process.out)

