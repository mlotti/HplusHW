import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

#dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"
dataVersion = "38X"
#dataVersion = "data" # this is for collision data 

options = getOptions()
if options.dataVersion != "":
    dataVersion = options.dataVersion

print "Assuming data is ", dataVersion
dataVersion = DataVersion(dataVersion) # convert string to object

process = cms.Process("TauEmbeddingAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    fileNames = cms.untracked.vstring(
        "/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_3_8_X/WJets/WJets_7TeV-madgraph-tauola/Summer10_START36_V9_S09_v1_AODSIM_tauembedding_embedding_v3_2/ed6563e15d1b423a9bd5d11109ca1e30/embedded_RECO_8_1_JTn.root"
        #"file:embedded_RECO.root"
  )
)
options.doPat = 1
################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
#process.MessageLogger.cerr.FwkReport.reportEvery = 1


process.TFileService.fileName = "histograms.root"

from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection import addDataSelection, dataSelectionCounters
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import *
from PhysicsTools.PatAlgos.tools.coreTools import removeSpecificPATObjects, removeCleaning, removeMCMatching
process.patSequence = cms.Sequence()
if options.doPat != 0:
    print "Running PAT on the fly"

    process.out = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string('dummy.root'),
        outputCommands = cms.untracked.vstring()
    )


    process.collisionDataSelection = cms.Sequence()
    if dataVersion.isData():
        process.collisionDataSelection = addDataSelection(process, dataVersion, trigger)

    process.patPlainSequence = addPat(process, dataVersion, doPatTrigger=False, doTauHLTMatching=False,
                                      doPatCalo=False, doBTagging=False, doPatMET=False, doPatElectronID=False)
    process.patSequence = cms.Sequence(
        process.collisionDataSelection *
        process.patPlainSequence
    )
    removeSpecificPATObjects(process, ["Muons", "Electrons", "Photons"], False)
    #removeSpecificPATObjects(process, ["Photons"], False)
    removeCleaning(process, False)

    del process.out

process.configInfo = cms.EDAnalyzer("HPlusConfigInfoAnalyzer")
if options.crossSection >= 0.:
    process.configInfo.crossSection = cms.untracked.double(options.crossSection)
    print "Dataset cross section has been set to %g pb" % options.crossSection
if options.luminosity >= 0:
    process.configInfo.luminosity = cms.untracked.double(options.luminosity)
    print "Dataset integrated luminosity has been set to %g pb^-1" % options.luminosity

process.commonSequence = cms.Sequence(
    process.patSequence +
    process.configInfo
)

################################################################################

# Recalculate gen MET
from RecoMET.Configuration.GenMETParticles_cff import genParticlesForMETAllVisible
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
    src = cms.VInputTag(cms.InputTag("genMetTrueOriginal"), cms.InputTag("genMetTrue", "", "EMBEDDINGHLT"))
)
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
    process.genMetNuOriginal *
    process.genMetNuEmbedded
)

process.commonSequence *= process.genMetSequence

#process.load("HiggsAnalysis.HeavyChHiggsToTauNu.tauEmbedding.printGenParticles_cff")
#process.commonSequence *= process.printGenParticles


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
                                     "&& tauID('byIsolation') > 0.5 && tauID('ecalIsolation') > 0.5",
                                     selector="PATTauSelector")

selectedTausPt = analysis.addSelection("LooseTauPtId", taus,
                                       "pt > 40"
                                       "&& abs(eta) < 2.5 "
                                       "&& leadPFChargedHadrCand().isNonnull() "
                                       "&& leadPFChargedHadrCand().pt() > 20 "
                                       "&& tauID('againstMuon') > 0.5 && tauID('againstElectron') > 0.5"
                                       "&& tauID('byIsolation') > 0.5 && tauID('ecalIsolation') > 0.5",
                                       selector="PATTauSelector")

histoAnalyzer = analysis.addMultiHistoAnalyzer("All", [
        ("muon_", muons, [histoMuonPt, histoMuonEta]),
        ("tau_", selectedTaus, [histoTauPt, histoTauEta]),
        ("pfmet_", pfMET, [histoMet]),
        ("pfmetOriginal_", pfMETOriginal, [histoMet])])

process.EmbeddingAnalyzer = cms.EDAnalyzer("HPlusTauEmbeddingAnalyzer",
    muonSrc = cms.untracked.InputTag(muons.value()),
    tauSrc = cms.untracked.InputTag(taus.value()),
    metSrc = cms.untracked.InputTag(pfMET.value()),
    origMetSrc = cms.untracked.InputTag(pfMETOriginal.value()),
    genMetSrc = cms.untracked.InputTag("genMetTrueEmbedded"),
    origGenMetSrc = cms.untracked.InputTag("genMetTrue", "", "REDIGI36X"),
    nuMetSrc = cms.untracked.InputTag("genMetNuEmbedded"),
    origNuMetSrc = cms.untracked.InputTag("genMetNuOriginal"),
    genParticleSrc = cms.untracked.InputTag("genParticles"),

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
    process.EmbeddingAnalyzer *
    process.tauIdEmbeddingAnalyzer *
    process.tauPtIdEmbeddingAnalyzer
)
