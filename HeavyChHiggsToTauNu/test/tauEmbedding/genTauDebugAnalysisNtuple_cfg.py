import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

dataVersion = "44XmcS6"

options, dataVersion = getOptionsDataVersion(dataVersion, useDefaultSignalTrigger=False)

process = cms.Process("TauEmbeddingAnalysis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_tauembedding_gentauskim_v44_5/9ecb3a23e436fc2ffd8a803eac2a3a15/pattuple_1012_1_LSv.root",
    ),
)

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
# Fragment to run PAT on the fly if requested from command line
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
patArgs = {"doPatTrigger": False,
#           "doPatTaus": False,
#           "doHChTauDiscriminators": False,
           "doPatElectronID": True,
           "doTauHLTMatching": False,
           }
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, patArgs=patArgs,
                                                            doHBHENoiseFilter=False,
                                                            )
import HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisConfiguration as AnalysisConfiguration
dataEras = [
    "Run2011AB",
    "Run2011A",
    "Run2011B",
]
puWeights = AnalysisConfiguration.addPuWeightProducers(dataVersion, process, process.commonSequence, dataEras)

# Add GenTau skim counters
import HiggsAnalysis.HeavyChHiggsToTauNu.CustomGenTauSkim as tauSkim
additionalCounters = tauSkim.getCounters() + additionalCounters
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as customisations
process.genTaus = cms.EDFilter("GenParticleSelector",
    src = cms.InputTag("genParticles"),
    cut = cms.string(customisations.generatorTauSelection % customisations.generatorTauPt),
)
process.commonSequence += process.genTaus

# Add configuration information to histograms.root
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools
process.infoPath = HChTools.addConfigInfo(process, options, dataVersion)

# PV selection
import HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex as HChPrimaryVertex
HChPrimaryVertex.addPrimaryVertexSelection(process, process.commonSequence)

# Jet selection
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF as muonSelection
muonSelection.addMuonSelectionForEmbedding(process)
process.commonSequence += process.goodJets

# Muon selection (for muons coming from "the other W"), must the same as for embedding
process.commonSequence += process.tightMuons
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.PFEmbeddingSource_cff")
process.commonSequence += process.tightenedMuons


# Configuration
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.analysisConfig as analysisConfig
import HiggsAnalysis.HeavyChHiggsToTauNu.Ntuple as Ntuple
ntuple = cms.EDAnalyzer("HPlusTauNtupleAnalyzer",
    selectedPrimaryVertexSrc = cms.InputTag("selectedPrimaryVertex"),
    goodPrimaryVertexSrc = cms.InputTag("goodPrimaryVertices"),

    patTriggerSrc = cms.InputTag("patTriggerEvent"),
    triggerPaths = cms.PSet(),

    tauEnabled = cms.bool(False),
    tauSrc = cms.InputTag("NOT_SET"),
    tauFunctions = cms.PSet(),

    jets = Ntuple.jets.clone(
        enabled = False,
    ),

    muonsEnabled = cms.bool(True),
    muons = Ntuple.muons.clone(
        src = "tightenedMuons",
        functions = cms.PSet(),
    )

    genParticleSrc = cms.InputTag("genParticles"),
    genParticleTauSrc = cms.InputTag("genTaus"),
    genTTBarEnabled = cms.bool(True),

    mets = cms.PSet(),
    doubles = cms.PSet(),

    eventCounter = param.eventCounter.clone(),
    histogramAmbientLevel = cms.untracked.string("Informative"),
)

for era, weight in zip(dataEras, puWeights):
    setattr(ntuple.doubles, "weightPileup_"+era, cms.InputTag(weight))


HChTools.addAnalysis(process, "tauNtuple", ntuple,
                     preSequence=process.commonSequence,
                     additionalCounters=additionalCounters)
process.tauNtuple.eventCounter.printMainCounter = True


f = open("configDumpEmbeddingDebugTauAnalysisNtuple.py", "w")
f.write(process.dumpPython())
f.close()
