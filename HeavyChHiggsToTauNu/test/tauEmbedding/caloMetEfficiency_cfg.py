import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

################################################################################
# Configuration

dataVersion = "42Xmc"
#dataVersion = "42Xdata"

debug = False
#debug = True

################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)
#options.doPat = 1

################################################################################
# Define the process
process = cms.Process("CaloMetEfficiency")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(200) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())#
process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        # For testing in lxplus
        #dataVersion.getAnalysisDefaultFileCastor()
        # For testing in jade
        #dataVersion.getAnalysisDefaultFileMadhatter()
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_2_X/TTJets_TuneZ2_Summer11_1/TTJets_TuneZ2_7TeV-madgraph-tauola/Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_skim_v13_2/6ce8de2c5b6c0c9ed414998577b7e28d/skim_982_1_xgs.root"
  )
)
###############################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
#process.options.wantSummary = cms.untracked.bool(True)
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
process.MessageLogger.categories.append("TauIsolationSelector")

# Uncomment the following in order to print the counters at the end of
# the job (note that if many other modules are being run in the same
# job, their INFO messages are printed too)
#process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")

# Fragment to run PAT on the fly if requested from command line
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
from PhysicsTools.PatAlgos.tools.coreTools import removeSpecificPATObjects
patArgs = {"doPatTrigger": False,
#           "doPatTaus": False,
#           "doHChTauDiscriminators": False,
           "doPatElectronID": True,
           "doTauHLTMatching": False,
           }
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, plainPatArgs=patArgs)
#process.commonSequence.remove(process.goodPrimaryVertices10)
if options.doPat == 0:
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi")
    process.commonSequence *= (
        process.goodPrimaryVertices *
        process.goodPrimaryVertices10
    )

from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *
# Pileup weighting
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
process.pileupWeightEPS = cms.EDProducer("HPlusVertexWeightProducer",
    alias = cms.string("pileupWeightEPS"),
)
process.pileupWeightRun2011AnoEPS = process.pileupWeightEPS.clone(
    alias = "pileupWeightRun2011AnoEPS"
)
process.pileupWeightRun2011A = process.pileupWeightEPS.clone(
    alias = "pileupWeightRun2011A"
)
param.setPileupWeightFor2011(dataVersion, era="EPS")
insertPSetContentsTo(param.vertexWeight.clone(), process.pileupWeightEPS)
param.setPileupWeightFor2011(dataVersion, era="Run2011A-EPS")
insertPSetContentsTo(param.vertexWeight.clone(), process.pileupWeightRun2011AnoEPS)
param.setPileupWeightFor2011(dataVersion, era="Run2011A")
insertPSetContentsTo(param.vertexWeight.clone(), process.pileupWeightRun2011A)

process.commonSequence *= (
    process.pileupWeightEPS *
    process.pileupWeightRun2011AnoEPS *
    process.pileupWeightRun2011A
)
    
# Add the muon selection counters, as this is done after the skim
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF_cff as MuonSelection
additionalCounters.extend(MuonSelection.muonSelectionCounters)

# Add configuration information to histograms.root
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################

process.firstPrimaryVertex = cms.EDProducer("HPlusFirstVertexSelector",
    src = cms.InputTag("offlinePrimaryVertices")
)
process.commonSequence *= process.firstPrimaryVertex

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as customisations
muons = customisations.addMuonIsolationEmbedding(process, process.commonSequence, muons="tightMuons")

process.tightenedMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag(muons),
#    cut = cms.string("pt() > 40 && abs(eta()) < 2.1")
    cut = cms.string(
        "pt() > 40 && abs(eta()) < 2.1 &&"
        "isGlobalMuon() && isTrackerMuon()"
        "&& muonID('GlobalMuonPromptTight')"
        "&& innerTrack().numberOfValidHits() > 10"
        "&& innerTrack().hitPattern().pixelLayersWithMeasurement() >= 1"
        "&& numberOfMatches() > 1"
        "&& abs(dB()) < 0.02"
    )

)
process.tightenedMuonsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("tightenedMuons"),
    minNumber = cms.uint32(1)
)
process.tightenedMuonsCount = cms.EDProducer("EventCountProducer")
process.tauEmbeddingMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("tightenedMuons"),
    cut = cms.string("(userInt('byTightIc04ChargedOccupancy') + userInt('byTightIc04GammaOccupancy')) == 0")
)
process.tauEmbeddingMuonsFilter = cms.EDFilter("PATCandViewCountFilter",
    src = cms.InputTag("tauEmbeddingMuons"),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(1)
)
process.tauEmbeddingMuonsCount = cms.EDProducer("EventCountProducer")
process.selectedPatMuonsEmbeddingMuonCleaned = customisations.selectedMuonCleanedMuons("tauEmbeddingMuons") # needed for muon veto
process.commonSequence *= (
    process.tightenedMuons * process.tightenedMuonsFilter * process.tightenedMuonsCount *
    process.tauEmbeddingMuons * process.tauEmbeddingMuonsFilter * process.tauEmbeddingMuonsCount *
    process.selectedPatMuonsEmbeddingMuonCleaned
)
additionalCounters.extend(["tightenedMuonsCount", "tauEmbeddingMuonsCount"])


