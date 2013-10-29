import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

#dataVersion = "44Xdata"
dataVersion = "44XmcS6"

debug = False
#debug = True

#PF2PATVersion = "PFlow"

################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)

################################################################################
# Define the process
process = cms.Process("TauEmbeddingAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(5000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
#    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    fileNames = cms.untracked.vstring(
#        "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_2_X/TTToHplusBWB_M80_Summer11/TTToHplusBWB_M-80_7TeV-pythia6-tauola/Summer11_PU_S4_START42_V11_v1_AODSIM_pattuple_v18/8eea754df021b160abed50fa738aa521/pattuple_19_2_514.root"
#        "file:/mnt/flustre/wendland/AODSIM_PU_S6_START44_V9B_7TeV/Fall11_TTJets_TuneZ2_7TeV-madgraph-tauola_AODSIM_PU_S6_START44_V9B-v1_testfile.root"
#e        "file:/mnt/flustre/mkortela/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11-PU_S6_START44_V9B-v1/AODSIM/82A96ABF-C736-E111-8E5D-0030486790C0.root" # has lumi 255000, which induces a bug
#    "file:/home/mkortela/hplus/pat/CMSSW_4_4_5/src/HiggsAnalysis/HeavyChHiggsToTauNu/test/tauEmbedding/multicrab_genTauSkim_v44_5_130409_115103/pattuple.root"

        "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_tauembedding_gentauskim_v44_5/9ecb3a23e436fc2ffd8a803eac2a3a15/pattuple_1012_1_LSv.root",
#        "file:pattuple_1012_1_LSv.root",
#        "/store/group/local/HiggsChToTauNuFullyHadronic/pattuples/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Fall11_PU_S6_START44_V9B_v1_AODSIM_tauembedding_gentauskim_v44_5/9ecb3a23e436fc2ffd8a803eac2a3a15/pattuple_1011_1_OBr.root",
    ),
#    lumisToProcess = cms.untracked.VLuminosityBlockRange("1:255000"),
#    eventsToProcess = cms.untracked.VEventRange("1:255000:76484768"),
)

#options.doPat=1

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
    process.selectedPatTausHpsPFTau.cut = ""
#    process.selectedPatTausPFlow.cut = ""
#    process.selectedPatTausPFlowChs.cut = ""

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
import HiggsAnalysis.HeavyChHiggsToTauNu.AnalysisConfiguration as AnalysisConfiguration
dataEras = [
    "Run2011AB", 
    "Run2011A",
    "Run2011B",
    ]
firstPuWeight = None
if dataVersion.isMC():
    puEraSuffixWeights = AnalysisConfiguration.addPuWeightProducersVariations(dataVersion, process, process.commonSequence, dataEras)
    if options.wjetsWeighting != 0:
        raise Exception("This configuration does not support W+jets weighting (yet)")
    firstPuWeight = puEraSuffixWeights[0][2]

# Embedding-like preselection
import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations
#tauEmbeddingCustomisations.PF2PATVersion = PF2PATVersion
if options.doPat == 0:
    import HiggsAnalysis.HeavyChHiggsToTauNu.CustomGenTauSkim as tauSkim
    additionalCounters = tauSkim.getCounters() + additionalCounters
else:
    # To optimise, perform the generator level preselection before running PAT
    counters = tauEmbeddingCustomisations.addGenuineTauPreselection(process, process.commonSequence, param, pileupWeight=firstPuWeight)
    process.commonSequence.remove(process.genuineTauPreselectionSequence)
    puModule = getattr(process, firstPuWeight)
    process.commonSequence.replace(puModule, puModule*process.genuineTauPreselectionSequence)
    additionalCounters = counters+additionalCounters

process.preselectionSequence = cms.Sequence()
preselectionCounters = additionalCounters[:]
preselectionCounters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, process.preselectionSequence, param, pileupWeight=firstPuWeight,
                                                                                    selectOnlyFirstGenTau=True,
                                                                                    ))

# Add type 1 MET
#import HiggsAnalysis.HeavyChHiggsToTauNu.HChMetCorrection as MetCorrection
#sequence = MetCorrection.addCorrectedMet(process, param, postfix=PF2PATVersion)
#process.commonSequence *= sequence


import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.analysisConfig as analysisConfig
import HiggsAnalysis.HeavyChHiggsToTauNu.Ntuple as Ntuple
ntuple = cms.EDAnalyzer("HPlusTauNtupleAnalyzer",
    eventCounter = param.eventCounter.clone(),
    histogramAmbientLevel = cms.untracked.string("Vital"),
    selectedPrimaryVertexSrc = cms.InputTag("selectedPrimaryVertex"),
    goodPrimaryVertexSrc = cms.InputTag("goodPrimaryVertices"),

    patTriggerSrc = cms.InputTag("patTriggerEvent"),
    triggerPaths = cms.PSet(
        MediumIsoPFTau35_Trk20_MET60 = cms.vstring("HLT_MediumIsoPFTau35_Trk20_MET60_v1"),
    ),

    tauEnabled = cms.bool(True),
    tauSrc = cms.InputTag(param.tauSelection.src.value()), # this is set in addEmbeddingLikePreselection()
    tauFunctions = analysisConfig.tauFunctions.clone(),

    jets = Ntuple.jets.clone(
#        src = param.jetSelection.src.value(),
        src = "embeddingLikePreselectionCleanedJets",
        functions = analysisConfig.jetFunctions.clone(),
        pileupIDs = analysisConfig.jetPileupIDs.clone(),
    ),

    muons = Ntuple.muons.clone(enabled=False, src="NOT_SET"),

    genParticleSrc = cms.InputTag("genParticles"),
# For tau MC matching, use the same collection which was used in preselection
    genParticleTauSrc = cms.InputTag("embeddingLikePreselectionGenTau"),
    genTTBarEnabled = cms.bool(True),

    mets = cms.PSet(
#        pfMet_p4 = cms.InputTag("patMETs"+PF2PATVersion),
        pfMet_p4 = cms.InputTag(param.MET.rawSrc.value()),
        pfMetType1_p4 = cms.InputTag(param.MET.type1Src.value()), # Note that this MUST be corrected for the selected tau in the subsequent analysis!
        pfMetType2_p4 = cms.InputTag(param.MET.type2Src.value())
    ),
    doubles = cms.PSet(),
)
if dataVersion.isMC():
    for era, suffix, weight in puEraSuffixWeights:
        setattr(ntuple.doubles, "weightPileup_"+era+suffix, cms.InputTag(weight))

    ntuple.mets.genMetTrue_p4 = cms.InputTag("genMetTrue")
 #   ntuple.mets.genMetCalo_p4 = cms.InputTag("genMetCalo")
