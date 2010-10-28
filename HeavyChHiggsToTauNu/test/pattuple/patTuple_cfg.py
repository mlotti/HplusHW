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
        #dataVersion.getPatDefaultFileCastor()
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
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection import addDataSelection
process.collisionDataSelection = cms.Sequence()
if dataVersion.isData():
    if dataVersion.isRun2010A():
        myTrigger = "HLT_SingleLooseIsoTau20" #HLT_SingleIsoTau20_Trk5"
    elif dataVersion.isRun2010B():
        myTrigger = "HLT_SingleIsoTau20_Trk15_MET20"
    else:
        raise Exception("Unsupported data version!")
    process.collisionDataSelection = addDataSelection(process, dataVersion, myTrigger)
else:
    if dataVersion.is38X():
        myTrigger = "HLT_SingleIsoTau20_Trk15_MET20"
    else:
        myTrigger = "HLT_SingleLooseIsoTau20" #HLT_SingleIsoTau20_Trk5"

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
        "keep *_offlinePrimaryVertices_*_*",
        "keep recoTracks_generalTracks_*_*"
    )
)

################################################################################
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

################################################################################
# Do tau -> HLT tau trigger matching and tau -> HLT jet trigger matching
# Produces:
#   1) a patTauCollection of patTaus matched to the HLT tau trigger and
#   2) a copy of the same collection with the patTau matching to the HLT jet trigger
#      removed (needed to remove trigger bias in QCD backround measurement).
# Yes, I agree that this sounds (and is) a bit compicated :)
patTauCollectionList = [
    "selectedPatTausShrinkingConePFTau",
    "selectedPatTausHpsPFTau",
    "selectedPatTausCaloRecoTau"
    ] # add to the list new sources for patTauCollections, if necessary

patTauTriggerMatchHplusProtoType = cms.EDProducer("PATTriggerMatcherDRLessByR",
    src                   = cms.InputTag("dummy"),
    matched               = cms.InputTag("patTrigger"),
    andOr                 = cms.bool(False),
    filterIdsEnum         = cms.vstring('*'),
    filterIds             = cms.vint32(0),
    filterLabels          = cms.vstring('*'),
    pathNames             = cms.vstring(myTrigger),
    collectionTags        = cms.vstring('*'),
    maxDeltaR             = cms.double(0.4), # start with 0.4; patTrigger pages propose 0.1 or 0.2
    resolveAmbiguities    = cms.bool(True),
    resolveByMatchQuality = cms.bool(False)
)

patTauEmptyCleanerProtoType = cms.EDFilter("PATTauSelector",
    src = cms.InputTag("dummy"),
    cut = cms.string("!triggerObjectMatchesByPath('"+myTrigger+"').empty()"),
)

process.triggerMatchingSequence = cms.Sequence()

