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
if options.doPat != 0:
    process.source.fileNames = cms.untracked.vstring(
        #dataVersion.getPatDefaultFileCastor()
        dataVersion.getPatDefaultFileMadhatter(dcap=True)
    )

################################################################################

# References for muon selection:
# https://twiki.cern.ch/twiki/bin/view/CMS/WorkBookPATExampleTopQuarks

# Configuration
trigger = "HLT_Mu9"

tightMuonCut = "isGlobalMuon() && isTrackerMuon()"

ptCut = "pt() > 20"
etaCut = "abs(eta()) < 2.1"

qualityCut = "muonID('GlobalMuonPromptTight') && "
qualityCut += "globalTrack().hitPattern().numberOfValidPixelHits() > 0 && " 
qualityCut += "innerTrack().numberOfValidHits() > 10"
# These two are included in the GlobalMuonPromptThigh ID
#qualityCut += "globalTrack().normalizedChi2() < 10.0 && " +
#qualityCut += "globalTrack().hitPattern().numberOfValidMuonHits () > 0 && " 

dbCut = "abs(dB()) < 0.2" # currently w.r.t PV! (not beamspot)

relIso = "(isolationR03().emEt+isolationR03().hadEt+isolationR03().sumPt)/pt()"
isolationCut = "%s < 0.15" % relIso

jetSelection = "pt() > 30 && abs(eta()) < 2.4"
jetMinMultiplicity = 3

applyMuonVeto = True
muonVeto = "isGlobalMuon && pt > 10. && abs(eta) < 2.5 && "+relIso+" < 0.2"


################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
process.MessageLogger.categories.append("EventCounts")
process.MessageLogger.cerr.FwkReport.reportEvery = 5000

# Uncomment the following in order to print the counters at the end of
# the job (note that if many other modules are being run in the same
# job, their INFO messages are printed too)
#process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")
process.TFileService.fileName = "histograms.root"

from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection import addDataSelection, dataSelectionCounters
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import *
from PhysicsTools.PatAlgos.tools.coreTools import removeSpecificPATObjects, removeCleaning
process.patSequence = cms.Sequence()
if options.doPat != 0:
    print "Running PAT on the fly"

    process.collisionDataSelection = cms.Sequence()
    if dataVersion.isData():
        process.collisionDataSelection = addDataSelection(process, dataVersion, trigger)

    process.patSequence = cms.Sequence(
        process.collisionDataSelection *
        addPat(process, dataVersion, doPatTrigger=False, doPatTaus=False)
    )
    removeSpecificPATObjects(process, ["Electrons", "Photons"], False)
    removeCleaning(process, False)    

    # In order to calculate the transverse impact parameter w.r.t.
    # beam spot instead of primary vertex, see
    # https://twiki.cern.ch/twiki/bin/view/CMS/WorkBookPATExampleTopQuarks
    process.patMuons.usePV = False


################################################################################

# Analysis by successive cuts

from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *
counters = []
if dataVersion.isData():
    counters = dataSelectionCounters
analysis = Analysis(process, "analysis", options, additionalCounters=counters)
process.countAnalyzer.verbose = cms.untracked.bool(True)

histoPt = Histo("pt", "pt()", min=0., max=200., nbins=200, description="muon pt (GeV/c)")
histoEta = Histo("eta", "eta()", min=-3, max=3, nbins=60, description="muon eta")
histoIso = Histo("relIso", relIso, min=0, max=0.5, nbins=100, description="Relative isolation")
histoDB = Histo("trackDB", "dB()", min=-2, max=2, nbins=400, description="Track ip @ PV (cm)")
histoNhits = Histo("trackNhits", "innerTrack().numberOfValidHits()", min=0, max=60, nbins=60, description="N(valid global hits)")
histoChi2 = Histo("trackNormChi2", "globalTrack().normalizedChi2()", min=0, max=20, nbins=40, description="Track norm chi2")

