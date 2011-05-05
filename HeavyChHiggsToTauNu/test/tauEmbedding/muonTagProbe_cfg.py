# https://twiki.cern.ch/twiki/bin/view/CMS/TagAndProbe
# https://twiki.cern.ch/twiki/bin/view/CMS/MuonTagAndProbe
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonAnalysisMuonAssociators#Configuration_file_to_produce_PA
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideTagProbeFitTreeProducer

import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

dataVersion = "39Xredigi"
#dataVersion = "311Xredigi"
#dataVersion = "41Xdata"

################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)
options.doPat=1

trigger = options.trigger
if len(trigger) == 0:
    trigger = "HLT_Mu9"

#mu9filter = "hltSingleL3MuonPre9"
#mu15filter = "hltSingleL3MuonPre15"
mu9filter = "hltSingleMu9L3Filtered9"
mu15filter = "hltSingleMu15L3Filtered15"
mu20filter = "hltSingleMu20L3Filtered20"
mu24filter = "hltSingleMu24L3Filtered24"

triggerFilter = ""
if "HLT_Mu9" in trigger:
    triggerFilter = mu9filter
elif "HLT_Mu15" in trigger:
    triggerFilter = mu15filter
elif "HLT_Mu20" in trigger:
    triggerFilter = mu20filter
elif "HLT_Mu24" in trigger:
    triggerFilter = mu24filter
else:
    raise Exception("Trigger '%s' not recognized" % trigger)

print "Trigger %s, filter %s" % (trigger, triggerFilter)


################################################################################
# Define the process
process = cms.Process("TagProbe")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        #dataVersion.getPatDefaultFileMadhatter()
        "file:/mnt/flustre/mkortela/data/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Winter10-E7TeV_ProbDist_2010Data_BX156_START39_V8-v1/AODSIM/E28BCD86-B311-E011-A953-E0CB4E19F95B.root"
        #"/store/data/Run2011A/SingleMu/AOD/PromptReco-v1/000/160/431/7A229484-EB4F-E011-B173-0030487CD7B4.root"
    )
)

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.load("Configuration.StandardSequences.Reconstruction_cff")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

################################################################################

# PAT
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('dummy.root'),
    outputCommands = cms.untracked.vstring()
)

from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
patArgs = {
#    "doPatTaus": False,
    "doPatMET": False,
    "doPatElectronID": False,
    "doPatCalo": False,
    "doBTagging": False,
    "doPatMuonPFIsolation": True,
    "doTauHLTMatching": False,
    }
process.commonSequence, counters = addPatOnTheFly(process, options, dataVersion, patArgs=patArgs)
del process.out
process.patDefaultSequence.remove(process.countPatTaus)

# Triggering
if dataVersion.isMC():
    process.load("HLTrigger.HLTfilters.triggerResultsFilter_cfi")
    process.triggerResultsFilter.hltResults = cms.InputTag("TriggerResults", "", dataVersion.getTriggerProcess())
    process.triggerResultsFilter.l1tResults = cms.InputTag("") # dummy
    process.triggerResultsFilter.throw = cms.bool(True)
    process.triggerResultsFilter.triggerConditions = cms.vstring(trigger)
    process.commonSequence *= process.triggerResultsFilter
else:
    process.TriggerFilter.triggerConditions = [trigger]

process.triggeredCount = cms.EDProducer("EventCountProducer")
process.commonSequence *= process.triggeredCount
counters.append("triggeredCount")

# Primary vertex
process.firstPrimaryVertex = cms.EDProducer("HPlusSelectFirstVertex",
    src = cms.InputTag("offlinePrimaryVertices")
)
process.goodPrimaryVertex = cms.EDFilter("VertexSelector",
    filter = cms.bool(False),
    src = cms.InputTag("firstPrimaryVertex"),
    cut = cms.string("!isFake && ndof > 4 && abs(z) < 24.0 && position.rho < 2.0")
)
process.goodPrimaryVertexFilter = cms.EDFilter("VertexCountFilter",
    src = cms.InputTag("goodPrimaryVertex"),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(999)
)
process.goodPrimaryVertexCount = cms.EDProducer("EventCountProducer")
process.commonSequence *= (
    process.firstPrimaryVertex *
    process.goodPrimaryVertex *
    process.goodPrimaryVertexFilter *
    process.goodPrimaryVertexCount
)
counters.append("goodPrimaryVertexCount")


# HLT matching and embedding
import MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff as muonTrigger
process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")
muonTrigger.useExistingPATMuons(process, "patMuons")
process.patTrigger.onlyStandAlone = False
process.commonSequence *= process.patMuonsWithTriggerSequence

