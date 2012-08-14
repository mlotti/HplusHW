import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

#dataVersion = "44Xdata"
dataVersion = "44XmcS6"

debug = False
#debug = True

################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)

################################################################################
# Define the process
process = cms.Process("TauEmbeddingAnalysis")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
#    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    fileNames = cms.untracked.vstring(
        "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_2_X/TTToHplusBWB_M80_Summer11/TTToHplusBWB_M-80_7TeV-pythia6-tauola/Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v18/8eea754df021b160abed50fa738aa521/pattuple_19_2_514.root"
  )
)
################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
#process.MessageLogger.cerr.FwkReport.reportEvery = 5000
#process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Fragment to run PAT on the fly if requested from command line
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion)

# Add configuration information to histograms.root
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################

# Nu MET                  
#process.genMetNu = cms.EDProducer("HPlusGenMETFromNuProducer",
#    src = cms.InputTag("genParticles")
#)
#process.commonSequence *= process.genMetNu

################################################################################


# Vertex selection
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex import addPrimaryVertexSelection
addPrimaryVertexSelection(process, process.commonSequence)

# Pileup weights
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
puWeights = [
    ("Run2011A", "Run2011A"),
    ("Run2011B", "Run2011B"),
    ("Run2011A+B", "Run2011AB")
    ]
for era, name in puWeights:
    modname = "pileupWeight"+name
    setattr(process, modname, cms.EDProducer("HPlusVertexWeightProducer",
        alias = cms.string(modname),
    ))
    param.setPileupWeight(dataVersion, process=process, commonSequence=process.commonSequence, era=era)
    insertPSetContentsTo(param.vertexWeight.clone(), getattr(process, modname))
    process.commonSequence *= getattr(process, modname)

# Embedding-like preselection
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations
additionalCounters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, process.commonSequence, param))

ntuple = cms.EDAnalyzer("HPlusTauNtupleAnalyzer",
    selectedPrimaryVertexSrc = cms.InputTag("selectedPrimaryVertex"),
    goodPrimaryVertexSrc = cms.InputTag("goodPrimaryVertices"),
    tauSrc = cms.InputTag(param.tauSelection.src.value()), # this is set in addEmbeddingLikePreselection()
    tauFunctions = cms.PSet(),
    jetSrc = cms.InputTag(param.jetSelection.src.value()),
    jetFunctions = cms.PSet(
        tche = cms.string("bDiscriminator('trackCountingHighEffBJetTags')"),
    ),
    genParticleSrc = cms.InputTag("genParticles"),
    mets = cms.PSet(
        pfMet_p4 = cms.InputTag("patMETsPF"),
    ),
    doubles = cms.PSet(),
)
for era, name in puWeights:
    setattr(ntuple.doubles, "weightPileup_"+name, cms.InputTag("pileupWeight"+name))

tauIds = [
    "decayModeFinding",
    "againstMuonLoose", "againstMuonTight", "againstElectronLoose", "againstElectronMedium", "againstElectronTight",
    "byVLooseIsolation", "byLooseIsolation", "byMediumIsolation", "byTightIsolation"
    ]
for name in tauIds:
    setattr(ntuple.tauFunctions, name, cms.string("tauID('%s')"%name))
if dataVersion.isMC():
    ntuple.mets.genMetTrue_p4 = cms.InputTag("genMetTrue")
 #   ntuple.mets.genMetCalo_p4 = cms.InputTag("genMetCalo")
#    ntuple.mets.genMetCaloAndNonPrompt_p4 = cms.InputTag("genMetCaloAndNonPrompt")
#    ntuple.mets.genMetNuSum_4 = cms.InputTag("genMetNu")

addAnalysis(process, "tauNtuple", ntuple,
            preSequence=process.commonSequence,
            additionalCounters=additionalCounters,
            signalAnalysisCounters=False)
process.tauNtupleCounters.printMainCounter = True

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

#f = open("configDump.py", "w")
#f.write(process.dumpPython())
#f.close()
