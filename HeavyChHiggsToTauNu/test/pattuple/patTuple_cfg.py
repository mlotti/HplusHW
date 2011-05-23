import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

dataVersion="42Xdata"

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)

# Create Process
process = cms.Process("HChPatTuple")
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(5) )

# Global tag
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())
print "GlobalTag="+dataVersion.getGlobalTag()

################################################################################
# Source
process.source = cms.Source('PoolSource',
  fileNames = cms.untracked.vstring(
#    "rfio:/castor/cern.ch/user/w/wendland/FE2DEA23-15CA-DF11-B86C-0026189438BF.root" #AOD
#	"rfio:/castor/cern.ch/user/s/slehti/testData/TTToHplusBWB_M-90_7TeV-pythia6-tauola_Fall10-START38_V12-v1_RAW_RECO.root"
#	"rfio:/castor/cern.ch/user/s/slehti/testData/test_H120_100_1_08t_RAW_RECO.root"
#        dataVersion.getPatDefaultFileCastor()
        dataVersion.getPatDefaultFileMadhatter()
  )
)

################################################################################
# Load common stuff
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
del process.TFileService

################################################################################
# In case of data, add trigger
myTrigger = options.trigger
if len(myTrigger) == 0:
    myTrigger = dataVersion.getDefaultSignalTrigger()

from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection import addDataSelection
process.collisionDataSelection = cms.Sequence()
if dataVersion.isData():
    process.collisionDataSelection = addDataSelection(process, dataVersion, myTrigger)

#myTrigger = "HLT_Jet30U" # use only for debugging

print "Trigger used for tau matching: "+myTrigger

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
        "keep L1GlobalTriggerReadoutRecord_*_*_*",   # needed for prescale provider
        "keep L1GlobalTriggerObjectMapRecord_*_*_*", # needed for prescale provider
        "keep *_conditionsInEdm_*_*",
        "keep edmMergeableCounter_*_*_*", # in lumi block
        "keep PileupSummaryInfos_*_*_*", # only in MC
        "keep *_offlinePrimaryVertices_*_*",
        "keep *_l1GtTriggerMenuLite_*_*", # in run block, needed for prescale provider
    ),
    dropMetaData = cms.untracked.string("ALL")
)

################################################################################
# Add PAT sequences
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import *

# Add first PF2PAT so that we get a clean patDefaultSequence
process.sPF2PAT = addPF2PAT(process, dataVersion,
                            matchingTauTrigger=myTrigger,
                            postfix="PFlow", doPFnoPU=False,
                            )
process.sPF2PATnoPU = addPF2PAT(process, dataVersion,
                                matchingTauTrigger=myTrigger,
                                )

process.sPAT = addPlainPat(process, dataVersion,
                           doPatMuonPFIsolation=True,
                           matchingTauTrigger=myTrigger,
                           includeTracksPFCands=False,
                           )

if dataVersion.isData():
    process.out.outputCommands.extend(["drop recoGenJets_*_*_*"])
else:
    process.out.outputCommands.extend([
            "keep *_genParticles_*_*",
            "keep GenEventInfoProduct_*_*_*",
            "keep GenRunInfoProduct_*_*_*",
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

#process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HLTTauEmulation_cff")
#process.out.outputCommands.extend(["keep recoCaloTaus_caloTauHLTTauEmu_*_*"])
#process.out.outputCommands.extend(["keep *_l1extraParticles_*_*"])
#process.out.outputCommands.extend(["keep recoTracks_generalTracks_*_*"])
#process.out.outputCommands.extend(["keep recoCaloJets_ak5CaloJets_*_*"])

# Create paths
process.path    = cms.Path(
    process.collisionDataSelection * # this is supposed to be empty for MC
#    process.HLTTauEmu * # Hopefully not needed anymore in 39X as the tau trigger should be fixed
    process.sPAT *
    process.sPF2PAT *
    process.sPF2PATnoPU
)
process.skimPath = cms.Path(
    process.heavyChHiggsToTauNuSequence
)
process.outpath = cms.EndPath(process.out)

