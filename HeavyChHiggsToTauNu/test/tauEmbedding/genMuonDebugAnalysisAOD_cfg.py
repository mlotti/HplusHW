import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

dataVersion = "44XmcS6"

options, dataVersion = getOptionsDataVersion(dataVersion, useDefaultSignalTrigger=False)

process = cms.Process("TauEmbeddingAnalysis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        "file:/mnt/flustre/mkortela/data/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM/7EE6381E-D036-E111-9BF5-002354EF3BDF.root"
    )
)

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")

additionalCounters = []
# Add configuration information to histograms.root
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools
process.infoPath = HChTools.addConfigInfo(process, options, dataVersion)

# Configuration
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
analyzer = cms.EDAnalyzer("HPlusEmbeddingDebugMuonAnalyzer",
    muonSrc = cms.untracked.InputTag("tightenedMuons"),
    jetSrc = cms.untracked.InputTag("goodJets"),
    genSrc = cms.untracked.InputTag("genParticles"),
    onlyGen = cms.untracked.bool(True),

    muonPtCut = cms.untracked.double(40),
    muonEtaCut = cms.untracked.double(2.1),

    embeddingMuonEfficiency = param.embeddingMuonEfficiency.clone(
        mode = "mcEfficiency"
    ),

    eventCounter = param.eventCounter.clone(),
    histogramAmbientLevel = cms.untracked.string("Informative"),
)

HChTools.addAnalysis(process, "debugAnalyzer", analyzer,
#                     preSequence=process.commonSequence,
                     additionalCounters=additionalCounters)
process.debugAnalyzer.eventCounter.printMainCounter = True

f = open("configDumpEmbeddingDebugMuonAnalysisAOD.py", "w")
f.write(process.dumpPython())
f.close()
