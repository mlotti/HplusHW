import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

#dataVersion = "44Xdata"
dataVersion = "44XmcS6"

debug = False
#debug = True

PF2PATVersion = "PFlow"

################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)

################################################################################
# Define the process
process = cms.Process("TauEmbeddingAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
#    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    fileNames = cms.untracked.vstring(
#        "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_2_X/TTToHplusBWB_M80_Summer11/TTToHplusBWB_M-80_7TeV-pythia6-tauola/Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v18/8eea754df021b160abed50fa738aa521/pattuple_19_2_514.root"
        "file:/mnt/flustre/wendland/AODSIM_PU_S6_START44_V9B_7TeV/Fall11_TTJets_TuneZ2_7TeV-madgraph-tauola_AODSIM_PU_S6_START44_V9B-v1_testfile.root"
  )
)

options.doPat=1

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
#process.MessageLogger.cerr.FwkReport.reportEvery = 5000
#process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Fragment to run PAT on the fly if requested from command line
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('dummy.root'),
    outputCommands = cms.untracked.vstring(),
)
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion)
del process.out
if options.doPat != 0:
    # Disable the tau pT cut
    process.selectedPatTausPFlow.cut = ""
    process.selectedPatTausPFlowChs.cut = ""

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
#from HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex import addPrimaryVertexSelection
#addPrimaryVertexSelection(process, process.commonSequence)

# Pileup weights
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
param.changeCollectionsToPF2PAT(PF2PATVersion)
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

# Embedding-like preselection
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations
tauEmbeddingCustomisations.PF2PATVersion = PF2PATVersion
if options.doPat != 0:
    # To optimise, perform the generator level preselection before running PAT
    counters = tauEmbeddingCustomisations.addGenuineTauPreselection(process, process.commonSequence, param, pileupWeight="pileupWeight"+puWeights[-1][1])
    process.commonSequence.remove(process.genuineTauPreselectionSequence)
    puModule = getattr(process, "pileupWeight"+puWeights[-1][1])
    process.commonSequence.replace(puModule, puModule*process.genuineTauPreselectionSequence)
    additionalCounters = counters+additionalCounters

additionalCounters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, process.commonSequence, param))

# Add type 1 MET
import HiggsAnalysis.HeavyChHiggsToTauNu.HChMetCorrection as MetCorrection
sequence = MetCorrection.addCorrectedMet(process, param, postfix=PF2PATVersion)
process.commonSequence *= sequence


import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.analysisConfig as analysisConfig
ntuple = cms.EDAnalyzer("HPlusTauNtupleAnalyzer",
    selectedPrimaryVertexSrc = cms.InputTag("selectedPrimaryVertex"),
    goodPrimaryVertexSrc = cms.InputTag("goodPrimaryVertices"),

    tauSrc = cms.InputTag(param.tauSelection.src.value()), # this is set in addEmbeddingLikePreselection()
    tauFunctions = analysisConfig.tauFunctions.clone(),

    jetSrc = cms.InputTag(param.jetSelection.src.value()),
    jetFunctions = analysisConfig.jetFunctions.clone(),

    genParticleSrc = cms.InputTag("genParticles"),
    mets = cms.PSet(
        pfMet_p4 = cms.InputTag("patMETs"+PF2PATVersion),
        pfMetType1_p4 = cms.InputTag(param.MET.type1Src.value()), # Note that this MUST be corrected for the selected tau in the subsequent analysis!
    ),
    doubles = cms.PSet(),
)
for era, name in puWeights:
    setattr(ntuple.doubles, "weightPileup_"+name, cms.InputTag("pileupWeight"+name))

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

addSignalAnalysis = True
if addSignalAnalysis:
    # Run signal analysis module on the same go with the embedding preselection without tau+MET trigger
    import HiggsAnalysis.HeavyChHiggsToTauNu.signalAnalysis as signalAnalysis
    module = signalAnalysis.createEDFilter(param)
    module.Tree.fill = cms.untracked.bool(False)
    module.eventCounter.printMainCounter = cms.untracked.bool(True)

    # Counters
    if len(additionalCounters) > 0:
        module.eventCounter.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in additionalCounters])

    setattr(process, "signalAnalysisTauEmbeddingLikePreselection", module)
    process.signalAnalysisPath = cms.Path(process.commonSequence * module)


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

#f = open("configDump.py", "w")
#f.write(process.dumpPython())
#f.close()
