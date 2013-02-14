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
options, dataVersion = getOptionsDataVersion(dataVersion, useDefaultSignalTrigger=False)
#options.doPat = 1
options.tauEmbeddingInput = 1

if debug:
    print "In debugging mode"

################################################################################
# Define the process
process = cms.Process("TauEmbeddingAnalysis")

if debug:
    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
else:
    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/TTJets_TuneZ2_Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/Tauembedding_embedding_v44_4_seed0_TTJets_TuneZ2_Fall11/e89cb1184437f798b6f9ed400ba3543f/embedded_119_1_LMb.root"
    ),
    inputCommands = cms.untracked.vstring(
        "keep *",
        "drop *_genFilterEfficiencyProducer_*_*" # in lumi
    )
)
if dataVersion.isData():
    process.source.fileNames = [
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_4_X/SingleMu_Mu_160431-163261_2011A_Nov08/SingleMu/Tauembedding_embedding_v44_3_seed0_SingleMu_Mu_160431-163261_2011A_Nov08/8bda05028676a01f201ca340afb9a6ec/embedded_1_1_N9l.root"
        ]

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
if debug:
    process.MessageLogger.cerr.FwkReport.reportEvery = 1


# Fragment to run PAT on the fly if requested from command line
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
patArgs = {
    "doPatTauIsoDeposits": True
}
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, patArgs=patArgs)

# Add configuration information to histograms.root
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addConfigInfo
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################

#recoProcess = "REDIGI36X"
#recoProcess = "REDIGI39X"
#recoProcess = "REDIGI311X"
#recoProcess = "REDIGI311X"
recoProcess = dataVersion.getRecoProcess()
hltProcess = dataVersion.getTriggerProcess()
if dataVersion.isData():
    recoProcess = "RECO"

# Calculate PF MET for 
# FIXME: this is somehow broken ATM
# from CommonTools.ParticleFlow.pfMET_cfi import pfMET
# process.pfMETOriginalNoMuon = pfMET.clone(
#     src = cms.InputTag("dimuonsGlobal", "forMixing"),
#     jets = cms.InputTag("ak5PFJets")
# )
# process.commonSequence *= process.pfMETOriginalNoMuon

# Recalculate gen MET
# True MET
from RecoMET.Configuration.GenMETParticles_cff import genParticlesForMETAllVisible, genCandidatesForMET
process.genParticlesForMETAllVisibleOriginal = genParticlesForMETAllVisible.clone(src=cms.InputTag("genParticles", "", "HLT"))
process.genParticlesForMETAllVisibleOriginalSelected = cms.EDProducer("HPlusGenParticleCleaner",
    src = cms.InputTag("genParticlesForMETAllVisibleOriginal"),
    candSrc = cms.InputTag("tauEmbeddingMuons"),
    maxDeltaR = cms.double(0.2),
    pdgIdsOnly = cms.vint32(13)
)
from RecoMET.METProducers.genMetTrue_cfi import genMetTrue
process.genMetTrueOriginal = genMetTrue.clone(src=cms.InputTag("genParticlesForMETAllVisibleOriginalSelected"))
process.genMetTrueEmbedded = cms.EDProducer("HPlusGenMETSumProducer",
#    src = cms.VInputTag(cms.InputTag("genMetTrue", "", "HLT"), cms.InputTag("genMetTrue", "", "EMBEDDINGHLT"))
    src = cms.VInputTag(cms.InputTag("genMetTrueOriginal"), cms.InputTag("genMetTrue", "", "EMBEDDING"))
)

# Calo MET
#process.genCandidatesForMETOriginal = genCandidatesForMET.clone(src=cms.InputTag("genParticles", "", "HLT"))
#process.genCandidatesForMETOriginalSelected = process.genParticlesForMETAllVisibleOriginalSelected.clone(
#    src = cms.InputTag("genCandidatesForMETOriginal")
#)
#from RecoMET.METProducers.genMetCalo_cfi import genMetCalo
#process.genMetCaloOriginal = genMetCalo.clone(src=cms.InputTag("genCandidatesForMETOriginalSelected"))
process.genMetCaloEmbedded = cms.EDProducer("HPlusGenMETSumProducer",
    src = cms.VInputTag(cms.InputTag("genMetCalo", "", hltProcess), cms.InputTag("genMetCalo", "", "EMBEDDING"))
#    src = cms.VInputTag(cms.InputTag("genMetCaloOriginal"), cms.InputTag("genMetCalo", "", "EMBEDDINGHLT"))
)                                            

