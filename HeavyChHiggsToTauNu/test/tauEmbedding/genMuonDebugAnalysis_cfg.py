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
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_tauembedding_skim_v44_5/a9adb1d2c9d25e1e9802345c8c130cf6/skim_4932_1_Skq.root",
#        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_tauembedding_skim_v44_5/a9adb1d2c9d25e1e9802345c8c130cf6/skim_4933_1_aYy.root",
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

# Add the muon selection counters, as this is done after the skim
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF as MuonSelection
additionalCounters.extend(MuonSelection.getMuonPreSelectionCountersForEmbedding())
additionalCounters.extend(MuonSelection.getMuonSelectionCountersForEmbedding(dataVersion))

# Add configuration information to histograms.root
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools
process.infoPath = HChTools.addConfigInfo(process, options, dataVersion)

# Embedding muon selection
process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.PFEmbeddingSource_cff")
# disable isolation
process.commonSequence += (
    process.tightenedMuons +
    process.tightenedMuonsFilter +
    process.tightenedMuonsCount
)
additionalCounters.extend([
        "tightenedMuonsCount",
#        "tauEmbeddingMuonsCount"
])

# Configuration
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
analyzer = cms.EDAnalyzer("HPlusEmbeddingDebugMuonAnalyzer",
    muonSrc = cms.untracked.InputTag("tightenedMuons"),
    jetSrc = cms.untracked.InputTag("goodJets"),
    genSrc = cms.untracked.InputTag("genParticles"),

    muonPtCut = cms.untracked.double(41),
    muonEtaCut = cms.untracked.double(2.1),

    pileupWeightReader = param.pileupWeightReader.clone(
        enabled = False
    ),

    embeddingMuonEfficiency = param.embeddingMuonEfficiency.clone(
        mode = "mcEfficiency"
    ),

    eventCounter = param.eventCounter.clone(),
    histogramAmbientLevel = cms.untracked.string("Informative"),
)

HChTools.addAnalysis(process, "debugAnalyzer", analyzer,
                     preSequence=process.commonSequence,
                     additionalCounters=additionalCounters)
process.debugAnalyzer.eventCounter.printMainCounter = True

for era, weight in zip(dataEras, puWeights):
    m = analyzer.clone()
    m.pileupWeightReader.weightSrc = weight
    m.pileupWeightReader.enabled = True
    if era in ["Run2011A", "Run2011B"]:
        m.embeddingMuonEfficiency.mcSelect = era

    HChTools.addAnalysis(process, "debugAnalyzer"+era, m,
                         preSequence=process.commonSequence,
                         additionalCounters=additionalCounters)


f = open("configDumpEmbeddingDebugMuonAnalysis.py", "w")
f.write(process.dumpPython())
f.close()
