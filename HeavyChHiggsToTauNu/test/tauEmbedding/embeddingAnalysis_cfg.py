import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

#dataVersion = "42Xdata"
dataVersion = "42Xmc"

debug = False
#debug = True

################################################################################

# Command line arguments (options) and DataVersion object
options, dataVersion = getOptionsDataVersion(dataVersion)
options.doPat = 1
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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
    #"/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_1_X/TTJets_TuneZ2_Spring11/TTJets_TuneZ2_7TeV-madgraph-tauola/Spring11_PU_S1_START311_V1G1_v1_AODSIM_tauembedding_embedding_v10_1_pt40/ac95b0c9ecfd651039bbe079053aed03/embedded_RECO_16_1_JtV.root"
    "root://madhatter.csc.fi:1094/pnfs/csc.fi/data/cms/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_1_X/TTJets_TuneZ2_Summer11/TTJets_TuneZ2_7TeV-madgraph-tauola/Summer11_PU_S4_START42_V11_v1_AODSIM_tauembedding_embedding_v11_6_pt40/af0b4aa82477426f47ec012132b67081/embedded_RECO_3_1_58j.root"
  )
)
if dataVersion.isData():
    process.source.fileNames = [
        #"/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_4_1_X/SingleMu_163270-163869_Prompt/SingleMu/Run2011A_PromptReco_v2_AOD_163270_tauembedding_embedding_v10_1_pt40/cee94be795a40bbb5b546b09a0917318/embedded_RECO_2_1_5GD.root"
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
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, plainPatArgs=patArgs)

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
from CommonTools.ParticleFlow.pfMET_cfi import pfMET
process.pfMETOriginalNoMuon = pfMET.clone(
    src = cms.InputTag("dimuonsGlobal", "forMixing"),
    jets = cms.InputTag("ak5PFJets")
)
process.commonSequence *= process.pfMETOriginalNoMuon

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
    src = cms.VInputTag(cms.InputTag("genMetTrueOriginal"), cms.InputTag("genMetTrue", "", "EMBEDDINGHLT"))
)

# Calo MET
#process.genCandidatesForMETOriginal = genCandidatesForMET.clone(src=cms.InputTag("genParticles", "", "HLT"))
#process.genCandidatesForMETOriginalSelected = process.genParticlesForMETAllVisibleOriginalSelected.clone(
#    src = cms.InputTag("genCandidatesForMETOriginal")
#)
#from RecoMET.METProducers.genMetCalo_cfi import genMetCalo
#process.genMetCaloOriginal = genMetCalo.clone(src=cms.InputTag("genCandidatesForMETOriginalSelected"))
process.genMetCaloEmbedded = cms.EDProducer("HPlusGenMETSumProducer",
    src = cms.VInputTag(cms.InputTag("genMetCalo", "", hltProcess), cms.InputTag("genMetCalo", "", "EMBEDDINGHLT"))
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
    src = cms.VInputTag(cms.InputTag("genMetCaloAndNonPrompt", "", hltProcess), cms.InputTag("genMetCaloAndNonPrompt", "", "EMBEDDINGHLT"))
#    src = cms.VInputTag(cms.InputTag("genMetCaloAndNonPromptOriginal"), cms.InputTag("genMetCaloAndNonPrompt", "", "EMBEDDINGHLT"))
)


