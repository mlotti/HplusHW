import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"
#dataVersion = "data" # this is for collision data 

options = VarParsing.VarParsing()
options.register("runPat",
                 0,
                 options.multiplicity.singleton,
                 options.varType.int,
                 "Run PAT on the fly (needed for RECO/AOD samples)")
options = getOptions(options)
if options.dataVersion != "":
    dataVersion = options.dataVersion

print "Assuming data is ", dataVersion
dataVersion = DataVersion(dataVersion) # convert string to object

process = cms.Process("HChMuonAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
    fileNames = cms.untracked.vstring(
        # For testing in lxplus
        #dataVersion.getAnalysisDefaultFileCastor()
        # For testing in jade
        dataVersion.getAnalysisDefaultFileMadhatter()
  )
)
if options.runPat != 0:
    process.source.fileNames = cms.untracked.vstring(dataVersion.getPatDefaultFileMadhatter(dcap=True))

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.categories.append("EventCounts")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# Uncomment the following in order to print the counters at the end of
# the job (note that if many other modules are being run in the same
# job, their INFO messages are printed too)
#process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")
process.TFileService.fileName = "histograms.root"

from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import *
process.patSequence = cms.Sequence()
if options.runPat != 0:
    print "Running PAT on the fly"
    process.patSequence = addPat(process, dataVersion)


from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *
analysis = Analysis(process, "analysis", options)

relIso = "(isolationR03().emEt+isolationR03().hadEt+isolationR03().sumPt)/pt()"

histosBeginning = [
    Histo("pt", "pt()", min=0., max=200., nbins=200, description="muon pt (GeV/c)"),
    Histo("eta", "eta()", min=-3, max=3, nbins=60, description="muon eta"),
    Histo("relIso", relIso, min=0, max=0.5, nbins=100, description="Relative isolation")
    ]

histosGlobal = histosBeginning+[
    Histo("trackDB", "dB()", min=-2, max=2, nbins=400, description="Track ip @ PV (cm)"),
    Histo("trackNhits", "innerTrack().numberOfValidHits()", min=0, max=60, nbins=60, description="N(valid global hits)"),
    Histo("trackNormChi2", "globalTrack().normalizedChi2()", min=0, max=20, nbins=40, description="Track norm chi2"),
    ]


# References for muon selection:
# https://twiki.cern.ch/twiki/bin/view/CMS/WorkBookPATExampleTopQuarks

muons = cms.InputTag("selectedPatMuons")
jets = cms.InputTag("selectedPatJets")
#jets = cms.InputTag("selectedPatJetsAK5JPT")

# Beginning
histoAnalyzer = analysis.addHistoAnalyzer("AllMuons", muons, histosBeginning)

# Trigger
analysis.addTriggerCut(dataVersion, "HLT_Mu9")
histoAnalyzer = analysis.addCloneHistoAnalyzer("Triggered", histoAnalyzer)

# Tight muon (global + tracker)
selectedMuons = analysis.addCut("GlobalTrackerMuon", muons, "isGlobalMuon() && isTrackerMuon()")
histoAnalyzer = analysis.addHistoAnalyzer("GlobalTrackerMuons", selectedMuons, histosGlobal)
histoAnalyzer.src = selectedMuons

# Kinematical cuts
selectMuons = analysis.addCut("MuonKin", selectedMuons, "pt() > 20 && abs(eta()) < 2.1")
histoAnalyzer = analysis.addCloneHistoAnalyzer("MuonKin", histoAnalyzer)
histoAnalyzer.src = selectedMuons

# Quality cuts
selectedMuons = analysis.addCut("MuonQuality", selectedMuons,
                                "muonID('GlobalMuonPromptTight') && "
                                #"globalTrack().normalizedChi2() < 10.0 && "
                                #"globalTrack().hitPattern().numberOfValidMuonHits () > 0 && "
                                "globalTrack().hitPattern().numberOfValidPixelHits() > 0 && "
                                "innerTrack().numberOfValidHits() > 10 && "
                                "abs(dB()) < 0.2") # currently w.r.t PV! (not beamspot)
histoAnalyzer = analysis.addCloneHistoAnalyzer("MuonQuality", histoAnalyzer)
histoAnalyzer.src = selectedMuons

# Isolation
selectedMuons = analysis.addCut("MuonIsolation", selectedMuons, "%s < 0.15" % relIso)
histoAnalyzer = analysis.addCloneHistoAnalyzer("MuonIsolation", histoAnalyzer)
histoAnalyzer.src = selectedMuons

# Veto against 2nd muon
# vetoMuons = analysis.addCut("MuonVeto", muons,
#                             'isGlobalMuon &&'
#                             'pt > 10. &&'
#                             'abs(eta) < 2.5 &&'
#                             '(trackIso+caloIso)/pt < 0.2',
#                             minNumber=0, maxNumber=0)
# histoAnalyzer = analysis.addCloneHistoAnalyzer("MuonVeto", histoAnalyzer)

# Jet selection
selectedJets = analysis.addCut("JetSelection", jets, "pt() > 30 && abs(eta()) < 2.4")
histoAnalyzer = analysis.addCloneHistoAnalyzer("JetSelection", histoAnalyzer)

process.analysisPath = cms.Path(
    process.patSequence *
    analysis.getSequence()
)
