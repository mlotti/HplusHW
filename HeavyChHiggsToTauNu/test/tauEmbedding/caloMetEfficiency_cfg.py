import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

################################################################################
# Configuration

#dataVersion = "44XmcS6"
dataVersion = "44Xdata"

debug = False
#debug = True

PF2PATVersion = "PFlow"

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
        #"/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Tauembedding_skim_v44_1_TTJets_TuneZ2_Fall11//2f6341f5a210122b891e378fe7516bcf/skim_1001_1_qUS.root"
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/SingleMu_Mu_173693-177452_2011B_Nov19/SingleMu/Tauembedding_skim_v44_1_SingleMu_Mu_173693-177452_2011B_Nov19//079054b3ab4c4121ae105c34f9c44ff5/skim_100_1_Khr.root"
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
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, patArgs=patArgs)
#process.commonSequence.remove(process.goodPrimaryVertices10)
#if options.doPat == 0:
#    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi")
#    process.commonSequence *= (
#        process.goodPrimaryVertices *
#        process.goodPrimaryVertices10
#    )

from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *
# Pileup weighting
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
param.changeCollectionsToPF2PAT(postfix=PF2PATVersion)
puWeights = [
    ("Run2011A", "Run2011A"),
    ("Run2011B", "Run2011B"),
    ("Run2011AB", "Run2011AB")
    ]
for era, name in puWeights:
    modname = "pileupWeight"+name
    setattr(process, modname, cms.EDProducer("HPlusVertexWeightProducer",
        alias = cms.string(modname),
    ))
    param.setPileupWeight(dataVersion, process=process, commonSequence=process.commonSequence, era=era)
    insertPSetContentsTo(param.vertexWeight.clone(), getattr(process, modname))
    process.commonSequence.insert(0, getattr(process, modname))
# FIXME: this is only a consequence of the swiss-knive effect...
process.commonSequence.remove(process.goodPrimaryVertices)
process.commonSequence.insert(0, process.goodPrimaryVertices)
# FIXME: and this one because HBHENoiseFilter is not stored in embedding skims of v44_1
if dataVersion.isData():
    process.HBHENoiseSequence = cms.Sequence()
    process.commonSequence.replace(process.HBHENoiseFilter, process.HBHENoiseSequence*process.HBHENoiseFilter)
    import HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection as DataSelection
    DataSelection.addHBHENoiseFilterResultProducer(process, process.HBHENoiseSequence)

# Add the muon selection counters, as this is done after the skim
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF as MuonSelection
additionalCounters.extend(MuonSelection.getMuonSelectionCountersForEmbedding(postfix=PF2PATVersion))

# Add configuration information to histograms.root
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################

# Add type 1 MET
#import HiggsAnalysis.HeavyChHiggsToTauNu.signalAnalysis as signalAnalysis # use signalAnalysis only to transfer the type1 MET collection (quick hack)
#process.signalAnalysis = signalAnalysis.createEDFilter(param)
#import HiggsAnalysis.HeavyChHiggsToTauNu.HChMetCorrection as MetCorrection
#sequence = MetCorrection.addCorrectedMet(process, process.signalAnalysis, postfix=PF2PATVersion)
#process.commonSequence *= sequence

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as customisations
muons = customisations.addMuonIsolationEmbedding(process, process.commonSequence, muons="tightMuons"+PF2PATVersion)

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
#    cut = cms.string("(userInt('byTightIc04ChargedOccupancy') + userInt('byTightIc04GammaOccupancy')) == 0")
    # Standard deltaBeta-corrected isolation, tight working point
    cut = cms.string("( chargedHadronIso() + max(0, neutralHadronIso()+photonIso()-0.5*puChargedHadronIso()) )/pt() < 0.12")
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
process.muonFinalSelectionJetSelectionGoodJets.src = "goodJets"+PF2PATVersion

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
#        pfMetType1_p4 = cms.InputTag(process.signalAnalysis.MET.type1Src.value())
    ),
    doubles = cms.PSet()
)
for era, name in puWeights:
    setattr(ntuple.doubles, "weightPileup_"+name, cms.InputTag("pileupWeight"+name))
#del process.signalAnalysis

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
    weightSrc = cms.InputTag("pileupWeight"+puWeights[-1][1])
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
