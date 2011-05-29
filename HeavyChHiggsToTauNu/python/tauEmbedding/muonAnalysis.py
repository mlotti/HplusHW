import FWCore.ParameterSet.Config as cms
import HiggsAnalysis.HeavyChHiggsToTauNu.HChTools as HChTools

# PfAllParticleIso=3,PfChargedHadronIso=4, PfNeutralHadronIso=5, PfGammaIso=6, 
isolations0304 = {
    # Detector iso
    "trackIso": "isolationR03().sumPt",
    "caloIso": "isolationR03().emEt+isolationR03().hadEt",
    # 'standard' PF isolation
    "pfChargedIso": "isoDeposit('PfChargedHadronIso').depositWithin(0.4)",
    "pfNeutralIso": "isoDeposit('PfNeutralHadronIso').depositWithin(0.4)",
    "pfGammaIso": "isoDeposit('PfGammaIso').depositWithin(0.4)",
}
isolations05 = {
    # Detector iso
    "trackIso": "isolationR05().sumPt",
    "caloIso": "isolationR05().emEt+isolationR05().hadEt",
    # 'standard' PF isolation
    "pfChargedIso": "isoDeposit('PfChargedHadronIso').depositWithin(0.5)",
    "pfNeutralIso": "isoDeposit('PfNeutralHadronIso').depositWithin(0.5)",
    "pfGammaIso": "isoDeposit('PfGammaIso').depositWithin(0.5)",
}

isolations = isolations0304
#isolations = isolations05
isolations["sumIso"] = "%s+%s" % (isolations["trackIso"], isolations["caloIso"])
isolations["pfSumIso"] = "%s+%s+%s" % (isolations["pfChargedIso"], isolations["pfNeutralIso"], isolations["pfGammaIso"])
for key, value in isolations.items():
    isolations[key+"Rel"] = "(%s)/pt" % value

tauIsolations = {
    "tauTightIso": "userInt('byTightOccupancy')",
    "tauMediumIso": "userInt('byMediumOccupancy')",
    "tauLooseIso": "userInt('byLooseOccupancy')",
    "tauVLooseIso": "userInt('byVLooseOccupancy')",

    "tauTightSc015Iso": "userInt('byTightSc015Occupancy')",
    "tauTightSc02Iso": "userInt('byTightSc02Occupancy')",
    "tauTightIc04Iso": "userInt('byTightIc04Occupancy')",
    "tauTightSc015Ic04Iso": "userInt('byTightSc015Ic04Occupancy')",
    "tauTightSc02Ic04Iso": "userInt('byTightSc02Ic04Occupancy')",

    "tauTightSc0Iso": "userInt('byTightSc0Occupancy')",
    "tauTightSc0Ic04Iso": "userInt('byTightSc0Ic04Occupancy')",
    "tauTightSc0Ic04NoqIso": "userInt('byTightSc0Ic04NoqOccupancy')",
    }
for key, value in tauIsolations.items():
    userFloat = value.replace("userInt", "userFloat")
    base = key.replace("Iso", "")
    tauIsolations[base+"SumPtIso"] = userFloat.replace("Occupancy", "SumPt")
    tauIsolations[base+"SumPtIsoRel"] = "(%s)/pt()" % userFloat.replace("Occupancy", "SumPt")
    tauIsolations[base+"MaxPtIso"] = userFloat.replace("Occupancy", "MaxPt")
isolations.update(tauIsolations)

# Define the histograms
histoPt = HChTools.Histo("pt", "pt()", min=0., max=800., nbins=800, description="pt (GeV/c)")
histoEta = HChTools.Histo("eta", "eta()", min=-3, max=3, nbins=120, description="eta")
histoPhi = HChTools.Histo("phi", "phi()", min=-3.5, max=3.5, nbins=70, description="phi")

histoIsos = {}
for name, value in isolations.iteritems():
    h = None
    if "IsoRel" in name or "SumPtRel" in name:
        h = HChTools.Histo(name, value, min=0, max=0.5, nbins=100, description=name)
        histoIsos[name+"Full"] = HChTools.Histo(name+"Full", value, min=0, max=5.0, nbins=500, description=name)
    else:
        h = HChTools.Histo(name, value, min=0, max=100.0, nbins=100, description=name)
    histoIsos[name] = h
    

