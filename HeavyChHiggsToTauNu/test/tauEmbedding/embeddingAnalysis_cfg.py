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

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(50) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    fileNames = cms.untracked.vstring(
        #"/store/group/local/HiggsChToTauNuFullyHadronic/tauembedding/CMSSW_3_8_X/WJets/WJets_7TeV-madgraph-tauola/local_local_Summer10_START36_V9_S09_v1_AODSIM_tauembedding_skim_v2_52e54222a22093cabccf53a197393901_USER_tauembedding_generation_v2_30de4d1810b82a43ef34b86cea04d93e_USER_tauembedding_embedding_v2/ed6563e15d1b423a9bd5d11109ca1e30/embedded_RECO_2_1_fTj.root",
        "file:embedded_RECO.root"
  )
)
options.doPat = 1
################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000


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

from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *
histoMuonPt = Histo("pt", "pt()", min=0., max=200., nbins=200, description="muon pt (GeV/c)")
histoMuonEta = Histo("eta", "eta()", min=-3, max=3, nbins=60, description="muon eta")

histoTauPt = Histo("pt", "pt()", min=0., max=200., nbins=200, description="tau pt (GeV/c)")
histoTauEta = Histo("eta", "eta()", min=-3, max=3, nbins=60, description="tau eta")

histoMet = Histo("et", "et()", min=0., max=300., nbins=300, description="MET (GeV)")


muons = cms.InputTag("tightMuons")
taus = cms.InputTag("selectedPatTaus")
pfMET = cms.InputTag("pfMet")
pfMETOriginal = cms.InputTag("pfMet", "", "RECO")


counters = []
if dataVersion.isData():
    counters = dataSelectionCounters
analysis = Analysis(process, "analysis", options, additionalCounters=counters)
analysis.getCountAnalyzer().verbose = cms.untracked.bool(True)

histoAnalyzer = analysis.addMultiHistoAnalyzer("All", [
        ("muon_", muons, [histoMuonPt, histoMuonEta]),
        ("tau_", taus, [histoTauPt, histoTauEta]),
        ("pfmet_", pfMET, [histoMet]),
        ("pfmetOriginal_", pfMETOriginal, [histoMet])])

process.embeddingAnalyzer = cms.EDAnalyzer("HPlusTauEmbeddingAnalyzer",
    muonSrc = cms.untracked.InputTag(muons.value()),
    tauSrc = cms.untracked.InputTag(taus.value()),
    metSrc = cms.untracked.InputTag(pfMET.value()),
    origMetSrc = cms.untracked.InputTag(pfMETOriginal.value())
)

#process.analysisSequence = 
process.analysisPath = cms.Path(
    process.commonSequence *
    analysis.getSequence() *
    process.embeddingAnalyzer
)
