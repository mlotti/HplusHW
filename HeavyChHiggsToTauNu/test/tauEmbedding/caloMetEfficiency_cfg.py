import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

################################################################################
# Configuration

dataVersion = "311Xredigi"
#dataVersion = "41Xdata"

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
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_1_X/TTJets_TuneZ2_Spring11/TTJets_TuneZ2_7TeV-madgraph-tauola/Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_skim_v10/b3c16f1ee121445edb6d9b12e0772d8e/skim_104_1_sYD.root"
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

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as customisations
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
additionalCounters.extend(customisations.addFinalMuonSelection(process, process.commonSequence, param))
process.muonFinalSelectionJetSelectionGoodJets.src = "goodJets"

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChBTaggingFilter_cfi")
process.hPlusBTaggingPtrSelectorFilter.jetSrc = "muonFinalSelectionJetSelectionGoodJets"

#process.commonSequence *= process.hPlusBTaggingPtrSelectorFilter

process.btaggingCount = cms.EDProducer("EventCountProducer")
process.commonSequence *= process.btaggingCount
additionalCounters.append("btaggingCount")

addAnalysis(process, "caloMetEfficiency", createHistoAnalyzer(cms.InputTag("met"), [
    Histo("caloMet", "et()", min=0, max=400, nbins=400)
    ]),
            preSequence=process.commonSequence,
            additionalCounters = additionalCounters,
            signalAnalysisCounters=False
            )

process.p = cms.Path(
    process.commonSequence
)