for patTauCollection in patTauCollectionList:
    ###########################################################################
    # Tau -> HLT tau trigger matching
    print "Matching patTauCollection "+patTauCollection+" to tau trigger "+myTrigger
    # create DeltaR matcher of trigger objects to a tau collection
    patTauTriggerMatcher = patTauTriggerMatchHplusProtoType.clone(
        src = cms.InputTag(patTauCollection)
    )
    patTauTriggerMatcherName = patTauCollection+"TauTriggerMatcher"
    setattr(process, patTauTriggerMatcherName, patTauTriggerMatcher)
    process.triggerMatchingSequence += getattr(process, patTauTriggerMatcherName)

    # produce patTriggerObjectStandAloneedmAssociation object
    patTauTriggerEvent = process.patTriggerEvent.clone(
        patTriggerMatches = cms.VInputTag(patTauTriggerMatcherName)
    )
    patTauTriggerEventName = patTauCollection+"TauTriggerEvent"
    setattr(process, patTauTriggerEventName, patTauTriggerEvent)
    process.triggerMatchingSequence += getattr(process, patTauTriggerEventName)

    # embed the patTriggerObjectStandAloneedmAssociation to a tau collection
    patTauTriggerEmbedder = cms.EDProducer("PATTriggerMatchTauEmbedder",
        src     = cms.InputTag(patTauCollection),
        matches = cms.VInputTag(patTauTriggerMatcherName)
    )
    patTauTriggerEmbedderName = patTauCollection+"TauTriggerEmbedder"
    setattr(process, patTauTriggerEmbedderName, patTauTriggerEmbedder)
    process.triggerMatchingSequence += getattr(process, patTauTriggerEmbedderName)

    # clean empty pat taus from the embedded tau collection
    patTausTriggerMatchedAndCleaned = patTauEmptyCleanerProtoType.clone(
        src = cms.InputTag(patTauTriggerEmbedderName)
    )
    patTausTriggerMatchedAndCleanedName = patTauCollection+"TauTriggerMatched"
    setattr(process, patTausTriggerMatchedAndCleanedName, patTausTriggerMatchedAndCleaned)
    process.triggerMatchingSequence += getattr(process, patTausTriggerMatchedAndCleanedName)

    ###########################################################################
    # Tau -> HLT jet trigger matching
    # (needed for removing the tau candidate matching to jet trigger in QCD bkg measurement)
    print "Matching patTauCollection "+patTauCollection+" to jet trigger "+myJetTrigger
    # create DeltaR matcher of trigger objects
    patJetTriggerMatcher = patTauTriggerMatcher.clone(
        pathNames = cms.vstring(myJetTrigger)
    )
    patJetTriggerMatcherName = patTauCollection+"JetTriggerMatcher"
    setattr(process, patJetTriggerMatcherName, patJetTriggerMatcher)
    process.triggerMatchingSequence += getattr(process, patJetTriggerMatcherName)

    # produce patTriggerObjectStandAloneedmAssociation object
    patJetTriggerEvent = process.patTriggerEvent.clone(
        patTriggerMatches = cms.VInputTag(patJetTriggerMatcherName)
    )
    patJetTriggerEventName = patTauCollection+"JetTriggerEvent"
    setattr(process, patJetTriggerEventName, patJetTriggerEvent)
    process.triggerMatchingSequence += getattr(process, patJetTriggerEventName)

    # embed the patTriggerObjectStandAloneedmAssociation to a tau collection
    patJetTriggerEmbedder = cms.EDProducer("PATTriggerMatchTauEmbedder",
        src     = cms.InputTag(patTauCollection),
        matches = cms.VInputTag(patJetTriggerMatcherName)
    )
    patJetTriggerEmbedderName = patTauCollection+"JetTriggerEmbedder"
    setattr(process, patJetTriggerEmbedderName, patJetTriggerEmbedder)
    process.triggerMatchingSequence += getattr(process, patJetTriggerEmbedderName)

    # clean empty pat taus from the embedded tau collection
    patJetTriggerMatchedAndCleaned = patTauEmptyCleanerProtoType.clone(
        src = cms.InputTag(patJetTriggerEmbedderName)
    )
    patJetTriggerMatchedAndCleanedName = patTauCollection+"JetTriggerMatched"
    setattr(process, patJetTriggerMatchedAndCleanedName, patJetTriggerMatchedAndCleaned)
    process.triggerMatchingSequence += getattr(process, patJetTriggerMatchedAndCleanedName)

    ###########################################################################
    # Remove first tau matching to the jet trigger from the list
    # of tau -> HLT tau trigger matched patTaus
    patJetTriggerCleanedTauTriggerMatchedTaus = cms.EDProducer("TauHLTMatchJetTriggerRemover",
        tausMatchedToTauTriggerSrc = cms.InputTag(patTausTriggerMatchedAndCleanedName),
        tausMatchedToJetTriggerSrc = cms.InputTag(patJetTriggerMatchedAndCleanedName),
    )
    patJetTriggerCleanedTauTriggerMatchedTausName = patTauCollection+"TauTriggerMatchedAndJetTriggerCleaned"
    setattr(process, patJetTriggerCleanedTauTriggerMatchedTausName, patJetTriggerCleanedTauTriggerMatchedTaus)
    process.triggerMatchingSequence += getattr(process, patJetTriggerCleanedTauTriggerMatchedTausName)

process.out.outputCommands.extend([
    "keep patTaus_*TauTriggerMatched_*_*",
    "drop *_*TauTriggerMatcher_*_*",
    "drop *_*TauTriggerEvent_*_*",
    "drop *_*TauTriggerEmbedder_*_*",
    "drop patTaus_*JetTriggerMatched_*_*",
    "drop *_*JetTriggerMatcher_*_*",
    "drop *_*JetTriggerEvent_*_*",
    "drop *_*JetTriggerEmbedder_*_*",
    "keep *_*TauTriggerMatchedAndJetTriggerCleaned_*_*"
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

