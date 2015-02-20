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

# do PAT muon stuff
process.commonSequence = cms.Sequence()
# Gen-level filtering
process.allEvents = cms.EDProducer("EventCountProducer")
process.genMuons = cms.EDFilter("GenParticleSelector",
    src = cms.InputTag("genParticles"),
    cut = cms.string("abs(pdgId()) == 13 && pt() > 30 && abs(eta()) < 2.5 && abs(mother().pdgId()) != 13")
)
process.genMuonsFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("genMuons"),
    minNumber = cms.uint32(1),
)
process.genMuonsCount = cms.EDProducer("EventCountProducer")
process.commonSequence += (
    process.allEvents +
    process.genMuons +
    process.genMuonsFilter +
    process.genMuonsCount
)
additionalCounters.extend(["allEvents", "genMuonsCount"])

# PAT muons
options.doPat = 1
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
process.fooSequenceSequence, fooCounters = addPatOnTheFly(process, options, dataVersion)
process.patMuons.userData.userFloats.src = []
process.selectedPatMuons.src = "patMuons"
process.selectedPatMuons.cut = ""
process.commonSequence += (
    process.pfParticleSelectionSequence +
    process.muIsoSequence +
    process.makePatMuons +
    process.selectedPatMuons
)

# muon selection
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.muonSelectionPF as MuonSelection
MuonSelection.addMuonSelectionForEmbedding(process)
process.commonSequence += (
#    process.muonSelectionAllEvents +
    process.tightMuons
#    process.tightMuonsFilter +
#    process.muonSelectionMuons
)
#additionalCounters.extend(["muonSelectionAllEvents", "muonSelectionMuons"])


process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.PFEmbeddingSource_cff")
import re
pt_re = re.compile("pt\(\) > \d+ &&")
(val, count) = pt_re.subn("", process.tightenedMuons.cut.value())
if count == 0:
    raise Exception("Did not find pt cut from %s" % process.tightenedMuons.cut.value())
process.tightenedMuons.cut = val
process.commonSequence += (
    process.tightenedMuons
#    process.tightenedMuonsFilter +
#    process.tightenedMuonsCount
)
#additionalCounters.append("tightenedMuonsCount")

# MuScleFit correction
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/MuScleFitCorrections2012
process.tightenedMuonsMuscle = cms.EDProducer("MuScleFitPATMuonCorrector", 
    src = cms.InputTag("tightenedMuons"), 
    debug = cms.bool(False), 
    identifier = cms.string("Fall11_START44"), 
    applySmearing = cms.bool(False), 
    fakeSmearing = cms.bool(False)
)
process.commonSequence += process.tightenedMuonsMuscle



# PV selection (no filtering) + PU weighting
import HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex as HChPrimaryVertex
HChPrimaryVertex.addPrimaryVertexSelection(process, process.commonSequence)
import HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisConfiguration as AnalysisConfiguration
dataEras = [
    "Run2011AB",
    "Run2011A",
    "Run2011B",
    ]
puWeights = AnalysisConfiguration.addPuWeightProducers(dataVersion, process, process.commonSequence, dataEras)


# Configuration
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.analysisConfig as analysisConfig
import HiggsAnalysis.HeavyChHiggsToTauNu.Ntuple as Ntuple
ntuple = cms.EDAnalyzer("HPlusMuonNtupleAnalyzer",
    patTriggerEvent = cms.InputTag("patTriggerEvent"),

    genParticleSrc = cms.InputTag("genParticles"),
    genTTBarEnabled = cms.bool(True),

    selectedPrimaryVertexSrc = cms.InputTag("selectedPrimaryVertex"),
    goodPrimaryVertexSrc = cms.InputTag("goodPrimaryVertices"),

    muons = Ntuple.muons.clone(
        src = "tightenedMuons",
        functions = cms.PSet(),
        correctedEnabled = True
        correctedSrc = "tightenedMuonsMuscle",
        tunePEnabled = True,
    ),
    muonEfficiencies = cms.PSet(
        Run2011A = param.embeddingMuonEfficiency.clone(
            mode = "mcEfficiency",
            mcSelect = "Run2011A",
        ),
        Run2011B = param.embeddingMuonEfficiency.clone(
            mode = "mcEfficiency",
            mcSelect = "Run2011B",
        ),
    ),

    jets = Ntuple.jets.clone(
        enabled = False,
    ),

    mets = cms.PSet(),
    doubles = cms.PSet(),
    bools = cms.PSet(),

    eventCounter = param.eventCounter.clone(),
    histogramAmbientLevel = cms.untracked.string("Informative"),
)
for era, weight in zip(dataEras, puWeights):
    setattr(ntuple.doubles, "weightPileup_"+era, cms.InputTag(weight))

HChTools.addAnalysis(process, "muonNtuple", ntuple,
                     preSequence=process.commonSequence,
                     additionalCounters=additionalCounters)
process.muonNtuple.eventCounter.printMainCounter = True

f = open("configDumpEmbeddingDebugMuonAnalysisNtupleAOD.py", "w")
f.write(process.dumpPython())
f.close()
