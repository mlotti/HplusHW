import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion

#dataVersion = "35X"
#dataVersion = "35Xredigi"
#dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"
#dataVersion = "38X"
dataVersion = "38Xrelval"
#dataVersion = "36Xdata" # this is for collision data 
#dataVersion = "38Xdata" # this is for collision data 

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
print "GlobalTag="+dataVersion.getGlobalTag()

# Jet trigger (for cleaning of tau->HLT matching
myJetTrigger = "HLT_Jet30U"
#myJetTrigger = "HLT_Jet50U"

################################################################################
# Source
process.source = cms.Source('PoolSource',
  duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
  fileNames = cms.untracked.vstring(
#    "rfio:/castor/cern.ch/user/w/wendland/FE2DEA23-15CA-DF11-B86C-0026189438BF.root" #AOD
        dataVersion.getPatDefaultFileCastor()
        #dataVersion.getPatDefaultFileMadhatter()
  )
)

################################################################################
# Load common stuff
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
del process.TFileService

################################################################################
# In case of data, add trigger
from HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalTrigger import getSignalTrigger
myTrigger = options.trigger
# Default trigger, deduce from data
if len(myTrigger) == 0:
    myTrigger = getSignalTrigger(dataVersion)

from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection import addDataSelection
process.collisionDataSelection = cms.Sequence()
if dataVersion.isData():
    process.collisionDataSelection = addDataSelection(process, dataVersion, myTrigger)

   
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection import addDataSelection
process.collisionDataSelection = cms.Sequence()
if dataVersion.isData():
    process.collisionDataSelection = addDataSelection(process, dataVersion, myTrigger)

#myTrigger = "HLT_Jet30U" # use only for debugging

print "Trigger used for tau matching: "+myTrigger
print "Trigger used for jet matching: "+myJetTrigger


################################################################################
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
        "keep L1GlobalTriggerReadoutRecord_*_*_*",
        "keep L1GlobalTriggerObjectMapRecord_*_*_*",
        "keep *_conditionsInEdm_*_*",
        "keep edmMergeableCounter_*_*_*", # in lumi block
        "keep PileupSummaryInfo_*_*_*", # this seems to be available only in 38X MC
        "keep *_offlinePrimaryVertices_*_*"
    )
)

################################################################################
# Add PAT sequences
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import *
process.s = addPat(process, dataVersion, matchingTauTrigger=myTrigger, matchingJetTrigger=myJetTrigger)

if dataVersion.isData():
    process.out.outputCommands.extend(["drop recoGenJets_*_*_*"])
else:
    process.out.outputCommands.extend([
            "keep *_genParticles_*_*",
            "keep GenEventInfoProduct_*_*_*",
            "keep GenRunInfoProduct_*_*_*"
            ])

################################################################################
# Take our skim, run it independently of the rest of the job, don't
# use it's result for selecting the events to save. It is used to just
# to get the decision, which is saved by the framework to the event,
# and it can be accessed later in the analysis stage.
process.load("HiggsAnalysis.Skimming.heavyChHiggsToTauNu_Sequences_cff")
process.heavyChHiggsToTauNuHLTFilter.TriggerResultsTag.setProcessName(dataVersion.getTriggerProcess())
process.heavyChHiggsToTauNuSequence.remove(process.heavyChHiggsToTauNuHLTrigReport)
process.heavyChHiggsToTauNuHLTFilter.HLTPaths = [myTrigger]


# Create paths
process.path    = cms.Path(
    process.collisionDataSelection * # this is supposed to be empty for MC
    process.s 
    * process.triggerMatchingSequence
)
process.skimPath = cms.Path(
    process.heavyChHiggsToTauNuSequence
)
process.outpath = cms.EndPath(process.out)