import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
additionalCounters.extend(customisations.addFinalMuonSelection(process, process.commonSequence, param))
process.muonFinalSelectionJetSelectionGoodJets.src = "goodJets"

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChBTaggingFilter_cfi")
process.hPlusBTaggingPtrSelectorFilter.jetSrc = "muonFinalSelectionJetSelectionGoodJets"

process.commonSequence *= process.hPlusBTaggingPtrSelectorFilter

process.btaggingCount = cms.EDProducer("EventCountProducer")
process.commonSequence *= process.btaggingCount
additionalCounters.append("btaggingCount")

ntuple = cms.EDAnalyzer("HPlusMetNtupleAnalyzer",
    patTriggerEvent = cms.InputTag("patTriggerEvent"),
    mets = cms.PSet(
        caloMet_p4 = cms.InputTag("met"),
        caloMetNoHF_p4 = cms.InputTag("metNoHF"),
        pfMet_p4 = cms.InputTag("pfMet"),
    ),
    doubles = cms.PSet(
        pileupWeightEPS = cms.InputTag("pileupWeightEPS"),
        weightPileup_Run2011AnoEPS = cms.InputTag("pileupWeightRun2011AnoEPS"),
        weightPileup_Run2011A = cms.InputTag("pileupWeightRun2011A")
    ),
)

addAnalysis(process, "metNtuple", ntuple,
            preSequence=process.commonSequence,
            additionalCounters=additionalCounters,
            signalAnalysisCounters=False)
process.metNtupleCounters.printMainCounter = True

# Replace all event counters with the weighted one
eventCounters = []
for label, module in process.producers_().iteritems():
    if module.type_() == "EventCountProducer":
        eventCounters.append(label)
prototype = cms.EDProducer("HPlusEventCountProducer",
    weightSrc = cms.InputTag("pileupWeightRun2011A")
)
for label in eventCounters:
    process.globalReplace(label, prototype.clone())


# met = Histo("et", "et()", min=0, max=400, nbins=400)

# histoList = [("calomet_", cms.InputTag("met"), [met]),
#              ("calometNoHF_", cms.InputTag("metNoHF"), [met]),
#              ("pfmet_", cms.InputTag("pfMet"), [met])]

# def createAnalysis(prefix, weightSrc=None):
#     wSrc = weightSrc
#     if dataVersion.isData():
#         wSrc = None

#     analysis = Analysis(process, "analysis", prefix, additionalCounters=additionalCounters, weightSrc=wSrc)
#     ha = analysis.addMultiHistoAnalyzer("h01_All", histoList)

#     analysis.addCut("CaloMet25", cms.InputTag("metNoHF"), "et() > 25")
#     ha = analysis.addCloneAnalyzer("h02_CaloMet25", ha)

#     analysis.addCut("CaloMet45", cms.InputTag("metNoHF"), "et() > 45")
#     ha = analysis.addCloneAnalyzer("h02_CaloMet45", ha)

#     analysis.addCut("CaloMet60", cms.InputTag("metNoHF"), "et() > 60")
#     ha = analysis.addCloneAnalyzer("h02_CaloMet60", ha)

#     p = cms.Path(process.commonSequence * analysis.getSequence())
#     setattr(process, prefix+"Path", p)

# name = "caloMetEfficiency"
# createAnalysis(name)
# createAnalysis(name+"VertexWeight", weightSrc="vertexWeight")
# createAnalysis(name+"PileupWeight", weightSrc="pileupWeight")