#    ntuple.mets.genMetCaloAndNonPrompt_p4 = cms.InputTag("genMetCaloAndNonPrompt")
#    ntuple.mets.genMetNuSum_4 = cms.InputTag("genMetNu")

process.preselectionSequence.insert(0, process.commonSequence)
addAnalysis(process, "tauNtuple", ntuple,
            preSequence=process.preselectionSequence,
            additionalCounters=preselectionCounters,
            signalAnalysisCounters=True)
process.tauNtuple.eventCounter.printMainCounter = True

addSignalAnalysis = True
if addSignalAnalysis:
    # Run signal analysis module on the same go with the embedding preselection without tau+MET trigger
    import HiggsAnalysis.HeavyChHiggsToTauNu.signalAnalysis as signalAnalysis
    module = signalAnalysis.createEDFilter(param)
    param.setJetPUIdSrc(module.jetSelection, "")
    module.Tree.fill = cms.untracked.bool(False)
    module.histogramAmbientLevel = "Vital"

    # Counters
    if len(preselectionCounters) > 0:
        module.eventCounter.counters = cms.untracked.VInputTag([cms.InputTag(c) for c in preselectionCounters])

    def addModule(mod, postfix="", sequence=None):
        for era, suffix, src in puEraSuffixWeights:
            m = mod.clone()
            m.pileupWeightReader.weightSrc = src
            if era == dataEras[0] and suffix == "":
                m.eventCounter.printMainCounter = cms.untracked.bool(True)
            if suffix != "":
                m.histogramAmbientLevel = "Systematics"

            setattr(process, "signalAnalysisTauEmbeddingLikePreselection"+postfix+era+suffix, m)
            p = cms.Path(process.preselectionSequence)
            if sequence is not None:
                p += sequence
            p += m
            setattr(process, "signalAnalysis"+postfix+era+suffix+"Path", p)

    # Nominal
    addModule(module)

    # Add sequence for exactly one gen tau
    # mod = module.clone()
    # process.oneGenTau40Sequence = cms.Sequence()
    # oneGenTau40Counters = preselectionCounters[:]
    # oneGenTau40Counters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, process.oneGenTau40Sequence, mod, pileupWeight=firstPuWeight,
    #                                                                                    prefix="embeddingLikePresectionOneGenTau40", maxGenTaus=1))
    # mod.eventCounter.counters = [cms.InputTag(c) for c in oneGenTau40Counters]
    # addModule(mod, "OneGenTau40", process.oneGenTau40Sequence)

    # Add sequence for generator tau pt>41 selection
    # mod = module.clone()
    # process.genTau41Sequence = cms.Sequence()
    # genTau41Counters = preselectionCounters[:]
    # tauEmbeddingCustomisations.generatorTauPt = 41
    # genTau41Counters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, process.genTau41Sequence, mod, pileupWeight=firstPuWeight,
    #                                                                                 prefix="embeddingLikePreselectionGenTau41"))
    # mod.eventCounter.counters = [cms.InputTag(c) for c in genTau41Counters]
    # addModule(mod, "GenTau41", process.genTau41Sequence)

    # Add sequence for exactly one generator tau pt>41 selection
    mod = module.clone()
    process.oneGenTau41Sequence = cms.Sequence()
    oneGenTau41Counters = preselectionCounters[:]
    oneGenTau41Counters.extend(tauEmbeddingCustomisations.addEmbeddingLikePreselection(process, process.oneGenTau41Sequence, mod, pileupWeight=firstPuWeight,
                                                                                       prefix="embeddingLikePreselectionOneGenTau41", maxGenTaus=1))
    mod.eventCounter.counters = [cms.InputTag(c) for c in oneGenTau41Counters]
    addModule(mod, "OneGenTau41", process.oneGenTau41Sequence)

# Replace all event counters with the weighted one
eventCounters = []
for label, module in process.producers_().iteritems():
    if module.type_() == "EventCountProducer":
        eventCounters.append(label)
prototype = cms.EDProducer("HPlusEventCountProducer",
    weightSrc = cms.InputTag(firstPuWeight)
)
for label in eventCounters:
    process.globalReplace(label, prototype.clone())

f = open("configDumpTauAnalysis.py", "w")
f.write(process.dumpPython())
f.close()