# Preselection by tracks
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.goodTracks = cms.EDFilter("TrackSelector",
    src = cms.InputTag("generalTracks"), # or cms.InputTag("standAloneMuons","UpdatedAtVtx"), 
#    cut = cms.string("pt > 25 && abs(eta) < 2.1 && numberOfValidHits >= 12"),
    cut = cms.string("pt > 25 && abs(eta) < 2.1"),
    filter = cms.bool(True)
)
process.goodTracksCount = cms.EDProducer("EventCountProducer")
counters.append("goodTracksCount")
process.trackCands = cms.EDProducer("ConcreteChargedCandidateProducer",
    src = cms.InputTag("goodTracks"),
    particleType = cms.string("mu+")
)
process.commonSequence *= (
    process.goodTracks *
    process.goodTracksCount *
    process.trackCands
)

# Preselection by track invariant mass
process.zCands = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("trackCands@+ trackCands@-"),
    cut   = cms.string("60 < mass < 120")
)
process.zCandsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("zCands"),
    minNumber = cms.uint32(1)
)
process.zCandsCount = cms.EDProducer("EventCountProducer")
counters.append("zCandsCount")
process.commonSequence *= (process.zCands * process.zCandsFilter * process.zCandsCount)

# Tag and Probe definitions
process.tagMuonsWithoutZ = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string(
        "isGlobalMuon() && isTrackerMuon()"
        "&& pt() > 30 && abs(eta()) < 2.1"
        "&& muonID('GlobalMuonPromptTight')"
        "&& innerTrack().numberOfValidHits() > 10"
        "&& innerTrack().hitPattern.pixelLayersWithMeasurement() >= 1"
        "&& numberOfMatches() > 1"
        "&& abs(dB()) < 0.02"
        "&& (isolationR03().emEt+isolationR03().hadEt+isolationR03().sumPt)/pt() < 0.1"
        "&& !triggerObjectMatchesByFilter('%s').empty()" % triggerFilter
    ),
)
process.tagMuons = cms.EDFilter("HPlusPATMuonViewVertexZSelector",
    src = cms.InputTag("tagMuonsWithoutZ"),
    vertexSrc = cms.InputTag("goodPrimaryVertex"),
    maxZ = cms.double(1.0)
)

#process.trkProbes  = cms.EDProducer("ConcreteChargedCandidateProducer", 
#    src  = cms.InputTag("goodTracks"),      
#    particleType = cms.string("mu+"),     # this is needed to define a mass
#)
process.probeMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string(
        "isTrackerMuon()"
        "&& pt() > 40"
    )
)
process.probeMuonsVertexZ = cms.EDProducer("HPlusCandViewVertexZDiffComputer",
    candSrc = cms.InputTag("probeMuons"),
    vertexSrc = cms.InputTag("goodPrimaryVertex")
)
process.probeMuonsTauIsolationVLoose = cms.EDProducer("HPlusTauIsolationPATMuonRefSelector",
    candSrc = cms.InputTag("probeMuons"),
    tauSrc = cms.InputTag("selectedPatTausHpsPFTau"),
    isolationDiscriminator = cms.string("byVLooseIsolation"),
    againstMuonDiscriminator = cms.string("againstMuonLoose"),
    deltaR = cms.double(0.15),
    minCands = cms.uint32(1)
)
process.probeMuonsTauIsolationLoose = process.probeMuonsTauIsolationVLoose.clone(isolationDiscriminator = "byLooseIsolation")
process.probeMuonsTauIsolationMedium = process.probeMuonsTauIsolationVLoose.clone(isolationDiscriminator = "byMediumIsolation")
process.probeMuonsTauIsolationTight = process.probeMuonsTauIsolationVLoose.clone(isolationDiscriminator = "byTightIsolation")


process.muonMultiplicity = cms.EDAnalyzer("HPlusCandViewMultiplicityAnalyzer",
    allMuons = cms.untracked.PSet(
        src = cms.InputTag("patMuonsWithTrigger"),
        min = cms.untracked.int32(0),
        max = cms.untracked.int32(20),
        nbins = cms.untracked.int32(20)
    ),
    tagMuons = cms.untracked.PSet(
        src = cms.InputTag("tagMuons"),
        min = cms.untracked.int32(0),
        max = cms.untracked.int32(20),
        nbins = cms.untracked.int32(20)
    ),
    probeMuons = cms.untracked.PSet(
        src = cms.InputTag("probeMuons"),
        min = cms.untracked.int32(0),
        max = cms.untracked.int32(20),
        nbins = cms.untracked.int32(20)
    ),
)

process.tagProbes = cms.EDProducer("CandViewShallowCloneCombiner",
#    decay = cms.string("tagMuons@+ trkProbes@-"),
    decay = cms.string("tagMuons@+ probeMuons@-"),
#    cut   = cms.string("2.5 < mass < 3.8"),
    cut   = cms.string("60 < mass < 120"),
)

process.debug = cms.EDAnalyzer("EventContentAnalyzer")

