import FWCore.ParameterSet.Config as cms
from HiggsAnalysis.HeavyChHiggsToTauNu.HChOptions import getOptionsDataVersion
import FWCore.ParameterSet.VarParsing as VarParsing

dataVersion = "39Xredigi"
#dataVersion = "39Xdata"

################################################################################

# Command line arguments (options) and DataVersion object
options = VarParsing.VarParsing()
options.register("WDecaySeparate",
                 0,
                 options.multiplicity.singleton,
                 options.varType.int,
                 "Separate W decays from MC information")
options, dataVersion = getOptionsDataVersion(dataVersion, options)

process = cms.Process("HChMuonAnalysis")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string(dataVersion.getGlobalTag())

process.source = cms.Source('PoolSource',
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
#    trigger = "HLT_Mu9"
    trigger = "HLT_Mu15_v1"

print "Using trigger %s" % trigger

tightMuonCut = "isGlobalMuon() && isTrackerMuon()"

ptCutString = "pt() > %d"
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

# PfAllParticleIso=3,PfChargedHadronIso=4, PfNeutralHadronIso=5, PfGammaIso=6, 
isolations = {
    # Detector iso
    "trackIso": "isolationR03().sumPt",
    "caloIso": "isolationR03().emEt+isolationR03().hadEt",
    # 'standard' PF isolation
    "pfChargedIso": "isoDeposit('PfChargedHadronIso').depositWithin(0.4)",
    "pfNeutralIso": "isoDeposit('PfNeutralHadronIso').depositWithin(0.4)",
    "pfGammaIso": "isoDeposit('PfGammaIso').depositWithin(0.4)",
}
isolations["sumIso"] = "%s+%s" % (isolations["trackIso"], isolations["caloIso"])
isolations["pfSumIso"] = "%s+%s+%s" % (isolations["pfChargedIso"], isolations["pfNeutralIso"], isolations["pfGammaIso"])
for key, value in isolations.items():
    isolations[key+"Rel"] = "(%s)/pt" % value

jetSelection = "pt() > 30 && abs(eta()) < 2.4"
jetId = "emEnergyFraction() > 0.01 && jetID().n90Hits > 1 && jetID().fHPD < 0.98"
jetIdPF = "numberOfDaughters() > 1 && chargedEmEnergyFraction() < 0.99 && neutralHadronEnergyFraction() < 0.99 && neutralEmEnergyFraction < 0.99 && chargedHadronEnergyFraction() > 0 && chargedMultiplicity() > 0"

muonVeto = "isGlobalMuon && pt > 10. && abs(eta) < 2.5 && "+isolations["sumIsoRel"]+" < 0.2"
electronVeto = "et() > 15 && abs(eta()) < 2.5 && (dr03TkSumPt()+dr03EcalRecHitSumEt()+dr03HcalTowerSumEt())/et() < 0.2"
zMassVetoMuons ="isGlobalMuon && pt > 20. && abs(eta) < 2.5"
zMassVeto = "76 < mass() && mass < 106"

metCutString = "et() > %d"

muons = cms.InputTag("selectedPatMuons")
electrons = cms.InputTag("selectedPatElectrons")
jets = cms.InputTag("selectedPatJets")
jetsPF = cms.InputTag("selectedPatJetsAK5PF")

caloMET = "patMETs"
pfMET = "patMETsPF"
tcMET = "patMETsTC"

met = cms.InputTag(pfMET)

################################################################################

process.load("HiggsAnalysis.HeavyChHiggsToTauNu.HChCommon_cfi")
#process.options.wantSummary = cms.untracked.bool(True)
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
process.MessageLogger.categories.append("TauIsolationSelector")

# Uncomment the following in order to print the counters at the end of
# the job (note that if many other modules are being run in the same
# job, their INFO messages are printed too)
#process.MessageLogger.cerr.threshold = cms.untracked.string("INFO")

# Fragment to run PAT on the fly if requested from command line
from HiggsAnalysis.HeavyChHiggsToTauNu.HChPatTuple import addPatOnTheFly
from PhysicsTools.PatAlgos.tools.coreTools import removeSpecificPATObjects
patArgs = {"doPatTrigger": False,
#           "doPatTaus": False,
           "doHChTauDiscriminators": False,
           "doPatElectronID": False,
           "doTauHLTMatching": False,
           "doPatMuonPFIsolation": True,
           }
process.commonSequence, additionalCounters = addPatOnTheFly(process, options, dataVersion, patArgs=patArgs)

# Add configuration information to histograms.root
from HiggsAnalysis.HeavyChHiggsToTauNu.HChTools import *
process.infoPath = addConfigInfo(process, options, dataVersion)

################################################################################

process.firstPrimaryVertex = cms.EDProducer("HPlusSelectFirstVertex",
    src = cms.InputTag("offlinePrimaryVertices")
)
process.commonSequence *= process.firstPrimaryVertex

# Define the histograms
histoPt = Histo("pt", "pt()", min=0., max=800., nbins=800, description="pt (GeV/c)")
histoEta = Histo("eta", "eta()", min=-3, max=3, nbins=120, description="eta")
histoPhi = Histo("phi", "phi()", min=-3.5, max=3.5, nbins=70, description="phi")

histoIsos = {}
for name, value in isolations.iteritems():
    h = None
    if "IsoRel" in name:
        h = Histo(name, value, min=0, max=0.5, nbins=100, description=name)
    else:
        h = Histo(name, value, min=0, max=100.0, nbins=100, description=name)
    histoIsos[name] = h

histoDB = Histo("trackDB", "dB()", min=-0.2, max=0.2, nbins=400, description="Track ip @ PV (cm)")
histoNhits = Histo("trackNhits", "innerTrack().numberOfValidHits()", min=0, max=60, nbins=60, description="N(valid global hits)")
histoChi2 = Histo("trackNormChi2", "globalTrack().normalizedChi2()", min=0, max=20, nbins=100, description="Track norm chi2")

histoMet = Histo("et", "et()", min=0., max=400., nbins=400, description="MET (GeV)")

histoTransverseMass = Histo("tmass", "sqrt((daughter(0).pt+daughter(1).pt)*(daughter(0).pt+daughter(1).pt)-pt*pt)",
                            min=0, max=400, nbins=400, description="W transverse mass")
histoZMass = Histo("mass", "mass()", min=0, max=400, nbins=400, description="Z mass")

histosBeginning = [histoPt, histoEta, histoPhi] + histoIsos.values()
histosGlobal = histosBeginning+[histoDB, histoNhits, histoChi2]

histosJet = [histoPt, histoEta, histoPhi]

vertexCollections = ["offlinePrimaryVertices"]
if dataVersion.isData():
    vertexCollections.append("goodPrimaryVertices")

# Class to wrap the analysis steps, and to have methods for the defined analyses
class MuonAnalysis:
    def __init__(self, process, prefix="", beginSequence=None, afterOtherCuts=False,
                 muonPtCut=30, muonIsolationCut=0.05, metCut=20, njets=3, jets=jets, doJetId=False, doIsolationWithTau=False):
        self.process = process
        self.prefix = prefix
        self.afterOtherCuts = afterOtherCuts
        self.doJetId = doJetId
        self.doIsolationWithTau = doIsolationWithTau
        self._ptCut = ptCutString % muonPtCut
        self._metCut = metCutString % metCut
        self._njets = njets
        self._jets = jets
        self._isolationCut = "%s < %f" % (isolations["sumIsoRel"], muonIsolationCut)

        self.analysis = Analysis(self.process, "analysis", options, prefix, additionalCounters=additionalCounters)
        #self.analysis.getCountAnalyzer().printMainCounter = cms.untracked.bool(True)
        #self.analysis.getCountAnalyzer().printSubCounters = cms.untracked.bool(True)
        #self.analysis.getCountAnalyzer().printAvailableCounters = cms.untracked.bool(True)

        if beginSequence != None:
            self.analysis.appendToSequence(beginSequence)
        self.multipName = "Multiplicity"
        self.pileupName = "VertexCount"

        self.selectedMuons = muons
        self.selectedJets = self._jets

        # Setup the analyzers
        if not self.afterOtherCuts:
            self.histoAnalyzer = self.analysis.addMultiHistoAnalyzer("AllMuons", [
                    ("muon_", muons, histosBeginning),
                    ("calojet_", jets, histosJet),
                    ("pfjet_", jetsPF, histosJet),
                    ("calomet_", cms.InputTag(caloMET), [histoMet]),
                    ("pfmet_", cms.InputTag(pfMET), [histoMet]),
                    ("tcmet_", cms.InputTag(tcMET), [histoMet])])
            self.multipAnalyzer = self.analysis.addAnalyzer(self.multipName, cms.EDAnalyzer("HPlusCandViewMultiplicityAnalyzer",
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
                        src = self._jets,
                        min = cms.untracked.int32(0),
                        max = cms.untracked.int32(20),
                        nbins = cms.untracked.int32(20)
                    )
            ))
            self.pileupAnalyzer = None
            if beginSequence == None:
                self.pileupAnalyzer = self.analysis.addAnalyzer(self.pileupName, cms.EDAnalyzer("HPlusVertexCountAnalyzer",
                        src = cms.untracked.VInputTag([cms.untracked.InputTag(x) for x in vertexCollections]),
                        min = cms.untracked.double(0),
                        max = cms.untracked.double(20),
                        nbins = cms.untracked.int32(20),
                ))
    
        # Create the prototype for muon cleaner
        from PhysicsTools.PatAlgos.cleaningLayer1.muonCleaner_cfi import cleanPatMuons
        self.muonJetCleanerPrototype = cleanPatMuons.clone(
            src = cms.InputTag("dummy"),
            checkOverlaps = cms.PSet(
                jets = cms.PSet(
                    src                 = cms.InputTag("dummy"),
                    algorithm           = cms.string("byDeltaR"),
                    preselection        = cms.string(""),
                    deltaR              = cms.double(0.3),
                    checkRecoComponents = cms.bool(False),
                    pairCut             = cms.string(""),
                    requireNoOverlaps   = cms.bool(True)
                )
            )
        )
        # Create the prototype for jet cleaner
        from PhysicsTools.PatAlgos.cleaningLayer1.jetCleaner_cfi import cleanPatJets
        self.jetMuonCleanerPrototype = cleanPatJets.clone(
            src = cms.InputTag("dummy"),
            checkOverlaps = cms.PSet(
                muons = cms.PSet(
                    src                 = cms.InputTag("dummy"),
                    algorithm           = cms.string("byDeltaR"),
                    preselection        = cms.string(""),
                    deltaR              = cms.double(0.1),
                    checkRecoComponents = cms.bool(False),
                    pairCut             = cms.string(""),
                    requireNoOverlaps   = cms.bool(True)
                )
            )
        )

        # Create the prototype for candidate combiner
        self.candCombinerPrototype = cms.EDProducer("CandViewShallowCloneCombiner",
            checkCharge = cms.bool(False),
            cut = cms.string(""),
            decay = cms.string("dummy")
        )

        # Setup the afterOtherCuts prototypes
        if self.afterOtherCuts:
            self.afterOtherCutsModule = cms.EDAnalyzer("HPlusCandViewHistoAfterOtherCutsAnalyzer",
                src = cms.InputTag("dummy"),
                histograms = cms.VPSet(
                    histoPt.pset().clone(cut=cms.untracked.string(self._ptCut)),
                    histoEta.pset().clone(cut=cms.untracked.string(etaCut)),
                    histoDB.pset().clone(cut=cms.untracked.string(dbCut)),
                )
            )
            self.afterOtherCutsModuleIso = self.afterOtherCutsModule.clone()
            self.afterOtherCutsModuleIso.histograms.append(histoIsos["sumIsoRel"].pset().clone(cut=cms.untracked.string(self._isolationCut)))
        

    def cloneHistoAnalyzer(self, name, **kwargs):
        self.histoAnalyzer = self.analysis.addCloneAnalyzer(name, self.histoAnalyzer)
        if "muonSrc" in kwargs:
            self.histoAnalyzer.muon_.src = kwargs["muonSrc"]
        if "pfJetSrc" in kwargs:
            self.histoAnalyzer.pfjet_.src = kwargs["pfJetSrc"]

    def cloneMultipAnalyzer(self, **kwargs):
        name = self.multipName
        if "name" in kwargs:
            name = kwargs["name"]
        self.multipAnalyzer = self.analysis.addCloneAnalyzer(name, self.multipAnalyzer)
        if "selMuonSrc" in kwargs:
            self.multipAnalyzer.selMuons.src = kwargs["selMuonSrc"]

    def clonePileupAnalyzer(self):
        if self.pileupAnalyzer:
            self.pileupAnalyzer = self.analysis.addCloneAnalyzer(self.pileupName, self.pileupAnalyzer)

    def addAfterOtherCutsAnalyzer(self, prefix):
        self.analysis.addAnalyzer(prefix+"AfterOtherCuts", self.afterOtherCutsModule.clone(src=self.selectedMuons))
        self.analysis.addAnalyzer(prefix+"AfterOtherCutsIso", self.afterOtherCutsModuleIso.clone(src=self.selectedMuons))

    def createAnalysisPath(self):
        setattr(self.process, self.prefix+"analysisPath", cms.Path(
                self.process.commonSequence *
                self.analysis.getSequence()
        ))

    def addWtransverseMassHistos(self):
        wmunuCalo = self.analysis.addProducer("WMuNuCalo", self.candCombinerPrototype.clone(decay = cms.string(self.selectedMuons.getModuleLabel()+" "+caloMET)))
        wmunuPF   = self.analysis.addProducer("WMuNuPF",   self.candCombinerPrototype.clone(decay = cms.string(self.selectedMuons.getModuleLabel()+" "+pfMET)))
        wmunuTC   = self.analysis.addProducer("WMuNuTC",   self.candCombinerPrototype.clone(decay = cms.string(self.selectedMuons.getModuleLabel()+" "+tcMET)))
        self.cloneHistoAnalyzer("WMuNuCands")
        self.histoAnalyzer.wmumetCalo_ = cms.untracked.PSet(src = wmunuCalo, histograms = cms.VPSet(histoTransverseMass.pset()))
        self.histoAnalyzer.wmumetPF_   = cms.untracked.PSet(src = wmunuPF,   histograms = cms.VPSet(histoTransverseMass.pset()))
        self.histoAnalyzer.wmumetTC_   = cms.untracked.PSet(src = wmunuTC,   histograms = cms.VPSet(histoTransverseMass.pset()))

    def addZMassHistos(self):
        from PhysicsTools.PatAlgos.cleaningLayer1.muonCleaner_cfi import cleanPatMuons
        zMassMuons = self.analysis.addAnalysisModule(
            "ZMassMuons",
            selector = cleanPatMuons.clone(
                #preselection = cms.string(zMassVetoMuons),
                src = muons,
                checkOverlaps = cms.PSet(
                    muons = cms.PSet(
                        src                 = self.selectedMuons,
                        algorithm           = cms.string("byDeltaR"),
                        preselection        = cms.string(""),
                        deltaR              = cms.double(0.1),
                        checkRecoComponents = cms.bool(False),
                        pairCut             = cms.string(""),
                        requireNoOverlaps   = cms.bool(True)
                    )
                )
            ),
            counter=False).getSelectorInputTag()

        self.zmumu = self.analysis.addProducer("ZMuMu", self.candCombinerPrototype.clone(decay = cms.string(self.selectedMuons.getModuleLabel()+" "+zMassMuons.getModuleLabel())))
        self.cloneHistoAnalyzer("ZMuMuCands")
        self.histoAnalyzer.zmumu_ = cms.untracked.PSet(src = self.zmumu, histograms = cms.VPSet(histoZMass.pset()))
        self.cloneMultipAnalyzer(name="MultiplicityZMuMuCands")
        self.multipAnalyzer.zMassMuons = self.multipAnalyzer.selMuons.clone(src = zMassMuons)

    def triggerPrimaryVertex(self):
        from HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi import goodPrimaryVertices

        # Trigger
        self.analysis.addTriggerCut(dataVersion, trigger)
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer("Triggered")
            self.cloneMultipAnalyzer()
            self.clonePileupAnalyzer()

        # Select primary vertex
        self.selectedPrimaryVertex = self.analysis.addAnalysisModule("PrimaryVertex",
            selector = goodPrimaryVertices.clone(src = cms.InputTag("firstPrimaryVertex")),
            filter = cms.EDFilter("VertexCountFilter",
                                  src = cms.InputTag("dummy"),
                                  minNumber = cms.uint32(1),
                                  maxNumber = cms.uint32(999)),
            counter=True).getSelectorInputTag()
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer("PrimaryVertex")
            self.cloneMultipAnalyzer()
            self.clonePileupAnalyzer()

    def jetSelection(self, analyze=True):
        # Select jets already here (but do not cut on their number), so we can
        # track the multiplicity through the selections
        self.selectedJets = self.analysis.addSelection("JetSelection", self.selectedJets, jetSelection)
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer("JetSelection", pfJetSrc=self.selectedJets)
            self.cloneMultipAnalyzer(name="MultiplicityAfterJetSelection")
            self.multipAnalyzer.jets.src = self.selectedJets

    def jetId(self, pf=False):
        idstr = jetId
        if pf:
            idstr = jetIdPF

        self.selectedJets = self.analysis.addSelection("JetId", self.selectedJets, idstr)
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer("JetId", pfJetSrc=self.selectedJets)
            self.cloneMultipAnalyzer(name="MultiplicityAfterJetId")
            self.multipAnalyzer.jets.src = self.selectedJets

    def jetMultiplicityFilter(self, analyze=True):
        name = "JetMultiplicityCut"
        self.analysis.addNumberCut(name, self.selectedJets, minNumber=self._njets)
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name)
            self.cloneMultipAnalyzer()
            self.clonePileupAnalyzer()
        return name

    def tightMuonSelection(self):
        name = "GlobalTrackerMuon"
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, tightMuonCut, selector="PATMuonSelector")
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name, muonSrc=self.selectedMuons)
            self.histoAnalyzer.muon_.histograms = cms.VPSet([h.pset() for h in histosGlobal])
            self.cloneMultipAnalyzer(selMuonSrc=self.selectedMuons)
            self.clonePileupAnalyzer()
        return name

    def muonKinematicSelection(self):
        name = "MuonKin"
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, self._ptCut + " && " + etaCut, selector="PATMuonSelector")
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name, muonSrc=self.selectedMuons)
            self.cloneMultipAnalyzer(selMuonSrc=self.selectedMuons)
            self.clonePileupAnalyzer()

    def muonKinematicEtaSelection(self):
        name = "MuonEta"
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, etaCut, selector="PATMuonSelector")
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name, muonSrc=self.selectedMuons)
            self.cloneMultipAnalyzer(selMuonSrc=self.selectedMuons)
            self.clonePileupAnalyzer()

    def muonKinematicPtCustomSelection(self, pt):
        name = "MuonPt%d" % pt
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, "pt() > %d" % pt, selector="PATMuonSelector")
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name, muonSrc=self.selectedMuons)
            self.cloneMultipAnalyzer(selMuonSrc=self.selectedMuons)
            self.clonePileupAnalyzer()
        
    def muonCleaningFromJet(self):
        m = self.muonJetCleanerPrototype.clone(src=self.selectedMuons)
        m.checkOverlaps.jets.src = self.selectedJets
        self.selectedMuons = self.analysis.addAnalysisModule("MuonCleaningFromJet",
            selector = m,
            filter = makeCountFilter(cms.InputTag("dummy"), minNumber=1),
            counter=True).getSelectorInputTag()
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer("MuonJetDR", muonSrc=self.selectedMuons)
            self.cloneMultipAnalyzer(selMuonSrc=self.selectedMuons)
            self.clonePileupAnalyzer()

    def jetCleaningFromMuon(self):
        m = self.jetMuonCleanerPrototype.clone(src=self.selectedJets)
        m.checkOverlaps.muons.src = self.selectedMuons
        self.selectedJets = self.analysis.addAnalysisModule(
            "JetCleaningFromMuon",
            selector = m).getSelectorInputTag()
        if not self.afterOtherCuts:
            self.cloneMultipAnalyzer(name="MultiplicityAfterJetCleaning")
            self.multipAnalyzer.jets.src = self.selectedJets

    def muonQuality(self):
        name = "MuonQuality"
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, qualityCut)
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name, muonSrc=self.selectedMuons)
            self.cloneMultipAnalyzer(selMuonSrc=self.selectedMuons)
            self.clonePileupAnalyzer()
        return name

    def muonImpactParameter(self):
        name = "MuonIP"
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, dbCut)
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name, muonSrc=self.selectedMuons)
            self.cloneMultipAnalyzer(selMuonSrc=self.selectedMuons)
            self.clonePileupAnalyzer()
        return name

    def muonIsolation(self):
        name = "MuonIsolation"
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, self._isolationCut)
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name, muonSrc=self.selectedMuons)
            self.cloneMultipAnalyzer(selMuonSrc=self.selectedMuons)
            self.clonePileupAnalyzer()

    def muonIsolationCustom(self, postfix, cut):
        name = "MuonIsolation"+postfix
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, "%s < %f " % (isolations["sumIsoRel"], cut))
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name, muonSrc=self.selectedMuons)
            self.cloneMultipAnalyzer(selMuonSrc=self.selectedMuons)
            self.clonePileupAnalyzer()

    def muonIsolationWithTau(self):
        name = "MuonIsolationWithTau"
        self.selectedMuons = self.analysis.addAnalysisModule(
            name,
            selector = cms.EDProducer("HPlusCandViewPtrTauIsolationSelector",
                                      candSrc = self.selectedMuons,
                                      tauSrc = cms.InputTag("selectedPatTausShrinkingConePFTau"),
                                      isolationDiscriminator = cms.string("byIsolation"),
                                      deltaR = cms.double(0.15),
                                      minCands = cms.uint32(1)),
            filter = makeCountFilter(cms.InputTag("dummy"), 1),
            counter=True).getSelectorInputTag()
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name, muonSrc=self.selectedMuons)
            self.cloneMultipAnalyzer(selMuonSrc=self.selectedMuons)
            self.clonePileupAnalyzer()

    def muonVertexDiff(self):
        name = "MuonVertexDiff"
        self.selectedMuons = self.analysis.addAnalysisModule(name,
            selector = cms.EDFilter("HPlusCandViewPtrVertexZSelector",
                                    src = self.selectedMuons,
                                    vertexSrc = self.selectedPrimaryVertex,
                                    maxZ = cms.double(maxVertexZ)),
            filter = makeCountFilter(cms.InputTag("dummy"), minNumber=1),
            counter = True).getSelectorInputTag()
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name, muonSrc=self.selectedMuons)
            self.cloneMultipAnalyzer(selMuonSrc=self.selectedMuons)
            self.clonePileupAnalyzer()
        return name

    def muonLargestPt(self):
        name = "MuonLargestPt"
        self.selectedMuons = self.analysis.addAnalysisModule(name,
            selector = cms.EDFilter("HPlusLargestPtCandViewPtrSelector",
                src = self.selectedMuons,
                filter = cms.bool(False),
                maxNumber = cms.uint32(1))).getSelectorInputTag()
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name, muonSrc=self.selectedMuons)
        return name

    def muonVeto(self):
        name = "MuonVeto"
        vetoMuons = self.analysis.addCut(name, muons, muonVeto, minNumber=0, maxNumber=1)
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name)
            self.cloneMultipAnalyzer()
            self.clonePileupAnalyzer()
        return name

    def electronVeto(self):
        name = "ElectronVeto"
        vetoElectrons = self.analysis.addCut(name, electrons, electronVeto, minNumber=0, maxNumber=0)
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name)
            self.cloneMultipAnalyzer()
            self.clonePileupAnalyzer()
        return name

    def zMassVeto(self):
        name = "ZMassVeto"
        vetoZCands = self.analysis.addCut(name, self.zmumu, zMassveto, minNumber=0, maxNumber=0)
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name)
            self.cloneMultipAnalyzer()
            self.clonePileupAnalyzer()
        return name

    def metCut(self):
        name = "METCut"
        selectedMET = self.analysis.addCut(name, met, self._metCut)
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name)
            self.cloneMultipAnalyzer()
            self.clonePileupAnalyzer()
        return name

    

    def _topMuJetRef(self):
        self.triggerPrimaryVertex()
        self.jetSelection()
        if self.doJetId:
            self.jetId()

        self.tightMuonSelection()
        if not self.afterOtherCuts:
            self.muonKinematicSelection()

        self.muonCleaningFromJet()
        self.muonQuality()
        self.muonImpactParameter()

        if not self.afterOtherCuts:
            self.muonIsolation()

        self.muonVertexDiff()

        if not self.afterOtherCuts:
            self.addWtransverseMassHistos()
            self.addZMassHistos()

        self.muonVeto()
        name = self.electronVeto()
        if self.afterOtherCuts:
            self.addAfterOtherCutsAnalyzer(name)
           
        name = self.jetMultiplicityFilter()
        if self.afterOtherCuts:
            self.addAfterOtherCutsAnalyzer(name)
            
    def topMuJetRef(self):
        self._topMuJetRef()
        self.createAnalysisPath()

    def topMuJetRefMet(self):
        self._topMuJetRef()
        name = self.metCut()
        if self.afterOtherCuts:
            self.addAfterOtherCutsAnalyzer(name)
        self.createAnalysisPath()

    def muonSelection(self):
        self.triggerPrimaryVertex()
        self.jetSelection()
        if self.doJetId:
            self.jetId()

        self.tightMuonSelection()

        if not self.afterOtherCuts:
            self.muonKinematicSelection()

        self.muonCleaningFromJet()
        self.muonQuality()
        self.muonImpactParameter()
        self.muonVertexDiff()
        name = self.muonLargestPt()

        if not self.afterOtherCuts:
            self.addWtransverseMassHistos()
            self.addZMassHistos()
        else:
            self.addAfterOtherCutsAnalyzer(name)
            
        name = self.jetMultiplicityFilter()
        if self.afterOtherCuts:
            self.addAfterOtherCutsAnalyzer(name)

        name = self.metCut()
        if self.afterOtherCuts:
            self.addAfterOtherCutsAnalyzer(name)

        self.createAnalysisPath()

    def muonSelectionPF(self):
        self.triggerPrimaryVertex()
        self.tightMuonSelection()

        if not self.afterOtherCuts:
            self.muonKinematicSelection()

        self.muonQuality()
        self.muonImpactParameter()
        self.muonVertexDiff()
        if self.doIsolationWithTau:
            self.muonIsolationWithTau()
        name = self.muonLargestPt()

        if not self.afterOtherCuts:
            self.addWtransverseMassHistos()
            self.addZMassHistos()
        else:
            self.addAfterOtherCutsAnalyzer(name)

        self.jetCleaningFromMuon()
        self.jetSelection()
        if self.doJetId:
            self.jetId(pf=True)

        name = self.jetMultiplicityFilter()
        if self.afterOtherCuts:
            self.addAfterOtherCutsAnalyzer(name)

        name = self.metCut()
        if self.afterOtherCuts:
            self.addAfterOtherCutsAnalyzer(name)

        self.createAnalysisPath()

    def muonLast(self):
        self.triggerPrimaryVertex()
        self.jetSelection()
        if self.doJetId:
            self.jetId()
        self.jetMultiplicityFilter()
        self.muonCleaningFromJet()

        self.tightMuonSelection()
        #self.muonKinematicSelection()
        self.muonKinematicEtaSelection()
        self.muonKinematicPtCustomSelection(5)
        self.muonKinematicPtCustomSelection(10)
        self.muonKinematicPtCustomSelection(15)
        self.muonKinematicPtCustomSelection(20)
        self.muonKinematicPtCustomSelection(25)
        self.muonKinematicPtCustomSelection(30)
        self.muonKinematicPtCustomSelection(35)
        self.muonKinematicPtCustomSelection(40)
        self.muonQuality()
        self.muonImpactParameter()
        self.muonVertexDiff()
        self.muonIsolationCustom("050", 0.5)
        self.muonIsolationCustom("015", 0.15)
        self.muonIsolationCustom("010", 0.1)
        self.muonIsolationCustom("005", 0.05)
        self.muonVeto()
        self.electronVeto()

        self.createAnalysisPath()

    def noMuon(self):
        self.triggerPrimaryVertex()
        self.jetSelection()
        if self.doJetId:
            self.jetId()
        self.jetMultiplicityFilter()
        self.metCut()

        self.createAnalysisPath()

    def noMuonPF(self):
        self.triggerPrimaryVertex()
        self.jetSelection()
        if self.doJetId:
            self.jetId(pf=True)
        self.jetMultiplicityFilter()
        self.metCut()

        self.createAnalysisPath()