histoDB = HChTools.Histo("trackDB", "dB()", min=-0.1, max=0.1, nbins=50, description="Track ip @ PV (cm)")
histoNhits = HChTools.Histo("trackNhits", "innerTrack().numberOfValidHits()", min=0, max=60, nbins=60, description="N(valid global hits)")
histoChi2 = HChTools.Histo("trackNormChi2", "globalTrack().normalizedChi2()", min=0, max=20, nbins=100, description="Track norm chi2")

histoMet = HChTools.Histo("et", "et()", min=0., max=400., nbins=400, description="MET (GeV)")

histoTransverseMass = HChTools.Histo("tmass", "sqrt((daughter(0).pt+daughter(1).pt)*(daughter(0).pt+daughter(1).pt)-pt*pt)",
                                     min=0, max=400, nbins=400, description="W transverse mass")
histoZMass = HChTools.Histo("mass", "mass()", min=0, max=400, nbins=400, description="Z mass")

histoGenMother = HChTools.Histo("genMother", "abs(userInt('genMotherPdgId'))", min=0, max=100, nbins=100, description="Muon mother pdgid")
histoGenGrandMother = HChTools.Histo("genGrandMother", "abs(userInt('genGrandMotherPdgId'))", min=0, max=100, nbins=100, description="Muon grandmother pdgid")

histosBeginning = [histoPt, histoEta, histoPhi, histoGenMother, histoGenGrandMother] + histoIsos.values()
histosTrack = [histoDB, histoNhits, histoChi2]
histosJet = [histoPt, histoEta, histoPhi]
histosMet = [histoMet]

