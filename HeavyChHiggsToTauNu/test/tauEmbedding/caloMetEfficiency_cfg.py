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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())#
process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        # For testing in lxplus
        #dataVersion.getAnalysisDefaultFileCastor()
        # For testing in jade
        #dataVersion.getAnalysisDefaultFileMadhatter()
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_1_X/SingleMu_160431-163261_May10/SingleMu/Run2011A_May10ReReco_v1_AOD_160431_tauembedding_skim_v11/d2154bd8672d0356e956d91d6de8768f/skim_19_2_olM.root"
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
           "doPatMuonPFIsolation": True,
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
weight = None
if dataVersion.isMC():
    import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param

    # Pileup weighting
    process.pileupWeight = cms.EDProducer("HPlusVertexWeightProducer",
        alias = cms.string("pileupWeight"),
    )
    param.setPileupWeightFor2011()
    insertPSetContentsTo(param.vertexWeight.clone(), process.pileupWeight)

    # Vertex weighting
    process.vertexWeight = cms.EDProducer("HPlusVertexWeightProducer",
        alias = cms.string("vertexWeight"),
    )
    param.setVertexWeightFor2011()
    insertPSetContentsTo(param.vertexWeight.clone(), process.vertexWeight)

    process.commonSequence *= (process.pileupWeight*process.vertexWeight)
    
# Add the muon selection counters, as this is done after the skim
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF_cff as MuonSelection
additionalCounters.extend(MuonSelection.muonSelectionCounters)

# Add configuration information to histograms.root
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################

process.firstPrimaryVertex = cms.EDProducer("HPlusSelectFirstVertex",
    src = cms.InputTag("offlinePrimaryVertices")
)
process.commonSequence *= process.firstPrimaryVertex

process.tightenedMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("tightMuons"),
    cut = cms.string("pt() > 40 && abs(eta()) < 2.1")
)
process.tightenedMuonsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("tightenedMuons"),
    minNumber = cms.uint32(1)
)
process.tauEmbeddingMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("tightenedMuons"),
    cut = cms.string("(userInt('byTightIc04ChargedOccupancy') + userInt('byTightIc04GammaOccupancy')) == 0")
)
process.tauEmbeddingMuonsFilter = cms.EDFilter("CandViewCountFilter",
                                       src = cms.InputTag("tauEmbeddingMuons"),
                                       minNumber = cms.uint32(1))
process.commonSequence *= (process.tightenedMuons * process.tightenedMuonsFilter * process.tauEmbeddingMuons * process.tauEmbeddingMuonsFilter)


import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as customisations
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
additionalCounters.extend(customisations.addFinalMuonSelection(process, process.commonSequence, param))
process.muonFinalSelectionJetSelectionGoodJets.src = "goodJets"

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChBTaggingFilter_cfi")
process.hPlusBTaggingPtrSelectorFilter.jetSrc = "muonFinalSelectionJetSelectionGoodJets"

process.commonSequence *= process.hPlusBTaggingPtrSelectorFilter

process.btaggingCount = cms.EDProducer("EventCountProducer")
process.commonSequence *= process.btaggingCount
additionalCounters.append("btaggingCount")

met = Histo("et", "et()", min=0, max=400, nbins=400)

histoList = [("calomet_", cms.InputTag("met"), [met]),
             ("calometNoHF_", cms.InputTag("metNoHF"), [met]),
             ("pfmet_", cms.InputTag("pfMet"), [met])]

def createAnalysis(prefix, weightSrc=None):
    wSrc = weightSrc
    if dataVersion.isData():
        wSrc = None

    analysis = Analysis(process, "analysis", prefix, additionalCounters=additionalCounters, weightSrc=wSrc)
    ha = analysis.addMultiHistoAnalyzer("h01_All", histoList)

    analysis.addCut("CaloMet25", cms.InputTag("metNoHF"), "et() > 25")
    ha = analysis.addCloneAnalyzer("h02_CaloMet25", ha)

    analysis.addCut("CaloMet45", cms.InputTag("metNoHF"), "et() > 45")
    ha = analysis.addCloneAnalyzer("h02_CaloMet45", ha)

    analysis.addCut("CaloMet60", cms.InputTag("metNoHF"), "et() > 60")
    ha = analysis.addCloneAnalyzer("h02_CaloMet60", ha)

    p = cms.Path(process.commonSequence * analysis.getSequence())
    setattr(process, prefix+"Path", p)

name = "caloMetEfficiency"
createAnalysis(name)
createAnalysis(name+"VertexWeight", weightSrc="vertexWeight")
createAnalysis(name+"PileupWeight", weightSrc="pileupWeight")