# CaloAndNonPromt MET
#from RecoJets.Configuration.GenJetParticles_cff import genParticlesForJetsNoMuNoNu
#process.genParticlesForJetsNoMuNoNuOriginal = genParticlesForJetsNoMuNoNu.clone(src=cms.InputTag("genParticles", "", "HLT"))
#process.genParticlesForJetsNoMuNoNuOriginalSelected = process.genParticlesForMETAllVisibleOriginalSelected.clone(
#    src = cms.InputTag("genParticlesForJetsNoMuNoNuOriginal")
#)
#from RecoMET.METProducers.genMetCaloAndNonPrompt_cfi import genMetCaloAndNonPrompt
#process.genMetCaloAndNonPromptOriginal = genMetCaloAndNonPrompt.clone(src=cms.InputTag("genParticlesForJetsNoMuNoNuOriginalSelected"))
process.genMetCaloAndNonPromptEmbedded = cms.EDProducer("HPlusGenMETSumProducer",
    src = cms.VInputTag(cms.InputTag("genMetCaloAndNonPrompt", "", hltProcess), cms.InputTag("genMetCaloAndNonPrompt", "", "EMBEDDING"))
#    src = cms.VInputTag(cms.InputTag("genMetCaloAndNonPromptOriginal"), cms.InputTag("genMetCaloAndNonPrompt", "", "EMBEDDINGHLT"))
)


# Nu MET                  
process.genMetNuOriginal = cms.EDProducer("HPlusGenMETFromNuProducer",
    src = cms.InputTag("genParticles", "", "HLT")
)
process.genMetNuEmbedded = cms.EDProducer("HPlusGenMETFromNuProducer",
    src = cms.InputTag("genParticles", "", "HLT"),
    embeddedSrc = cms.InputTag("genParticles", "", "EMBEDDING")
)
process.genMetSequence = cms.Sequence(
    process.genParticlesForMETAllVisibleOriginal *
    process.genParticlesForMETAllVisibleOriginalSelected *
    process.genMetTrueOriginal *
    process.genMetTrueEmbedded *

#    process.genCandidatesForMETOriginal *
#    process.genCandidatesForMETOriginalSelected *
#    process.genMetCaloOriginal *
    process.genMetCaloEmbedded *

#    process.genParticlesForJetsNoMuNoNuOriginal *
#    process.genParticlesForJetsNoMuNoNuOriginalSelected *
#    process.genMetCaloAndNonPromptOriginal *
    process.genMetCaloAndNonPromptEmbedded *

    process.genMetNuOriginal *
    process.genMetNuEmbedded
)

if False and dataVersion.isMC(): # FIXME
    process.commonSequence *= process.genMetSequence


# Select PFCands in 0.1 cone
process.selectedPFCands = cms.EDProducer("HPlusPFCandCandViewDeltaRSelector",
    src = cms.InputTag("particleFlow"),
    refSrc = cms.InputTag("tauEmbeddingMuons"),
    deltaR = cms.double(0.1)
)
process.selectedPFCandsORG = process.selectedPFCands.clone(
    src = cms.InputTag("particleFlowORG")
)

#process.commonSequence *= process.selectedPFCands
#process.commonSequence *= process.selectedPFCandsORG


if debug:
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.printGenParticles_cff")
    process.commonSequence *= process.printGenParticles


################################################################################


from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *

# Vertex selection
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex import addPrimaryVertexSelection
addPrimaryVertexSelection(process, process.commonSequence)

# Pileup weights
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
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

# Switch to PF2PAT objects
#PF2PATVersion = "PFlow"
#param.changeCollectionsToPF2PAT(postfix=PF2PATVersion)

muons = cms.InputTag("tauEmbeddingMuons")
#taus = cms.InputTag("selectedPatTausShrinkingConePFTau")
taus = cms.InputTag("selectedPatTausHpsPFTau")
pfMET = cms.InputTag("pfMet")
pfMETOriginal = cms.InputTag("pfMet", "", recoProcess)

# Finalise muon selection
process.firstPrimaryVertex = cms.EDProducer("HPlusFirstVertexSelector",
    src = cms.InputTag("offlinePrimaryVertices")
)
process.commonSequence *= process.firstPrimaryVertex

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
# FIXME: hack to apply trigger in MC
#if dataVersion.isMC():
#    additionalCounters.extend(tauEmbeddingCustomisations.addMuonTriggerFix(process, dataVersion, process.commonSequence, options))
param.setAllTauSelectionSrcSelectedPatTausTriggerMatched()
tauEmbeddingCustomisations.customiseParamForTauEmbedding(param, options, dataVersion)

#tauEmbeddingCustomisations.PF2PATVersion = PF2PATVersion
#muons = cms.InputTag(tauEmbeddingCustomisations.addMuonIsolationEmbedding(process, process.commonSequence, muons.value()))
additionalCounters.extend(tauEmbeddingCustomisations.addFinalMuonSelection(process, process.commonSequence, param, enableIsolation=False))
#taus = cms.InputTag("patTaus"+PF2PATVersion+"TauEmbeddingMuonMatched")
#taus = cms.InputTag("patTaus"+PF2PATVersion+"TauEmbeddingMuonMatched")
taus = cms.InputTag(param.tauSelectionHPSMediumTauBased.src.value())