def createAnalysis(name, postfix="", **kwargs):
    a = MuonAnalysis(process, prefix=name+postfix, **kwargs)
    getattr(a, name)()
    #a = MuonAnalysis(process, prefix=name+postfix+"JetId", doJetId=True, **kwargs)
    #getattr(a, name)()
    if not "doIsolationWithTau" in kwargs:
        a = MuonAnalysis(process, prefix=name+postfix+"IsoTau", doIsolationWithTau=True, **kwargs)
        getattr(a, name)()
    a = MuonAnalysis(process, prefix=name+postfix+"Aoc", afterOtherCuts=True, **kwargs)
    getattr(a, name)()

def createAnalysis2(**kwargs):
    createAnalysis("topMuJetRefMet", doIsolationWithTau=False, **kwargs)

    postfix = ""
    if "postfix" in kwargs:
        postfix = kwargs["postfix"]
        del kwargs["postfix"]

    #for pt, met, njets in [(30, 20, 1), (30, 20, 2),
    #                       (30, 20, 3), (30, 30, 3), (30, 40, 3),
    #                       (40, 20, 3), (40, 30, 3), (40, 40, 3)]:
    for pt, met, njets in [(30, 20, 1), (30, 20, 2),
                           (30, 20, 3), (40, 20, 3)]:
        kwargs["postfix"] = "Pt%dMet%dNJets%d%s" % (pt, met, njets, postfix)
        kwargs["muonPtCut"] = pt
        kwargs["metCut"] = met
        kwargs["njets"] = njets
        kwargs["jets"] = jetsPF
        kwargs["doJetId"] = True
        createAnalysis("muonSelectionPF", **kwargs)

createAnalysis2()
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

    createAnalysis2(postfix="Wmunu", beginSequence=process.wMuNuSequence)
    createAnalysis2(postfix="WOther", beginSequence=process.wOtherSequence)


#print process.dumpPython()

