import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptions
from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataVersion import DataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

#dataVersion = "36X"
#dataVersion = "36Xspring10"
#dataVersion = "37X"
dataVersion = "38X"
#dataVersion = "data" # this is for collision data 

options = VarParsing.VarParsing()
options.register("WDecaySeparate",
                 0,
                 options.multiplicity.singleton,
                 options.varType.int,
                 "Separate W decays from MC information")
options = getOptions(options)
if options.dataVersion != "":
    dataVersion = options.dataVersion

print "Assuming data is ", dataVersion
dataVersion = DataVersion(dataVersion) # convert string to object

process = cms.Process("HChMuonAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

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
# https://twiki.cern.ch/twiki/bin/view/CMS/TopLeptonPlusJetsRefSel_mu

# Configuration
trigger = options.trigger
if len(trigger) == 0:
    trigger = "HLT_Mu9"

print "Using trigger %s" % trigger

tightMuonCut = "isGlobalMuon() && isTrackerMuon()"

ptCut = "pt() > 40"
etaCut = "abs(eta()) < 2.1"

qualityCut = "muonID('GlobalMuonPromptTight')"
qualityCut += " && innerTrack().numberOfValidHits() > 10"
qualityCut += " && innerTrack().hitPattern().pixelLayersWithMeasurement() >= 1"
qualityCut += " && numberOfMatches() > 1"
# These two are included in the GlobalMuonPromptThigh ID
#qualityCut += "globalTrack().normalizedChi2() < 10.0 && " +
#qualityCut += "globalTrack().hitPattern().numberOfValidMuonHits () > 0 && " 

dbCut = "abs(dB()) < 0.02" # w.r.t. beamSpot (note process.patMuons.usePV = False, PATMuonProducer takes beam spot from the event, so this could be safe also for 36X data

maxVertexZ = 1.0

relIso = "(isolationR03().emEt+isolationR03().hadEt+isolationR03().sumPt)/pt()"
isolationCut = "%s < 0.05" % relIso

jetSelection = "pt() > 30 && abs(eta()) < 2.4"
jetMinMultiplicity = 3

applyMuonVeto = False
muonVeto = "isGlobalMuon && pt > 10. && abs(eta) < 2.5 && "+relIso+" < 0.2"

applyElectronVeto = False
electronVeto = "et() > 15 && abs(eta()) < 2.5 && (dr03TkSumPt()+dr03EcalRecHitSumEt()+dr03HcalTowerSumEt())/et() < 0.2"

applyZVeto = True
zVetoMuonSelection ="isGlobalMuon && pt > 20. && abs(eta) < 2.5"

metCut = "et() > 40"

muons = cms.InputTag("selectedPatMuons")
electrons = cms.InputTag("selectedPatElectrons")
jets = cms.InputTag("selectedPatJets")
#jets = cms.InputTag("selectedPatJetsAK5JPT")

caloMET = "patMETs"
pfMET = "patMETsPF"
tcMET = "patMETsTC"

met = cms.InputTag(pfMET)

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
#process.options.wantSummary = cms.untracked.bool(True)
process.MessageLogger.cerr.FwkReport.reportEvery = 5000

# Uncomment the following in order to print the counters at the end of
# the job (note that if many other modules are being run in the same
# job, their INFO messages are printed too)
#process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")
process.TFileService.fileName = "histograms.root"

from HiggsAnalysis.HeavyChHiggsToTauNu.HChDataSelection import addDataSelection, dataSelectionCounters
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import *
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi import *
from PhysicsTools.PatAlgos.tools.coreTools import removeSpecificPATObjects, removeCleaning
process.patSequence = cms.Sequence()
if options.doPat != 0:
    print "Running PAT on the fly"

    process.collisionDataSelection = cms.Sequence()
    if dataVersion.isData():
        process.collisionDataSelection = addDataSelection(process, dataVersion, trigger)

    process.patPlainSequence = addPat(process, dataVersion, doPatTrigger=False, doPatTaus=False, doPatElectronID=False, doTauHLTMatching=False)
    process.patSequence = cms.Sequence(
        process.collisionDataSelection *
        process.patPlainSequence
    )
    #removeSpecificPATObjects(process, ["Electrons", "Photons"], False)
    removeSpecificPATObjects(process, ["Photons"], False)
    removeCleaning(process, False)    

    # In order to calculate the transverse impact parameter w.r.t.
    # beam spot instead of primary vertex, see
    # https://twiki.cern.ch/twiki/bin/view/CMS/WorkBookPATExampleTopQuarks
    process.patMuons.usePV = False


################################################################################

# Generator and configuration info analyzers
process.configInfo = cms.EDAnalyzer("HPlusConfigInfoAnalyzer")
if options.crossSection >= 0.:
    process.configInfo.crossSection = cms.untracked.double(options.crossSection)
    print "Dataset cross section has been set to %g pb" % options.crossSection
if options.luminosity >= 0:
    process.configInfo.luminosity = cms.untracked.double(options.luminosity)
    print "Dataset integrated luminosity has been set to %g pb^-1" % options.luminosity

process.firstPrimaryVertex = cms.EDProducer("HPlusSelectFirstVertex",
    src = cms.InputTag("offlinePrimaryVertices")
)
process.patSequence *= process.firstPrimaryVertex

process.commonSequence = cms.Sequence(
    process.patSequence +
    process.configInfo
)

# Analysis by successive cuts
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *
histoPt = Histo("pt", "pt()", min=0., max=400., nbins=400, description="muon pt (GeV/c)")
histoEta = Histo("eta", "eta()", min=-3, max=3, nbins=120, description="muon eta")
histoIso = Histo("relIso", relIso, min=0, max=0.5, nbins=100, description="Relative isolation")
histoDB = Histo("trackDB", "dB()", min=-0.2, max=0.2, nbins=400, description="Track ip @ PV (cm)")
histoNhits = Histo("trackNhits", "innerTrack().numberOfValidHits()", min=0, max=60, nbins=60, description="N(valid global hits)")
histoChi2 = Histo("trackNormChi2", "globalTrack().normalizedChi2()", min=0, max=20, nbins=100, description="Track norm chi2")

histoMet = Histo("et", "et()", min=0., max=400., nbins=400, description="MET (GeV)")

histoTransverseMass = Histo("tmass", "sqrt((daughter(0).pt+daughter(1).pt)*(daughter(0).pt+daughter(1).pt)-pt*pt)",
                            min=0, max=120, nbins=120, description="W transverse mass")

histosBeginning = [histoPt, histoEta, histoIso]
histosGlobal = histosBeginning+[histoDB, histoNhits, histoChi2]

vertexCollections = ["offlinePrimaryVertices"]
if dataVersion.isData():
    vertexCollections.append("goodPrimaryVertices")

def createAnalysis(process, prefix="", beginSequence=None):
    counters = []
    if dataVersion.isData():
        counters = dataSelectionCounters
    analysis = Analysis(process, "analysis", options, prefix=prefix, additionalCounters=counters)
    analysis.getCountAnalyzer().printMainCounter = cms.untracked.bool(True)
    #analysis.getCountAnalyzer().printSubCounters = cms.untracked.bool(True)
    #analysis.getCountAnalyzer().printAvailableCounters = cms.untracked.bool(True)
    
    if beginSequence != None:
        analysis.appendToSequence(beginSequence)

    multipName = "Multiplicity"
    pileupName = "VertexCount"

    # Beginning
    histoAnalyzer = analysis.addMultiHistoAnalyzer("AllMuons", [
            ("muon_", muons, histosBeginning),
            ("calomet_", cms.InputTag(caloMET), [histoMet]),
            ("pfmet_", cms.InputTag(pfMET), [histoMet]),
            ("tcmet_", cms.InputTag(tcMET), [histoMet])])
    multipAnalyzer = analysis.addAnalyzer(multipName, cms.EDAnalyzer("HPlusCandViewMultiplicityAnalyzer",
            allMuons = cms.untracked.PSet(
                src = muons,
                min = cms.untracked.int32(0),
                max = cms.untracked.int32(10),
                nbins = cms.untracked.int32(10)
            ),
            selMuons = cms.untracked.PSet(
                src = muons,
                min = cms.untracked.int32(0),
                max = cms.untracked.int32(10),
                nbins = cms.untracked.int32(10)
            ),
            jets = cms.untracked.PSet(
                src = jets,
                min = cms.untracked.int32(0),
                max = cms.untracked.int32(20),
                nbins = cms.untracked.int32(20)
            )
    ))
    pileupAnalyzer = None
    if beginSequence == None:
        pileupAnalyzer = analysis.addAnalyzer(pileupName, cms.EDAnalyzer(
                "HPlusVertexCountAnalyzer",
                src = cms.untracked.VInputTag([cms.untracked.InputTag(x) for x in vertexCollections]),
                min = cms.untracked.double(0),
                max = cms.untracked.double(20),
                nbins = cms.untracked.int32(20),
        ))
        
    # Select jets already here (but do not cut on their number), so we can
    # track the multiplicity through the selections
    selectedJets = analysis.addSelection("JetSelection", jets, jetSelection)
    multipAnalyzer = analysis.addCloneAnalyzer("MultiplicityAfterJetSelection", multipAnalyzer)
    multipAnalyzer.jets.src = selectedJets
    
    
    # Trigger
    analysis.addTriggerCut(dataVersion, trigger)
    histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("Triggered", histoAnalyzer)
    multipAnalyzer = analysis.addCloneAnalyzer(multipName, multipAnalyzer)
    if pileupAnalyzer:
        pileupAnalyzer = analysis.addCloneAnalyzer(pileupName, pileupAnalyzer)
    
    # Select primary vertex
    selectedPrimaryVertex = analysis.addAnalysisModule("PrimaryVertex",
                                                       selector = goodPrimaryVertices.clone(src = cms.InputTag("firstPrimaryVertex")),
                                                       filter = cms.EDFilter("VertexCountFilter",
                                                                             src = cms.InputTag("dummy"),
                                                                             minNumber = cms.uint32(1),
                                                                             maxNumber = cms.uint32(999)),
                                                       counter=True).getSelectorInputTag()
    
    histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("PrimaryVertex", histoAnalyzer)
    multipAnalyzer = analysis.addCloneAnalyzer(multipName, multipAnalyzer)
    if pileupAnalyzer:
        pileupAnalyzer = analysis.addCloneAnalyzer(pileupName, pileupAnalyzer)
    
    # Tight muon (global + tracker)
    selectedMuons = analysis.addCut("GlobalTrackerMuon", muons, tightMuonCut, selector="PATMuonSelector")
    histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("GlobalTrackerMuons", histoAnalyzer)
    histoAnalyzer.muon_.src = selectedMuons
    histoAnalyzer.muon_.histograms = cms.VPSet([h.pset() for h in histosGlobal])
    
    multipAnalyzer = analysis.addCloneAnalyzer(multipName, multipAnalyzer)
    multipAnalyzer.selMuons.src = selectedMuons
    if pileupAnalyzer:
        pileupAnalyzer = analysis.addCloneAnalyzer(pileupName, pileupAnalyzer)
    
    # Kinematical cuts
    selectedMuons = analysis.addCut("MuonKin", selectedMuons, ptCut + " && " + etaCut, selector="PATMuonSelector")
    histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("MuonKin", histoAnalyzer)
    histoAnalyzer.muon_.src = selectedMuons
    multipAnalyzer = analysis.addCloneAnalyzer(multipName, multipAnalyzer)
    multipAnalyzer.selMuons.src = selectedMuons
    if pileupAnalyzer:
        pileupAnalyzer = analysis.addCloneAnalyzer(pileupName, pileupAnalyzer)
    
    # DR against the selected jets
    from PhysicsTools.PatAlgos.cleaningLayer1.muonCleaner_cfi import cleanPatMuons
    muonJetCleaner = cleanPatMuons.clone(
        src = selectedMuons,
        checkOverlaps = cms.PSet(
            jets = cms.PSet(
                src                 = selectedJets,
                algorithm           = cms.string("byDeltaR"),
                preselection        = cms.string(""),
                deltaR              = cms.double(0.3),
                checkRecoComponents = cms.bool(False),
                pairCut             = cms.string(""),
                requireNoOverlaps   = cms.bool(True)
                )
        )
    )
    selectedMuons = analysis.addAnalysisModule("MuonCleaningFromJet",
                                               selector = muonJetCleaner,
                                               filter = makeCountFilter(cms.InputTag("dummy"), minNumber=1),
                                               counter=True).getSelectorInputTag()
    
    histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("MuonJetDR", histoAnalyzer)
    histoAnalyzer.muon_.src = selectedMuons
    multipAnalyzer = analysis.addCloneAnalyzer(multipName, multipAnalyzer)
    multipAnalyzer.selMuons.src = selectedMuons
    if pileupAnalyzer:
        pileupAnalyzer = analysis.addCloneAnalyzer(pileupName, pileupAnalyzer)
    
    # Quality cuts
    selectedMuons = analysis.addCut("MuonQuality", selectedMuons, qualityCut+" && "+dbCut)
    histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("MuonQuality", histoAnalyzer)
    histoAnalyzer.muon_.src = selectedMuons
    multipAnalyzer = analysis.addCloneAnalyzer(multipName, multipAnalyzer)
    multipAnalyzer.selMuons.src = selectedMuons
    if pileupAnalyzer:
        pileupAnalyzer = analysis.addCloneAnalyzer(pileupName, pileupAnalyzer)
    
    # Isolation
#    selectedMuons = analysis.addCut("MuonIsolation", selectedMuons, isolationCut)
#    histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("MuonIsolation", histoAnalyzer)
#    histoAnalyzer.muon_.src = selectedMuons
#    multipAnalyzer = analysis.addCloneAnalyzer(multipName, multipAnalyzer)
#    multipAnalyzer.selMuons.src = selectedMuons
    
    # Difference in vertex z coordinate
    selectedMuons = analysis.addAnalysisModule("MuonVertexDiff",
                                               selector = cms.EDProducer("HPlusCandViewPtrVertexZSelector",
                                                                         candSrc = selectedMuons,
                                                                         vertexSrc = selectedPrimaryVertex,
                                                                         maxZ = cms.double(maxVertexZ)),
                                               filter = makeCountFilter(cms.InputTag("dummy"), minNumber=1),
                                               counter = True).getSelectorInputTag()
    histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("MuonVertex", histoAnalyzer)
    histoAnalyzer.muon_.src = selectedMuons
    multipAnalyzer = analysis.addCloneAnalyzer(multipName, multipAnalyzer)
    multipAnalyzer.selMuons.src = selectedMuons
    if pileupAnalyzer:
        pileupAnalyzer = analysis.addCloneAnalyzer(pileupName, pileupAnalyzer)
    
    # Veto against 2nd muon
    if applyMuonVeto:
        vetoMuons = analysis.addCut("MuonVeto", muons, muonVeto, minNumber=0, maxNumber=1)
        histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("MuonVeto", histoAnalyzer)
        multipAnalyzer = analysis.addCloneAnalyzer(multipName, multipAnalyzer)
        multipAnalyzer.selMuons.src = selectedMuons
        if pileupAnalyzer:
            pileupAnalyzer = analysis.addCloneAnalyzer(pileupName, pileupAnalyzer)
    
    # Veto against electrons
    if applyElectronVeto:
        vetoElectrons = analysis.addCut("ElectronVeto", electrons, electronVeto, minNumber=0, maxNumber=0)
        histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("ElectronVeto", histoAnalyzer)
        multipAnalyzer = analysis.addCloneAnalyzer(multipName, multipAnalyzer)
        if pileupAnalyzer:
            pileupAnalyzer = analysis.addCloneAnalyzer(pileupName, pileupAnalyzer)
    
    
    # W transverse mass
    candCombinerPrototype = cms.EDProducer("CandViewShallowCloneCombiner",
        checkCharge = cms.bool(False),
    #    cut = cms.string('sqrt((daughter(0).pt+daughter(1).pt)*(daughter(0).pt+daughter(1).pt)-pt*pt)>50'),
        cut = cms.string(""),
        decay = cms.string("dummy")
    )
    wmunuCalo = analysis.addProducer("WMuNuCalo", candCombinerPrototype.clone(decay = cms.string(selectedMuons.getModuleLabel()+" "+caloMET)))
    wmunuPF   = analysis.addProducer("WMuNuPF",   candCombinerPrototype.clone(decay = cms.string(selectedMuons.getModuleLabel()+" "+pfMET)))
    wmunuTC   = analysis.addProducer("WMuNuTC",   candCombinerPrototype.clone(decay = cms.string(selectedMuons.getModuleLabel()+" "+tcMET)))
    histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("WMunuCands", histoAnalyzer)
    histoAnalyzer.wmunuCalo_ = cms.untracked.PSet(src = wmunuCalo, histograms = cms.VPSet(histoTransverseMass.pset()))
    histoAnalyzer.wmunuPF_   = cms.untracked.PSet(src = wmunuPF,   histograms = cms.VPSet(histoTransverseMass.pset()))
    histoAnalyzer.wmunuTC_   = cms.untracked.PSet(src = wmunuTC,   histograms = cms.VPSet(histoTransverseMass.pset()))
    
    # Jet selection
    selectedJets = analysis.addNumberCut("JetMultiplicityCut", selectedJets, minNumber=jetMinMultiplicity)
    histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("JetSelection", histoAnalyzer)
    multipAnalyzer = analysis.addCloneAnalyzer(multipName, multipAnalyzer)
    multipAnalyzer.selMuons.src = selectedMuons
    if pileupAnalyzer:
        pileupAnalyzer = analysis.addCloneAnalyzer(pileupName, pileupAnalyzer)
    
    # MET cut
    selectedMET = analysis.addCut("METCut", met, metCut)
    histoAnalyzer = analysis.addCloneMultiHistoAnalyzer("METCut", histoAnalyzer)
    multipAnalyzer = analysis.addCloneAnalyzer(multipName, multipAnalyzer)
    if pileupAnalyzer:
        pileupAnalyzer = analysis.addCloneAnalyzer(pileupName, pileupAnalyzer)
    
    setattr(process, prefix+"analysisPath", cms.Path(
        process.commonSequence *
        analysis.getSequence()
    ))
    
    ################################################################################

    path = cms.Path(process.commonSequence)
    if beginSequence != None:
        path *= beginSequence
    path *= analysis.getAnalysisModule("Trigger").getFilterSequence()
    path *= analysis.getAnalysisModule("PrimaryVertex").getFilterSequence()
    path *= analysis.getAnalysisModule("JetSelection").getFilterSequence()
    
    # Muon preselection
    m = muonJetCleaner.clone(
        src = muons,
        preselection = cms.string(tightMuonCut+"&&"+qualityCut)
    )
    setattr(process, prefix+"afterOtherCutsMuonPreSelection", m)
    path *= m

    m = cms.EDProducer("HPlusCandViewPtrVertexZSelector",
        candSrc = cms.InputTag(prefix+"afterOtherCutsMuonPreSelection"),
        vertexSrc = analysis.getAnalysisModule("PrimaryVertex").getSelectorInputTag(),
        maxZ = cms.double(maxVertexZ)
    )
    setattr(process, prefix+"afterOtherCutsMuonVertexSelection", m)
    path *= m
    selectedMuons = cms.InputTag(prefix+"afterOtherCutsMuonVertexSelection")

    m = cms.EDFilter("CandViewCountFilter",
        src = selectedMuons,
        minNumber = cms.uint32(1)
    )
    setattr(process, prefix+"afterOtherCutsMuonPreSelectionFilter", m)
    path *= m

    if applyMuonVeto:
        path *= analysis.getAnalysisModule("MuonVeto").getFilterSequence()
    if applyElectronVeto:
        path *= analysis.getAnalysisModule("ElectronVeto").getFilterSequence()

    afterOtherCuts = cms.EDAnalyzer("HPlusCandViewHistoAfterOtherCutsAnalyzer",
        src = selectedMuons,
        histograms = cms.VPSet(
            histoPt.pset().clone(cut=cms.untracked.string(ptCut)),
            histoEta.pset().clone(cut=cms.untracked.string(etaCut)),
            histoDB.pset().clone(cut=cms.untracked.string(dbCut)),
        )
    )
    afterOtherCutsIso = afterOtherCuts.clone()
    afterOtherCutsIso.histograms.append(histoIso.pset().clone(cut=cms.untracked.string(isolationCut)))

    def addAfterCuts(path, name):
        m = afterOtherCuts.clone()
        setattr(process, prefix+"afterOtherCuts"+name, m)
        path *= m
        m = afterOtherCutsIso.clone()
        setattr(process, prefix+"afterOtherCutsIso"+name, m)
        path *= m
    
    # Plots after vetoes
    addAfterCuts(path, "AfterVetoes")
    
    # Plots after jet multiplicity cuts
    path *= analysis.getAnalysisModule("JetMultiplicityCut").getFilterSequence()
    addAfterCuts(path, "AfterJetMultiplicityCut")
    
    # Plots after MET cut
    path *= analysis.getAnalysisModule("METCut").getFilterSequence()
    addAfterCuts(path, "AfterMETCut")
    
    # Plots after Wmunu transverse mass cut
    m = candCombinerPrototype.clone(decay = cms.string(selectedMuons.getModuleLabel()+" "+pfMET))
    setattr(process, prefix+"afterOtherCutsWMuNuPF", m)
    path *= m
    m = cms.EDFilter("HPlusCandViewLazyPtrSelector",
        src = cms.InputTag(prefix+"afterOtherCutsWMuNuPF"),
        cut = cms.string(histoTransverseMass.getPlotQuantity()+ " > 50")
    )
    setattr(process, prefix+"afterOtherCutsWMuNuSelector", m)
    path *= m
    m = cms.EDFilter("CandViewCountFilter",
        src = cms.InputTag("afterOtherCutsWMuNuSelector"),
        minNumber = cms.uint32(1)
    )
    setattr(process, prefix+"afterOtherCutsWMuNuFilter", m)
    path *= m

    addAfterCuts(path, "AfterWMuNuCut")

    setattr(process, prefix+"afterOtherCutsPath", path)

class AddGenEventFilter:
    def __init__(self, invert=False):
        self.invert = invert

    def __call__(self, analysis):
        analysis.addAnalysisModule("MCEventTopology", filter=cms.EDFilter("HPlusGenEventTopologyFilter",
                src = cms.InputTag("genParticles"),
                particle = cms.string("abs(pdgId()) == 24"),
                daughter = cms.string("abs(pdgId()) == 13"),
                minParticles = cms.uint32(1),
                minDaughters = cms.uint32(1)
            ),
            invertFilter=self.invert
        )

class AddVertexCountFilter:
    def __init__(self, maxVertices):
        self.maxVertices = maxVertices

    def __call__(self, analysis):
        analysis.addAnalysisModule("VertexCount", filter=cms.EDFilter("VertexCountFilter",
                src = cms.InputTag("goodPrimaryVertices"),
                minNumber = cms.uint32(1),
                maxNumber = cms.uint32(self.maxVertices)
        ))


createAnalysis(process)
if options.WDecaySeparate > 0:
    process.mcEventTopology = cms.EDFilter("HPlusGenEventTopologyFilter",
        src = cms.InputTag("genParticles"),
        particle = cms.string("abs(pdgId()) == 24"),
        daughter = cms.string("abs(pdgId()) == 13"),
        minParticles = cms.uint32(1),
        minDaughters = cms.uint32(1)
    )
    process.wMuNuSequence = cms.Sequence(
        process.mcEventTopology
    )
    process.wOtherSequence = cms.Sequence(
        ~process.mcEventTopology
    )

    createAnalysis(process, "WMuNu", process.wMuNuSequence)
    createAnalysis(process, "WOther", process.wOtherSequence)

if dataVersion.isData():
    for i in xrange(1, 11):
        m = cms.EDFilter("VertexCountFilter",
            src = cms.InputTag("goodPrimaryVertices"),
            minNumber = cms.uint32(1),
            maxNumber = cms.uint32(i)
        )
        s = cms.Sequence(m)
        setattr(process, "pileupV%dVertexCount"%i, m)
        setattr(process, "pileupV%dVertexCountSequence"%i, s)

        createAnalysis(process, "PileupV%d"%i, s)

#print process.dumpPython()