process.tagAndProbeSequence = cms.Sequence(
    process.tagMuonsWithoutZ *
    process.tagMuons *
#    process.trkProbes *
    process.probeMuons *
    process.probeMuonsVertexZ *
    process.probeMuonsTauIsolationVLoose *
    process.probeMuonsTauIsolationLoose *
    process.probeMuonsTauIsolationMedium *
    process.probeMuonsTauIsolationTight *
    process.muonMultiplicity *
#    process.debug *
    process.tagProbes
)

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonAnalysis as muonAnalysis
sumIsoRel = muonAnalysis.isolations["sumIsoRel"]
pfSumIsoRel = muonAnalysis.isolations["pfSumIsoRel"]

# Tag and Probe tree
process.tnpTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
    # choice of tag and probe pairs, and arbitration
    tagProbePairs = cms.InputTag("tagProbes"),
    arbitration   = cms.string("OneProbe"), ## that is, use only tags associated to a single probe.
    # probe variables
    variables = cms.PSet(
        pt     = cms.string("pt"),
        eta    = cms.string("eta"),
        abseta = cms.string("abs(eta)"),

        #
        sumIsoRel = cms.string(sumIsoRel),
        pfSumIsoRel = cms.string(pfSumIsoRel),

        # external variables
        dz = cms.InputTag("probeMuonsVertexZ"),
    ),
    # choice of what defines a 'passing' probe
    flags = cms.PSet(
        isGlobalMuon = cms.string("isGlobalMuon"),
        isTrackerMuon = cms.string("isTrackerMuon"),
        #isHLTMu9     = cms.string("!triggerObjectMatchesByFilter('hltSingleL3MuonPre9').empty()"),  
        #isHLTMu15    = cms.string("!triggerObjectMatchesByFilter('hltSingleL3MuonPre15').empty()"),  
        isHLTMu9     = cms.string("!triggerObjectMatchesByFilter('%s').empty()" % mu9filter),
        isHLTMu15    = cms.string("!triggerObjectMatchesByFilter('%s').empty()" % mu15filter),
        isHLTMu20    = cms.string("!triggerObjectMatchesByFilter('%s').empty()" % mu20filter),
        isHLTMu24    = cms.string("!triggerObjectMatchesByFilter('%s').empty()" % mu24filter),
        isID         = cms.string("muonID('GlobalMuonPromptTight')"),
        hitQuality   = cms.string("innerTrack().numberOfValidHits() > 10 && innerTrack().hitPattern.pixelLayersWithMeasurement() >= 1 && numberOfMatches() > 1"),
        dB           = cms.string("abs(dB()) < 0.02"),
        sumIsoRel10   = cms.string("%s < 0.1" % sumIsoRel),
        sumIsoRel15   = cms.string("%s < 0.15" % sumIsoRel),
        pfSumIsoRel10   = cms.string("%s < 0.1" % pfSumIsoRel),
        pfSumIsoRel15   = cms.string("%s < 0.15" % pfSumIsoRel),
        fullSelection = cms.string(
            "isGlobalMuon() && isTrackerMuon()"
            "&& pt() > 30 && abs(eta()) < 2.1"
            "&& muonID('GlobalMuonPromptTight')"
            "&& innerTrack().numberOfValidHits() > 10"
            "&& innerTrack().hitPattern.pixelLayersWithMeasurement() >= 1"
            "&& numberOfMatches() > 1"
            "&& abs(dB()) < 0.02"
            "&& (isolationR03().emEt+isolationR03().hadEt+isolationR03().sumPt)/pt() < 0.1"
            "&& !triggerObjectMatchesByFilter('%s').empty()" % triggerFilter
        ),

        # external flags
        tauIsolationVLoose = cms.InputTag("probeMuonsTauIsolationVLoose"),
        tauIsolationLoose = cms.InputTag("probeMuonsTauIsolationLoose"),
        tauIsolationMedium = cms.InputTag("probeMuonsTauIsolationMedium"),
        tauIsolationTight = cms.InputTag("probeMuonsTauIsolationTight"),
    ),
    ## DATA-related info
    addRunLumiInfo = cms.bool(True),
    ## MC-related info
    isMC = cms.bool(False), ## on MC you can set this to true, add some parameters and get extra info in the tree.
#    isMC = cms.bool(dataVersion.isMC()), ## on MC you can set this to true, add some parameters and get extra info in the tree.
)

# Count analyzer
process.tnpCounters = cms.EDAnalyzer("HPlusEventCountAnalyzer",
    counters = cms.untracked.VInputTag([cms.InputTag(c) for c in counters])
)

# Path
process.tagAndProbeSequence *= (process.tnpTree * process.tnpCounters)

process.path = cms.Path(
    process.commonSequence *
    process.tagAndProbeSequence
)