# Class to wrap the analysis steps, and to have methods for the defined analyses
class MuonAnalysis:
    def __init__(self, process, dataVersion, additionalCounters, 
                 prefix="", beginSequence=None, afterOtherCuts=False,
                 trigger=None,
                 muons="selectedPatMuons", allMuons="selectedPatMuons", muonPtCut=30,
                 doIsolationWithTau=False, isolationWithTauDiscriminator="byTightIsolation",
                 doMuonIsolation=False, muonIsolation="sumIsoRel", muonIsolationCut=0.05,
                 electrons="selectedPatElectrons",
                 met="patMETsPF", metCut=20,
                 jets="selectedPatJetsAK5PF", njets=3,
                 weightSrc=None):
        self.process = process
        self.dataVersion = dataVersion
        self.prefix = prefix
        self.afterOtherCuts = afterOtherCuts
        self.doIsolationWithTau = doIsolationWithTau
        self.doMuonIsolation = doMuonIsolation
        self._trigger = trigger
        self._muons = cms.InputTag(muons)
        self._allMuons = cms.InputTag(allMuons)
        self._ptCut = "pt() > %d" % muonPtCut
        self._etaCut = "abs(eta()) < 2.1"
        self._electrons = electrons
        self._met = met
        self._metCut = "et() > %d" % metCut
        self._njets = njets
        self._jets = cms.InputTag(jets)
        self._muonIsolation = muonIsolation
        self._isolationCut = "%s < %f" % (isolations[muonIsolation], muonIsolationCut)
        self._isolationWithTauDiscriminator = isolationWithTauDiscriminator

        if self._trigger == None:
            raise Exception("Must specify trigger!")

        self.analysis = HChTools.Analysis(self.process, "analysis", prefix, additionalCounters=additionalCounters, weightSrc=weightSrc)
        #self.analysis.getCountAnalyzer().printMainCounter = cms.untracked.bool(True)
        #self.analysis.getCountAnalyzer().printSubCounters = cms.untracked.bool(True)
        #self.analysis.getCountAnalyzer().printAvailableCounters = cms.untracked.bool(True)

        if beginSequence != None:
            self.analysis.appendToSequence(beginSequence)
        self.multipName = "Multiplicity"

        self.selectedMuons = cms.InputTag(muons)
        self.selectedJets = self._jets

        # Setup the analyzers
        if not self.afterOtherCuts:
            self.histoAnalyzer = self.analysis.addMultiHistoAnalyzer("AllMuons", [
                    ("muon_", self.selectedMuons, histosBeginning),
                    ("jet_", self.selectedJets, histosJet),
                    ("met_", cms.InputTag(met), histosMet)])
            self.multipAnalyzer = self.analysis.addAnalyzer(self.multipName, cms.EDAnalyzer("HPlusCandViewMultiplicityAnalyzer",
                    allMuons = cms.untracked.PSet(
                        src = self.selectedMuons,
                        min = cms.untracked.int32(0),
                        max = cms.untracked.int32(10),
                        nbins = cms.untracked.int32(10)
                    ),
                    selMuons = cms.untracked.PSet(
                        src = self.selectedMuons,
                        min = cms.untracked.int32(0),
                        max = cms.untracked.int32(10),
                        nbins = cms.untracked.int32(10)
                    ),
                    jets = cms.untracked.PSet(
                        src = self.selectedJets,
                        min = cms.untracked.int32(0),
                        max = cms.untracked.int32(20),
                        nbins = cms.untracked.int32(20)
                    )
            ))
            if self.weightSrc != None:
                self.multipAnalyzer.weights = cms.untracked.InputTag(self.weightSrc)
    
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
                    histoEta.pset().clone(cut=cms.untracked.string(self._etaCut)),
                )
            )
            if self.weightSrc != None:
                self.afterOtherCutsModule.weights = cms.untracked.InputTag(self.weightSrc)
            self.afterOtherCutsModuleIso = self.afterOtherCutsModule.clone()
            self.afterOtherCutsModuleIso.histograms.append(histoIsos[muonIsolation].pset().clone(
                    cut=cms.untracked.string(self._isolationCut)
            ))
        
    ########################################
    # Internal methods
    def cloneHistoAnalyzer(self, name, **kwargs):
        self.histoAnalyzer = self.analysis.addCloneAnalyzer(name, self.histoAnalyzer)
        if "muonSrc" in kwargs:
            self.histoAnalyzer.muon_.src = kwargs["muonSrc"]
        if "jetSrc" in kwargs:
            self.histoAnalyzer.jet_.src = kwargs["jetSrc"]
        if "appendMuonHistos" in kwargs:
            self.histoAnalyzer.muon_.histograms.extend([h.pset() for h in kwargs["appendMuonHistos"]])

    def cloneMultipAnalyzer(self, **kwargs):
        name = kwargs.get("name", self.multipName)
        self.multipAnalyzer = self.analysis.addCloneAnalyzer(name, self.multipAnalyzer)
        if "muonSrc" in kwargs:
            self.multipAnalyzer.selMuons.src = kwargs["muonSrc"]
        if "jetSrc" in kwargs:
            self.multipAnalyzer.jets.src = kwargs["jetSrc"]

    def cloneAnalyzers(self, name, **kwargs):
        if self.afterOtherCuts:
            return False

        self.cloneHistoAnalyzer(name, **kwargs)
        #self.cloneMultipAnalyzer(name=self.multipName+name, **kwargs)
        return True
        

    def addAfterOtherCutsAnalyzer(self, prefix):
        self.analysis.addAnalyzer(prefix+"AfterOtherCuts", self.afterOtherCutsModule.clone(src=self.selectedMuons))
        self.analysis.addAnalyzer(prefix+"AfterOtherCutsIso", self.afterOtherCutsModuleIso.clone(src=self.selectedMuons))

    def addWtransverseMassHistos(self):
        wmumet   = self.analysis.addProducer("WMuMet",   self.candCombinerPrototype.clone(decay = cms.string(self.selectedMuons.getModuleLabel()+" "+self._met)))
        self.cloneHistoAnalyzer("WMuMetCands")
        self.histoAnalyzer.wmumet_   = cms.untracked.PSet(src = wmumet,   histograms = cms.VPSet(histoTransverseMass.pset()))

    def addZMassHistos(self):
        from PhysicsTools.PatAlgos.cleaningLayer1.muonCleaner_cfi import cleanPatMuons
        zMassMuons = self.analysis.addAnalysisModule(
            "ZMassMuons",
            selector = cleanPatMuons.clone(
                #preselection = cms.string(zMassVetoMuons),
                src = self._muons,
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

    def createAnalysisPath(self):
        setattr(self.process, self.prefix+"analysisPath", cms.Path(
                self.process.commonSequence *
                self.analysis.getSequence()
        ))

    ########################################
    # Analysis steps

    # Trigger nad PV
    def triggerPrimaryVertex(self):
        from HiggsAnalysis.HeavyChHiggsToTauNu.HChPrimaryVertex_cfi import goodPrimaryVertices

        # Trigger
        self.analysis.addTriggerCut(self.dataVersion, self._trigger)
        self.cloneAnalyzers("Triggered")

        # Select primary vertex
        self.selectedPrimaryVertex = self.analysis.addAnalysisModule("PrimaryVertex",
            selector = goodPrimaryVertices.clone(src = cms.InputTag("firstPrimaryVertex")),
            filter = cms.EDFilter("VertexCountFilter",
                                  src = cms.InputTag("dummy"),
                                  minNumber = cms.uint32(1),
                                  maxNumber = cms.uint32(999)),
            counter=True).getSelectorInputTag()
        self.cloneAnalyzers("PrimaryVertex")

    # Jet selections
    def jetSelection(self, analyze=True):
        # Select jets already here (but do not cut on their number), so we can
        # track the multiplicity through the selections
        jetSelection = "pt() > 30 && abs(eta()) < 2.4"
        jetId  = "numberOfDaughters() > 1 && chargedEmEnergyFraction() < 0.99 && neutralHadronEnergyFraction() < 0.99 && neutralEmEnergyFraction < 0.99 && chargedHadronEnergyFraction() > 0 && chargedMultiplicity() > 0"

        self.selectedJets = self.analysis.addSelection("JetSelection", self.selectedJets, jetSelection+" && "+jetId)
        self.cloneAnalyzers("JetSelection", jetSrc=self.selectedJets)

    def jetMultiplicityFilter(self, analyze=True):
        name = "JetMultiplicityCut"
        self.analysis.addNumberCut(name, self.selectedJets, minNumber=self._njets)
        self.cloneAnalyzers(name)
        return name

    # MET cut
    def metCut(self):
        name = "METCut"
        selectedMET = self.analysis.addCut(name, cms.InputTag(self._met), self._metCut)
        self.cloneAnalyzers(name)
        return name


    # Muon selection
    def muonGlobalTrackerSelection(self):
        name = "GlobalTrackerMuon"
        selection = "isGlobalMuon() && isTrackerMuon()"
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, selection, selector="PATMuonSelector")
        self.cloneAnalyzers(name, muonSrc=self.selectedMuons, appendMuonHistos=histosTrack)
        return name

    def muonKinematicSelection(self):
        name = "MuonKin"
        selection = self._ptCut+" && "+self._etaCut
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, selection, selector="PATMuonSelector")
        self.cloneAnalyzers(name, muonSrc=self.selectedMuons)

    def muonKinematicEtaSelection(self):
        name = "MuonEta"
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, self._etaCut, selector="PATMuonSelector")
        self.cloneAnalyzers(name, muonSrc=self.selectedMuons)

    def muonKinematicPtCustomSelection(self, pt):
        name = "MuonPt%d" % pt
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, "pt() > %d" % pt, selector="PATMuonSelector")
        self.cloneAnalyzers(name, self.selectedMuons)
        
    def muonCleaningFromJet(self):
        m = self.muonJetCleanerPrototype.clone(src=self.selectedMuons)
        m.checkOverlaps.jets.src = self.selectedJets
        self.selectedMuons = self.analysis.addAnalysisModule("MuonCleaningFromJet",
            selector = m,
            filter = HChTools.makeCountFilter(cms.InputTag("dummy"), minNumber=1),
            counter=True).getSelectorInputTag()
        self.cloneAnalyzers("MuonJetDR", muonSrc=self.selectedMuons)

    def jetCleaningFromMuon(self):
        m = self.jetMuonCleanerPrototype.clone(src=self.selectedJets)
        m.checkOverlaps.muons.src = self.selectedMuons
        self.selectedJets = self.analysis.addAnalysisModule(
            "JetCleaningFromMuon",
            selector = m).getSelectorInputTag()

        if not self.afterOtherCuts:
            self.cloneMultipAnalyzer(name="MultiplicityJetCleaning")
            self.multipAnalyzer.jets.src = self.selectedJets

    def muonQuality(self):
        name = "MuonQuality"
        qualityCut = "muonID('GlobalMuonPromptTight')"
        qualityCut += " && innerTrack().numberOfValidHits() > 10"
        qualityCut += " && innerTrack().hitPattern().pixelLayersWithMeasurement() >= 1"
        qualityCut += " && numberOfMatches() > 1"
        # These two are included in the GlobalMuonPromptThigh ID
        #qualityCut += "globalTrack().normalizedChi2() < 10.0 && " +
        #qualityCut += "globalTrack().hitPattern().numberOfValidMuonHits () > 0 && " 
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, qualityCut, selector="PATMuonViewPtrSelector")
        self.cloneAnalyzers(name, muonSrc=self.selectedMuons)
        return name

    def muonImpactParameter(self):
        name = "MuonIP"
        dbCut = "abs(dB()) < 0.02" # w.r.t. beamSpot (note process.patMuons.usePV = False, PATMuonProducer takes beam spot from the event, so this could be safe also for 36X data
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, dbCut, selector="PATMuonViewPtrSelector")
        self.cloneAnalyzers(name, muonSrc=self.selectedMuons)
        return name

    def muonIsolation(self):
        name = "MuonIsolation"
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, self._isolationCut, selector="PATMuonViewPtrSelector")
        self.cloneAnalyzers(name, muonSrc=self.selectedMuons)

    def muonIsolationCustom(self, postfix, cut):
        name = "MuonIsolation"+postfix
        self.selectedMuons = self.analysis.addCut(name, self.selectedMuons, "%s < %f " % (isolations[self.muonIsolation], cut), selector="PATMuonViewPtrSelector")
        self.cloneAnalyzers(name, muonSrc=self.selectedMuons)

    def muonIsolationWithTau(self):
        name = "MuonIsolationWithTau"
        self.selectedMuons = self.analysis.addAnalysisModule(
            name,
            selector = cms.EDProducer("HPlusTauIsolationPATMuonViewPtrSelector",
                                      candSrc = self.selectedMuons,
#                                      tauSrc = cms.InputTag("selectedPatTausShrinkingConePFTau"),
                                      tauSrc = cms.InputTag("selectedPatTausHpsPFTau"),
                                      isolationDiscriminator = cms.string(self._isolationWithTauDiscriminator),
                                      againstMuonDiscriminator = cms.string("againstMuonLoose"),
                                      deltaR = cms.double(0.15),
                                      minCands = cms.uint32(1)),
            filter = HChTools.makeCountFilter(cms.InputTag("dummy"), 1),
            counter=True).getSelectorInputTag()
        self.cloneAnalyzers(name, muonSrc=self.selectedMuons)

    def muonVertexDiff(self):
        name = "MuonVertexDiff"
        maxVertexZ = 1.0 # cm
        self.selectedMuons = self.analysis.addAnalysisModule(name,
            selector = cms.EDFilter("HPlusPATMuonViewPtrVertexZSelector",
                                    src = self.selectedMuons,
                                    vertexSrc = self.selectedPrimaryVertex,
                                    maxZ = cms.double(maxVertexZ)),
            filter = HChTools.makeCountFilter(cms.InputTag("dummy"), minNumber=1),
            counter = True).getSelectorInputTag()
        self.cloneAnalyzers(name, muonSrc=self.selectedMuons)
        return name

    def muonLargestPt(self):
        name = "MuonLargestPt"
        self.selectedMuons = self.analysis.addAnalysisModule(name,
            selector = cms.EDFilter("HPlusLargestPtPATMuonViewPtrSelector",
                src = self.selectedMuons,
                filter = cms.bool(False),
                maxNumber = cms.uint32(1))).getSelectorInputTag()
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name, muonSrc=self.selectedMuons)
        return name

    def muonMostIsolated(self):
        name = "MuonMostIsolated"
        self.selectedMuons = self.analysis.addAnalysisModule(name,
            selector = cms.EDFilter("HPlusSmallestRelIsoPATMuonViewPtrSelector",
                src = self.selectedMuons,
                filter = cms.bool(False),
                maxNumber = cms.uint32(1))).getSelectorInputTag()
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name, muonSrc=self.selectedMuons)
        return name

    def muonExactlyOne(self):
        name = "MuonExactlyOne"
        self.analysis.addAnalysisModule(name,
            filter = HChTools.makeCountFilter(self.selectedMuons, minNumber=1, maxNumber=1),
            counter = True
        )
        if not self.afterOtherCuts:
            self.cloneHistoAnalyzer(name)
        return name

    # Vetoes
    def muonVeto(self):
        name = "MuonVeto"
        muonVeto = "isGlobalMuon && pt > 10. && abs(eta) < 2.5 && "+isolations["sumIsoRel"]+" < 0.2"
        vetoMuons = self.analysis.addCut(name, self._muons, muonVeto, minNumber=0, maxNumber=1)
        self.cloneAnalyzers(name)
        return name

    def muonVetoSignalAnalysis(self):
        name = "MuonVeto"
        m = self.muonJetCleanerPrototype.clone(
            src = self._allMuons
        )
        m.checkOverlaps.muons = m.checkOverlaps.jets.clone(
            src = self.selectedMuons,
            deltaR = 0.1
        )
        del m.checkOverlaps.jets

        from HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff import GlobalMuonVeto
        am = self.analysis.addAnalysisModule(name,
            selector = m,
            filter = cms.EDFilter("HPlusGlobalMuonVetoFilter",
                vertexSrc = cms.InputTag("firstPrimaryVertex"),
                GlobalMuonVeto=GlobalMuonVeto.clone()
            ),
            counter=True)
        am.setFilterSrcToSelector(lambda f: f.GlobalMuonVeto.MuonCollectionName)
        self.cloneAnalyzers(name)