histoMet = Histo("et", "et()", min=0., max=300., nbins=300, description="MET (GeV)")

histosBeginning = [histoPt, histoEta, histoIso]
histosGlobal = histosBeginning+[histoDB, histoNhits, histoChi2]

muons = cms.InputTag("selectedPatMuons")
jets = cms.InputTag("selectedPatJets")
#jets = cms.InputTag("selectedPatJetsAK5JPT")

# Beginning
histoAnalyzer = analysis.addMultiHistoAnalyzer("AllMuons", [
        ("muon_", muons, histosBeginning),
        ("calomet_", cms.InputTag("patMETs"), [histoMet]),
        ("pfmet_", cms.InputTag("patMETsPF"), [histoMet]),
        ("tcmet_", cms.InputTag("patMETsTC"), [histoMet])])
multipAnalyzer = analysis.addAnalyzer("Multiplicity", cms.EDAnalyzer("HPlusCandViewMultiplicityAnalyzer",
        allMuons = cms.untracked.PSet(
            src = muons,
            min = cms.untracked.int32(0),
            max = cms.untracked.int32(5),
            nbins = cms.untracked.int32(5)
        ),
        selMuons = cms.untracked.PSet(
            src = muons,
            min = cms.untracked.int32(0),
            max = cms.untracked.int32(5),
            nbins = cms.untracked.int32(5)
        ),
        jets = cms.untracked.PSet(
            src = jets,
            min = cms.untracked.int32(0),
            max = cms.untracked.int32(10),
            nbins = cms.untracked.int32(10)
        )
))

# Select jets already here (but do not cut on their number), so we can
# track the multiplicity through the selections
selectedJets = analysis.addSelection("JetSelection", jets, jetSelection)
multipAnalyzer = analysis.addCloneAnalyzer("MultiplicityAfterJetSelection", multipAnalyzer)
multipAnalyzer.jets.src = selectedJets


# Trigger (for MC)
analysis.addTriggerCut(dataVersion, trigger)
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("Triggered", histoAnalyzer)
multipAnalyzer = analysis.addCloneAnalyzer("Multiplicity", multipAnalyzer)

# Tight muon (global + tracker)
selectedMuons = analysis.addCut("GlobalTrackerMuon", muons, tightMuonCut)
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("GlobalTrackerMuons", histoAnalyzer)
histoAnalyzer.muon_.src = selectedMuons
histoAnalyzer.muon_.histograms = cms.VPSet([h.pset() for h in histosGlobal])

multipAnalyzer = analysis.addCloneAnalyzer("Multiplicity", multipAnalyzer)
multipAnalyzer.selMuons.src = selectedMuons

# Kinematical cuts
selectedMuons = analysis.addCut("MuonKin", selectedMuons, ptCut + " && " + etaCut)
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("MuonKin", histoAnalyzer)
histoAnalyzer.muon_.src = selectedMuons
multipAnalyzer = analysis.addCloneAnalyzer("Multiplicity", multipAnalyzer)
multipAnalyzer.selMuons.src = selectedMuons

# Quality cuts
selectedMuons = analysis.addCut("MuonQuality", selectedMuons, qualityCut+" && "+dbCut)
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("MuonQuality", histoAnalyzer)
histoAnalyzer.muon_.src = selectedMuons
multipAnalyzer = analysis.addCloneAnalyzer("Multiplicity", multipAnalyzer)
multipAnalyzer.selMuons.src = selectedMuons

# Isolation
selectedMuons = analysis.addCut("MuonIsolation", selectedMuons, isolationCut)
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("MuonIsolation", histoAnalyzer)
histoAnalyzer.muon_.src = selectedMuons
multipAnalyzer = analysis.addCloneAnalyzer("Multiplicity", multipAnalyzer)
multipAnalyzer.selMuons.src = selectedMuons

