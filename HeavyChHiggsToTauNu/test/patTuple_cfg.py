import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion

#dataVersion = "35X"
dataVersion = "35Xredigi"
#dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"
#dataVersion = "data" # this is for collision data 

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion

print "Assuming data is ", dataVersion
dataVersion = DataVersion(dataVersion) # convert string to object

# Create Process
process = cms.Process("HChPatTuple")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

# Global tag
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

# Source
process.source = cms.Source('PoolSource',
  duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
  fileNames = cms.untracked.vstring(
        dataVersion.getPatDefaultFileCastor()
        #dataVersion.getPatDefaultFileMadhatter()
  )
)

# Load common stuff
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
del process.TFileService

# In case of data, add trigger
from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter
process.triggerSequence = cms.Sequence()
if dataVersion.isData():
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

if dataVersion.isData():
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