#        self.multipAnalyzer.cleanedMuons = self.multipAnalyzer.selMuons.clone(src = am.selectorName)
        return name

    def electronVetoSignalAnalysis(self):
        name = "ElectronVeto"
        from HiggsAnalysis.HeavyChHiggsToTauNu.HChSignalAnalysisParameters_cff import GlobalElectronVeto
        self.analysis.addAnalysisModule(name,
            filter = cms.EDFilter("HPlusGlobalElectronVetoFilter",
                GlobalElectronVeto=GlobalElectronVeto.clone()
            ),
            counter=True)
        self.cloneAnalyzers(name)
        return name

    def electronVeto(self):
        name = "ElectronVeto"
        electronVeto = "et() > 15 && abs(eta()) < 2.5 && (dr03TkSumPt()+dr03EcalRecHitSumEt()+dr03HcalTowerSumEt())/et() < 0.2"
        vetoElectrons = self.analysis.addCut(name, cms.InputTag(self._electrons), electronVeto, minNumber=0, maxNumber=0)
        self.cloneAnalyzers(name)
        return name

    def zMassVeto(self):
        name = "ZMassVeto"
        zMassVeto = "76 < mass() && mass < 106"
        vetoZCands = self.analysis.addCut(name, self.zmumu, zMassveto, minNumber=0, maxNumber=0)
        self.cloneAnalyzers(name)
        return name

    ########################################
    # Selections

    # Top group mu+jet reference selection
    def topMuJetRef(self):
        self.triggerPrimaryVertex()
        self.jetSelection()

        self.muonGlobalTrackerSelection()
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
            
    def topMuJetRefMet(self):
        self.topMuJetRef()
        name = self.metCut()
        if self.afterOtherCuts:
            self.addAfterOtherCutsAnalyzer(name)

    # Our selection
    def muonSelectionPF(self):
        self.triggerPrimaryVertex()
        self.muonGlobalTrackerSelection()

        if not self.afterOtherCuts:
            self.muonKinematicSelection()

        self.muonQuality()
        self.muonImpactParameter()
        #self.muonVertexDiff()
        if self.doMuonIsolation:
            if self.doIsolationWithTau:
                self.muonIsolationWithTau()
            else:
                self.muonIsolation()
            self.muonExactlyOne()
        else:
            #self.muonLargestPt()
            self.muonMostIsolated()

        name = self.muonVetoSignalAnalysis()
        name = self.electronVetoSignalAnalysis()

        if not self.afterOtherCuts:
            self.addWtransverseMassHistos()
            self.addZMassHistos()
        else:
            self.addAfterOtherCutsAnalyzer(name)

        self.jetCleaningFromMuon()
        self.jetSelection()

        name = self.jetMultiplicityFilter()
        if self.afterOtherCuts:
            self.addAfterOtherCutsAnalyzer(name)

        name = self.metCut()
        if self.afterOtherCuts:
            self.addAfterOtherCutsAnalyzer(name)

def createAnalysis(process, dataVersion, additionalCounters, name, **kwargs):
    a = MuonAnalysis(process, dataVersion, additionalCounters, **kwargs)
    getattr(a, name)()
    a.createAnalysisPath()