# Veto against 2nd muon
if applyMuonVeto:
    vetoMuons = analysis.addCut("MuonVeto", muons, muonVeto, minNumber=0, maxNumber=1)
    histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("MuonVeto", histoAnalyzer)
    multipAnalyzer = analysis.addCloneAnalyzer("Multiplicity", multipAnalyzer)
    multipAnalyzer.selMuons.src = selectedMuons

# Jet selection
selectedJets = analysis.addNumberCut("JetMultiplicityCut", selectedJets, minNumber=jetMinMultiplicity)
histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("JetSelection", histoAnalyzer)
multipAnalyzer = analysis.addCloneAnalyzer("Multiplicity", multipAnalyzer)
multipAnalyzer.selMuons.src = selectedMuons

process.analysisPath = cms.Path(
    process.patSequence *
    analysis.getSequence()
)

################################################################################

from HLTrigger.HLTfilters.triggerResultsFilter_cfi import triggerResultsFilter
process.afterOtherCutsTriggerFilter = triggerResultsFilter.clone(
    hltResults = "TriggerResults::"+dataVersion.getTriggerProcess(),
    l1tResults = "",
    throw = True,
    triggerConditions = cms.vstring(trigger)
)

# Muon preselection
process.afterOtherCutsMuonPreSelection = cms.EDFilter("HPlusCandViewLazyPtrSelector",
    src = muons,
    cut = cms.string(tightMuonCut+"&&"+qualityCut)
)
selectedMuons = cms.InputTag("afterOtherCutsMuonPreSelection")
process.afterOtherCutsMuonPreSelectionFilter = cms.EDFilter("CandViewCountFilter",
    src = selectedMuons,
    minNumber = cms.uint32(1)
)
# Muon veto
process.afterOtherCutsMuonVetoSeq = cms.Sequence()
if applyMuonVeto:
    process.afterOtherCutsMuonVetoSelection = cms.EDFilter("HPlusCandViewLazyPtrSelector",
        src = muons,
        cut = cms.string(muonVeto)
    )
    process.afterOtherCutsMuonVetoFilter = cms.EDFilter("PATCandViewCountFilter",
        src = cms.InputTag("afterOtherCutsMuonVetoSelection"),
        minNumber = cms.uint32(0),
        maxNumber = cms.uint32(1)
    )
    process.afterOtherCutsMuonVetoSeq = cms.Sequence(
        process.afterOtherCutsMuonVetoSelection *
        process.afterOtherCutsMuonVetoFilter
    )

# Jet selection
selectedJets = cms.InputTag("afterOtherCutsJetSelection")
process.afterOtherCutsJetSelection = cms.EDFilter("HPlusCandViewLazyPtrSelector",
    src = jets,
    cut = cms.string(jetSelection)
)
process.afterOtherCutsJetSelectionFilter = cms.EDFilter("CandViewCountFilter",
    src = selectedJets,
    minNumber = cms.uint32(jetMinMultiplicity)
)

process.afterOtherCuts = cms.EDAnalyzer("HPlusCandViewHistoAfterOtherCutsAnalyzer",
    src = selectedMuons,
    histograms = cms.VPSet(
        histoPt.pset().clone(cut=cms.untracked.string(ptCut)),
        histoEta.pset().clone(cut=cms.untracked.string(etaCut)),
        histoDB.pset().clone(cut=cms.untracked.string(dbCut)),
        histoIso.pset().clone(cut=cms.untracked.string(isolationCut))
    )
)
process.afterOtherCutsPath = cms.Path(
    process.patSequence *
    process.afterOtherCutsTriggerFilter *
    process.afterOtherCutsMuonPreSelection *
    process.afterOtherCutsMuonPreSelectionFilter *
    process.afterOtherCutsMuonVetoSeq * # empty sequence if veto is not applied
    process.afterOtherCutsJetSelection *
    process.afterOtherCutsJetSelectionFilter *
    process.afterOtherCuts
)



