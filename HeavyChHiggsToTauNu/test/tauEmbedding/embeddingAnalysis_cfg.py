import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion

################################################################################
# Configuration

#dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"
#dataVersion = "38X"
dataVersion = "39Xredigi"

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
    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        #"/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_3_8_X/WJets/WJets_7TeV-madgraph-tauola/Summer10_START36_V9_S09_v1_AODSIM_tauembedding_embedding_v3_3/ed6563e15d1b423a9bd5d11109ca1e30/embedded_RECO_7_1_vMi.root"
        #"/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_3_9_X/DYJetsToLL_TuneZ2_Winter10/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6/a19686e39e81c7cc3074cf9dcfd07453/embedded_RECO_1_1_T59.root"
    #"/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_3_9_X/DYJetsToLL_TuneZ2_Winter10/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6_1_test1/a19686e39e81c7cc3074cf9dcfd07453/embedded_RECO_1_1_8Ag.root"
        #"file:embedded_RECO.root"
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_3_9_X/TTJets_TuneZ2_Winter10/TTJets_TuneZ2_7TeV-madgraph-tauola/Winter10_E7TeV_ProbDist_2010Data_BX156_START39_V8_v1_AODSIM_tauembedding_embedding_v6_1/105b277d7ebabf8cba6c221de6c7ed8a/embedded_RECO_29_1_C97.root"
  )
)
################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
if debug:
    process.MessageLogger.cerr.FwkReport.reportEvery = 1


# Fragment to run PAT on the fly if requested from command line
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion)

# Add configuration information to histograms.root
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import addConfigInfo
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################

#recoProcess = "REDIGI36X"
recoProcess = "REDIGI39X"

# Calculate PF MET for 
from PhysicsTools.PFCandProducer.pfMET_cfi import pfMET
process.pfMETOriginalNoMuon = pfMET.clone(src=cms.InputTag("dimuonsGlobal", "forMixing"))
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
    src = cms.VInputTag(cms.InputTag("genMetCalo", "", recoProcess), cms.InputTag("genMetCalo", "", "EMBEDDINGHLT"))
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
    src = cms.VInputTag(cms.InputTag("genMetCaloAndNonPrompt", "", recoProcess), cms.InputTag("genMetCaloAndNonPrompt", "", "EMBEDDINGHLT"))
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
histoMuonPt = Histo("pt", "pt()", min=0., max=200., nbins=200, description="muon pt (GeV/c)")
histoMuonEta = Histo("eta", "eta()", min=-3, max=3, nbins=60, description="muon eta")

histoTauPt = Histo("pt", "pt()", min=0., max=200., nbins=200, description="tau pt (GeV/c)")
histoTauEta = Histo("eta", "eta()", min=-3, max=3, nbins=60, description="tau eta")

histoMet = Histo("et", "et()", min=0., max=300., nbins=300, description="MET (GeV)")


muons = cms.InputTag("tauEmbeddingMuons")
taus = cms.InputTag("selectedPatTausShrinkingConePFTau")
pfMET = cms.InputTag("pfMet")
pfMETOriginal = cms.InputTag("pfMet", "", "RECO")


counters = []
if dataVersion.isData():
    counters = dataSelectionCounters
analysis = Analysis(process, "analysis", options, additionalCounters=counters)
analysis.getCountAnalyzer().verbose = cms.untracked.bool(True)

selectedTaus = analysis.addSelection("LooseTauId", taus,
                                     "abs(eta) < 2.5 "
                                     "&& leadPFChargedHadrCand().isNonnull() "
                                     "&& tauID('againstMuon') > 0.5 && tauID('againstElectron') > 0.5"
#                                     "&& tauID('byIsolation') > 0.5 && tauID('ecalIsolation') > 0.5"
                                     , selector="PATTauSelector")

selectedTausPt = analysis.addSelection("LooseTauPtId", taus,
                                       "pt > 40"
                                       "&& abs(eta) < 2.5 "
                                       "&& leadPFChargedHadrCand().isNonnull() "
                                       "&& leadPFChargedHadrCand().pt() > 20 "
                                       "&& tauID('againstMuon') > 0.5 && tauID('againstElectron') > 0.5"
#                                       "&& tauID('byIsolation') > 0.5 && tauID('ecalIsolation') > 0.5"
                                       , selector="PATTauSelector")

histoAnalyzer = analysis.addMultiHistoAnalyzer("All", [
        ("muon_", muons, [histoMuonPt, histoMuonEta]),
        ("tau_", selectedTaus, [histoTauPt, histoTauEta]),
        ("pfmet_", pfMET, [histoMet]),
        ("pfmetOriginal_", pfMETOriginal, [histoMet])])

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
        GenMetTrue = cms.untracked.PSet(
            embeddedSrc = cms.untracked.InputTag("genMetTrueEmbedded"),
            originalSrc = cms.untracked.InputTag("genMetTrue", "", recoProcess)
        ),
        GenMetCalo = cms.untracked.PSet(
            embeddedSrc = cms.untracked.InputTag("genMetCaloEmbedded"),
            originalSrc = cms.untracked.InputTag("genMetCalo", "", recoProcess)
        ),
        GenMetCaloAndNonPrompt = cms.untracked.PSet(
            embeddedSrc = cms.untracked.InputTag("genMetCaloAndNonPromptEmbedded"),
            originalSrc = cms.untracked.InputTag("genMetCaloAndNonPrompt", "", recoProcess)
        ),
        GenMetNuSum = cms.untracked.PSet(
            embeddedSrc = cms.untracked.InputTag("genMetNuEmbedded"),
            originalSrc = cms.untracked.InputTag("genMetNuOriginal")
        ),
    ),

    muonTauMatchingCone = cms.untracked.double(0.5),
    metCut = cms.untracked.double(60)
)
process.tauIdEmbeddingAnalyzer = process.EmbeddingAnalyzer.clone(
    tauSrc = cms.untracked.InputTag(selectedTaus.value())
)
process.tauPtIdEmbeddingAnalyzer = process.EmbeddingAnalyzer.clone(
    tauSrc = cms.untracked.InputTag(selectedTausPt.value())
)

#process.analysisSequence = 
process.analysisPath = cms.Path(
    process.commonSequence *
    analysis.getSequence() *
    process.EmbeddingAnalyzer# *
#    process.tauIdEmbeddingAnalyzer *
#    process.tauPtIdEmbeddingAnalyzer
)