# Nu MET                  
process.genMetNuOriginal = cms.EDProducer("HPlusGenMETFromNuProducer",
    src = cms.InputTag("genParticles", "", "HLT")
)
process.genMetNuEmbedded = cms.EDProducer("HPlusGenMETFromNuProducer",
    src = cms.InputTag("genParticles", "", "HLT"),
    embeddedSrc = cms.InputTag("genParticles", "", "EMBEDDINGHLT")
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

if dataVersion.isMC():
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

process.commonSequence *= process.selectedPFCands
process.commonSequence *= process.selectedPFCandsORG


if debug:
    process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.printGenParticles_cff")
    process.commonSequence *= process.printGenParticles


################################################################################


from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *

# Pileup weighting
weight = None
# weighting not possible with tauAnalysis (necessary collection missing from tauAnalysis)
# if dataVersion.isMC():
#     import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as params
#     params.setPileupWeightFor2010()
#     params.setPileupWeightFor2011()
#     params.setPileupWeightFor2010and2011()
#     process.pileupWeight = cms.EDProducer("HPlusVertexWeightProducer",
#         alias = cms.string("pileupWeight")
#     )
#     insertPSetContentsTo(params.vertexWeight, process.pileupWeight)
#     process.commonSequence *= process.pileupWeight
#     weight = "pileupWeight"


histoMuonPt = Histo("pt", "pt()", min=0., max=200., nbins=200, description="muon pt (GeV/c)")
histoMuonEta = Histo("eta", "eta()", min=-3, max=3, nbins=60, description="muon eta")

histoTauPt = Histo("pt", "pt()", min=0., max=200., nbins=200, description="tau pt (GeV/c)")
histoTauEta = Histo("eta", "eta()", min=-3, max=3, nbins=60, description="tau eta")

histoMet = Histo("et", "et()", min=0., max=300., nbins=300, description="MET (GeV)")


muons = cms.InputTag("tauEmbeddingMuons")
#taus = cms.InputTag("selectedPatTausShrinkingConePFTau")
taus = cms.InputTag("selectedPatTausHpsPFTau")
pfMET = cms.InputTag("pfMet")
pfMETOriginal = cms.InputTag("pfMet", "", recoProcess)

# Finalise muon selection
process.firstPrimaryVertex = cms.EDProducer("HPlusSelectFirstVertex",
    src = cms.InputTag("offlinePrimaryVertices")
)
process.commonSequence *= process.firstPrimaryVertex

import HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.customisations as tauEmbeddingCustomisations
import HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff as param
muons = cms.InputTag(tauEmbeddingCustomisations.addMuonIsolationEmbedding(process, process.commonSequence, muons.value()))
additionalCounters.extend(tauEmbeddingCustomisations.addFinalMuonSelection(process, process.commonSequence, param))


analysis = Analysis(process, "analysis", additionalCounters=additionalCounters, weightSrc=weight)
analysis.getCountAnalyzer().verbose = cms.untracked.bool(True)

selectedTaus = analysis.addSelection("LooseTauId", taus,
                                     "abs(eta) < 2.5 "
                                     "&& leadPFChargedHadrCand().isNonnull() "
                                     "&& tauID('againstMuonLoose') > 0.5 && tauID('againstElectronLoose') > 0.5"
#                                     "&& tauID('byIsolation') > 0.5 && tauID('ecalIsolation') > 0.5"
                                     , selector="PATTauSelector")

selectedTausPt = analysis.addSelection("LooseTauPtId", taus,
                                       "pt > 40"
                                       "&& abs(eta) < 2.5 "
                                       "&& leadPFChargedHadrCand().isNonnull() "
                                       "&& leadPFChargedHadrCand().pt() > 20 "
                                       "&& tauID('againstMuonLoose') > 0.5 && tauID('againstElectronLoose') > 0.5"
#                                       "&& tauID('byIsolation') > 0.5 && tauID('ecalIsolation') > 0.5"
                                       , selector="PATTauSelector")

histoAnalyzer = analysis.addMultiHistoAnalyzer("All", [
        ("muon_", muons, [histoMuonPt, histoMuonEta]),
        ("tau_", selectedTaus, [histoTauPt, histoTauEta]),
        ("pfmet_", pfMET, [histoMet]),
        ("pfmetOriginal_", pfMETOriginal, [histoMet])])

process.tauSelectionSequence = analysis.getSequence()
process.commonSequence *= process.tauSelectionSequence


# Embedding analyzer
process.EmbeddingAnalyzer = cms.EDAnalyzer("HPlusTauEmbeddingAnalyzer",
    muonSrc = cms.untracked.InputTag(muons.value()),
    tauSrc = cms.untracked.InputTag(taus.value()),
    pfCandSrc = cms.untracked.InputTag("particleFlowORG"),
#    pfCandSrc = cms.untracked.InputTag("selectedPFCands"),
    vertexSrc = cms.untracked.InputTag("offlinePrimaryVertices"),
    genParticleOriginalSrc = cms.untracked.InputTag("genParticles", "", "HLT"),
    genParticleEmbeddedSrc = cms.untracked.InputTag("genParticles"),
    visibleTauSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauOneAndThreeProng"),
#    visibleTauSrc = cms.untracked.InputTag("VisibleTaus", "HadronicTauOneProng"),
    mets = cms.untracked.PSet(
        Met = cms.untracked.PSet(
            embeddedSrc = cms.untracked.InputTag(pfMET.value()),
            originalSrc = cms.untracked.InputTag(pfMETOriginal.value())
        ),
        MetNoMuon = cms.untracked.PSet(
            embeddedSrc = cms.untracked.InputTag(pfMET.value()),
            originalSrc = cms.untracked.InputTag("pfMETOriginalNoMuon")
        ),
    ),

    muonTauMatchingCone = cms.untracked.double(0.5),
    metCut = cms.untracked.double(60),
    tauIsolationCalculator = cms.untracked.PSet(
        vertexSrc = cms.InputTag("offlinePrimaryVertices")
    )
)
if weight != None:
    process.EmbeddingAnalyzer.prescaleSource = cms.untracked.InputTag(weight)


# if dataVersion.isMC():
#     process.EmbeddingAnalyzer.GenMetTrue = cms.untracked.PSet(
#         embeddedSrc = cms.untracked.InputTag("genMetTrueEmbedded"),
#         originalSrc = cms.untracked.InputTag("genMetTrue", "", recoProcess)
#     )
#     process.EmbeddingAnalyzer.GenMetCalo = cms.untracked.PSet(
#         embeddedSrc = cms.untracked.InputTag("genMetCaloEmbedded"),
#         originalSrc = cms.untracked.InputTag("genMetCalo", "", recoProcess)
#     )
#     process.EmbeddingAnalyzer.GenMetCaloAndNonPrompt = cms.untracked.PSet(
#         embeddedSrc = cms.untracked.InputTag("genMetCaloAndNonPromptEmbedded"),
#         originalSrc = cms.untracked.InputTag("genMetCaloAndNonPrompt", "", recoProcess)
#     )
#     process.EmbeddingAnalyzer.GenMetNuSum = cms.untracked.PSet(
#          embeddedSrc = cms.untracked.InputTag("genMetNuEmbedded"),
#          originalSrc = cms.untracked.InputTag("genMetNuOriginal")
#     )

process.tauIdEmbeddingAnalyzer = process.EmbeddingAnalyzer.clone(
    tauSrc = cms.untracked.InputTag(selectedTaus.value())
)
process.tauPtIdEmbeddingAnalyzer = process.EmbeddingAnalyzer.clone(
    tauSrc = cms.untracked.InputTag(selectedTausPt.value())
)

#process.analysisSequence = 
process.analysisPath = cms.Path(
    process.commonSequence *
    process.EmbeddingAnalyzer# *
#    process.tauIdEmbeddingAnalyzer *
#    process.tauPtIdEmbeddingAnalyzer
)

# def _setMuon(module, muonSrc):
#     module.muonSrc = cms.untracked.InputTag(muonSrc)

# tauEmbeddingCustomisations.addMuonIsolationAnalyses(process, "EmbeddingAnalyzer", process.EmbeddingAnalyzer,
#                                                     process.commonSequence, [],
#                                                     modify=_setMuon, signalAnalysisCounters=False)
