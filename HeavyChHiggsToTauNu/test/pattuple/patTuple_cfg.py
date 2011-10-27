import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

dataVersion="42XmcS4"
#dataVersion="42Xdata"

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

doTauHLTMatching = options.doTauHLTMatching != 0
if doTauHLTMatching:
    if len(myTrigger) == 0:
        myTrigger = dataVersion.getDefaultSignalTrigger()
    print "Trigger used for tau matching: "+str(myTrigger)

################################################################################
# Output module
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('pattuple.root'),
    outputCommands = cms.untracked.vstring(
        "drop *",
        "keep *_genParticles_*_*",
        "keep edmTriggerResults_*_*_*",
#        "keep triggerTriggerEvent_*_*_*", # the information is alread in full PAT trigger
        "keep L1GlobalTriggerReadoutRecord_*_*_*",   # needed for prescale provider
        "keep L1GlobalTriggerObjectMapRecord_*_*_*", # needed for prescale provider
        "keep *_conditionsInEdm_*_*",
        "keep edmMergeableCounter_*_*_*", # in lumi block
        "keep PileupSummaryInfos_*_*_*", # only in MC
        "keep *_offlinePrimaryVertices_*_*",
        "keep *_l1GtTriggerMenuLite_*_*", # in run block, needed for prescale provider
        "keep recoCaloMETs_*_*_*", # keep all calo METs (metNoHF is needed!)
        "keep *_kt6PFJets_rho_HChPatTuple", # keep the rho of the event
        "keep *_HBHENoiseFilterResultProducer_*_*", # keep the resulf of HBHENoiseFilterResultProducer
        ),
    dropMetaData = cms.untracked.string("ALL")
)
# For MC we apply the trigger filter, but save all events in order to
# get a correct handle to all events with pileup weighting. The trict
# is that the rest of the path (after triggering) is NOT executed,
# hence the branches are empty for those events.
if dataVersion.isData():
    process.out.SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring("path")
    )


################################################################################
# Add PAT sequences
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import *

options.doPat=1
(process.sPAT, c) = addPatOnTheFly(process, options, dataVersion,
                                   doPlainPat=True, doPF2PAT=False,
                                   plainPatArgs={"doTauHLTMatching": doTauHLTMatching,
                                                 "matchingTauTrigger": myTrigger},
                                   )

process.out.outputCommands.extend([
        "drop *_selectedPatTausHpsTancPFTau_*_*",
        "drop *_patTausHpsTancPFTauTauTriggerMatched_*_*",
        "drop *_selectedPatJets_*_*",
        "drop patTriggerObjectStandAlones_patTrigger_*_*",
        ])

# Prune GenParticles
if dataVersion.isMC():
    process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
    process.genParticles = cms.EDProducer("GenParticlePruner",
        src = cms.InputTag("genParticles"),
        select = cms.vstring(
            "keep *",
            # Remove the soft photons from fragmentations (we have not needed them)
#            "drop pdgId() = {gamma} && mother().pdgId() = {pi0}"
            "drop++ pdgId() = {string}",
            "keep pdgId() = {string}",
            )
    )
    process.out.outputCommands.extend([
        "drop *_genParticles_*_*",
        "keep *_genParticles_*_"+process.name_(),
        ])

    process.sPAT.replace(process.patSequence, process.genParticles*process.patSequence)

#    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.printGenParticles_cff")
#    process.sPAT *= process.printGenParticles

#if dataVersion.isMC():
#    process.genParticles = cms.EDProducer("GenParticlePruner",
#        src = cms.InputTag("genParticles"),
#        select = cms.vstring("keep *")
#    )
#    process.out.outputCommands.extend([
#        "drop *_genParticles_*_*",
#        "keep *_genParticles_*_"+process.name_(),
#        ])
#
#    process.sPAT.replace(process.patSequence, process.genParticles*process.patSequence)


if dataVersion.isData():
    process.out.outputCommands.extend(["drop recoGenJets_*_*_*"])
else:
    process.out.outputCommands.extend([
            "keep LHEEventProduct_*_*_*",
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
if isinstance(myTrigger, basestring):
    myTrigger = [myTrigger]
process.heavyChHiggsToTauNuHLTFilter.HLTPaths = myTrigger
process.heavyChHiggsToTauNuHLTFilter.throw = False

# TotalKinematicsFilter for managing with buggy LHE+Pythia samples
# https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/1489.html
if dataVersion.isMC():
    process.load("GeneratorInterface.GenFilters.TotalKinematicsFilter_cfi")
    process.totalKinematicsFilter.src.setProcessName(dataVersion.getTriggerProcess())
    process.totalKinematicsFilterPath = cms.Path(
        process.totalKinematicsFilter
    )

#process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HLTTauEmulation_cff")
#process.out.outputCommands.extend(["keep recoCaloTaus_caloTauHLTTauEmu_*_*"])
#process.out.outputCommands.extend(["keep *_l1extraParticles_*_*"])
#process.out.outputCommands.extend(["keep recoTracks_generalTracks_*_*"])
#process.out.outputCommands.extend(["keep recoCaloJets_ak5CaloJets_*_*"])

process.triggerObjects = cms.EDAnalyzer("HPlusPATTriggerPrinter",
    src = cms.InputTag("patTriggerEvent")
)

# Create paths
process.path    = cms.Path(
#    process.collisionDataSelection * # this is supposed to be empty for MC
#    process.HLTTauEmu * # Hopefully not needed anymore in 39X as the tau trigger should be fixed
    process.sPAT
#    process.sPF2PAT *
#    process.sPF2PATnoPU
    * process.triggerObjects
)
process.skimPath = cms.Path(
    process.heavyChHiggsToTauNuSequence
)

# In case of OR of many triggers, add event counts for each trigger separately
if dataVersion.isData() and len(options.trigger) > 1:
    import HLTrigger.HLTfilters.hltHighLevel_cfi as hltHighLevel
    for trig in options.trigger:
        name = trig.replace("_", "")

        mt = hltHighLevel.hltHighLevel.clone(
            HLTPaths = cms.vstring(trig)
        )
        mt.TriggerResultsTag.setProcessName(dataVersion.getTriggerProcess())
        setattr(process, "Trigger"+name, mt)

        mc1 = cms.EDProducer("EventCountProducer")
        setattr(process, "Counter"+name, mc1)

        mc2 = cms.EDProducer("EventCountProducer")
        setattr(process, "CounterScraping"+name, mc2)

        path = cms.Path(
            process.hltPhysicsDeclared *
            mt * 
            mc1 *
            process.scrapingVeto *
            mc2
        )
        setattr(process, "Path"+name, path)

# If there is a need to apply some skim
if options.skimConfig != "":
    print "Skimming with configuration ", options.skimConfig
    process.load(options.skimConfig)
    process.plainPatSequence.replace(process.plainPatEndSequence,
                                     process.skimSequence*process.plainPatEndSequence)

# Output module in EndPath
process.outpath = cms.EndPath(process.out)