import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.analysisConfig as analysisConfig
ntuple = cms.EDAnalyzer("HPlusTauEmbeddingNtupleAnalyzer",
    histogramAmbientLevel = cms.untracked.string("Vital"),
    selectedPrimaryVertexSrc = cms.InputTag("selectedPrimaryVertex"),
    goodPrimaryVertexSrc = cms.InputTag("goodPrimaryVertices"),

    patTriggerSrc = cms.InputTag("patTriggerEvent"),
    triggerPaths = cms.PSet(
        IsoMu12 = cms.vstring("HLT_IsoMu12_v1"),
        IsoMu17 = cms.vstring("HLT_IsoMu17_v6", "HLT_IsoMu17_v8"),
        IsoMu24 = cms.vstring("HLT_IsoMu24_v5", "HLT_IsoMu24_v6", "HLT_IsoMu24_v7", "HLT_IsoMu24_v8"),
        IsoMu30_eta2p1 = cms.vstring("HLT_IsoMu30_eta2p1_v3", "HLT_IsoMu30_eta2p1_v6", "HLT_IsoMu30_eta2p1_v7"),
    
        Mu20 = cms.vstring("HLT_Mu20_v1"),
        Mu24 = cms.vstring("HLT_Mu24_v2"),
        Mu30 = cms.vstring("HLT_Mu30_v3"),
        Mu40 = cms.vstring("HLT_Mu40_v1", "HLT_Mu40_v2", "HLT_Mu40_v3", "HLT_Mu40_v5"),
        Mu40_eta2p1 = cms.vstring("HLT_Mu40_eta2p1_v1", "HLT_Mu40_eta2p1_v4", "HLT_Mu40_eta2p1_v5"),
    ),

    muonSrc = cms.InputTag(muons.value()),
    muonFunctions = analysisConfig.muonFunctions.clone(),
    embeddingMuonEfficiency = param.embeddingMuonEfficiency.clone(
        mode = "efficiency"
    ),

#    electronSrc = cms.InputTag("selectedPatElectrons"),
#    electronConversionSrc = cms.InputTag("allConversions"),
#    beamspotSrc = cms.InputTag("offlineBeamSpot"),
#    electronRhoSrc =  cms.InputTag("kt6PFJetsForEleIso", "rho"),
#    electronFunctions = analysisConfig.electronFunctions.clone(),

    tauSrc = cms.InputTag(taus.value()),
    tauFunctions = analysisConfig.tauFunctions.clone(),

#    jetSrc = cms.InputTag("selectedPatJets"),
#    jetFunctions = analysisConfig.jetFunctions.clone(),

    genParticleOriginalSrc = cms.InputTag("genParticles", "", "HLT"),
    genParticleEmbeddedSrc = cms.InputTag("genParticles"),
    mets = cms.PSet(
        pfMet_p4 = cms.InputTag(pfMET.value()),
        pfMetOriginal_p4 = cms.InputTag(pfMETOriginal.value()),
#        pfMetOriginalNoMuon_p4 = cms.InputTag("pfMETOriginalNoMuon"), # FIXME: broken ATM
    ),
    doubles = cms.PSet(),
    bools = cms.PSet()
)


if False and dataVersion.isMC(): # FIXME
    ntuple.mets.genMetTrueEmbedded_p4 = cms.InputTag("genMetTrueEmbedded")
    ntuple.mets.genMetTrueOriginal_p4 = cms.InputTag("genMetTrue", "", hltProcess)
    ntuple.mets.genMetCaloEmbedded_p4 = cms.InputTag("genMetCaloEmbedded")
    ntuple.mets.genMetCaloOriginal_p4 = cms.InputTag("genMetCalo", "", hltProcess)
    ntuple.mets.genMetCaloAndNonPromptEmbedded_p4 = cms.InputTag("genMetCaloAndNonPromptEmbedded")
    ntuple.mets.genMetCaloAndNonPromptOriginal_p4 = cms.InputTag("genMetCaloAndNonPrompt", "", hltProcess)
    ntuple.mets.genMetNuSumEmbedded_p4 = cms.InputTag("genMetNuEmbedded")
    ntuple.mets.genMetNuSumOriginal_p4 = cms.InputTag("genMetNuOriginal")
for era, name in puWeights:
    setattr(ntuple.doubles, "weightPileup_"+name, cms.InputTag("pileupWeight"+name))

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
    weightSrc = cms.InputTag("pileupWeight"+puWeights[-1][1])
)
for label in eventCounters:
    process.globalReplace(label, prototype.clone())


#f = open("configDumpEmbeddingAnalysis.py", "w")
#f.write(process.dumpPython())
#f.close()
