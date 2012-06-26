#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurementBasic.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TNamed.h"

namespace HPlus {
  QCDMeasurementBasic::QCDMeasurementBasic(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fEventWeight(eventWeight),
    fHistoWrapper(eventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
    fDeltaPhiCutValue(iConfig.getUntrackedParameter<double>("deltaPhiTauMET")),
    fTopRecoName(iConfig.getUntrackedParameter<std::string>("topReconstruction")),
    fTauPtBinLowEdges(iConfig.getUntrackedParameter<std::vector<double> >("factorisationTauPtBinLowEdges")),
    fTauEtaBinLowEdges(iConfig.getUntrackedParameter<std::vector<double> >("factorisationTauEtaBinLowEdges")),
    fNVerticesBinLowEdges(iConfig.getUntrackedParameter<std::vector<int> >("factorisationNVerticesBinLowEdges")),
    fTransverseMassRange(iConfig.getUntrackedParameter<std::vector<double> >("factorisationTransverseMassRange")),
    fFullMassRange(iConfig.getUntrackedParameter<std::vector<double> >("factorisationFullMassRange")),
    fAllCounter(eventCounter.addCounter("allEvents")),
    fTriggerCounter(eventCounter.addCounter("Trigger_and_HLT_MET")),
    fPrimaryVertexCounter(eventCounter.addCounter("PrimaryVertex")),
    fTausExistCounter(eventCounter.addCounter("TauCandSelection")),
    fControlPlotsMultipleTausCounter(eventCounter.addCounter("Rejected in ctrl plots (multiple taus)")),
    fVetoTauCounter(eventCounter.addCounter("VetoTauSelection")),
    fElectronVetoCounter(eventCounter.addCounter("GlobalElectronVeto")),
    fMuonVetoCounter(eventCounter.addCounter("GlobalMuonVeto")),
    //fNonIsolatedElectronVetoCounter(eventCounter.addCounter("NonIsolatedElectronVeto")),
    //fNonIsolatedMuonVetoCounter(eventCounter.addCounter("NonIsolatedMuonVeto")),
    fNJetsCounter(eventCounter.addCounter("JetSelection")),
    fMETCounter(eventCounter.addCounter("MET")),
    fBTaggingCounter(eventCounter.addCounter("bTagging")),
    fDeltaPhiTauMETCounter(eventCounter.addCounter("DeltaPhiTauMET")),
    fMaxDeltaPhiJetMETCounter(eventCounter.addCounter("maxDeltaPhiJetMET")),
    fTopSelectionCounter(eventCounter.addCounter("top selection")),
    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, fHistoWrapper),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, fHistoWrapper),
    fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, fHistoWrapper),
    fVetoTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("vetoTauSelection"), eventCounter, fHistoWrapper),
    fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, fHistoWrapper),
    //fNonIsolatedElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("NonIsolatedElectronVeto"), eventCounter, fHistoWrapper),
    fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, fHistoWrapper),
    //fNonIsolatedMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("NonIsolatedMuonVeto"), eventCounter, fHistoWrapper),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, fHistoWrapper),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, fHistoWrapper, "MET"),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, fHistoWrapper),
    //fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, fHistoWrapper),
    //fForwardJetVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("forwardJetVeto"), eventCounter, fHistoWrapper),
    fGenparticleAnalysis(iConfig.getUntrackedParameter<edm::ParameterSet>("GenParticleAnalysis"), eventCounter, fHistoWrapper),
    fTopSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topSelection"), eventCounter, fHistoWrapper),
    fTopChiSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topChiSelection"), eventCounter, fHistoWrapper),
    fTopWithBSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithBSelection"), eventCounter, fHistoWrapper),
    fTopWithWSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("topWithWSelection"), eventCounter, fHistoWrapper),
    fBjetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("bjetSelection"), eventCounter, fHistoWrapper),
    fEvtTopology(iConfig.getUntrackedParameter<edm::ParameterSet>("EvtTopology"), eventCounter, fHistoWrapper),
    fFullHiggsMassCalculator(eventCounter, fHistoWrapper),
    fVertexWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("vertexWeightReader")),
    fFakeTauIdentifier(fHistoWrapper, "TauCandidates"),
    fTriggerEfficiencyScaleFactor(iConfig.getUntrackedParameter<edm::ParameterSet>("triggerEfficiencyScaleFactor"), fHistoWrapper),
    fTree(iConfig.getUntrackedParameter<edm::ParameterSet>("Tree"), fBTagging.getDiscriminator()),
    fSFUncertaintyAfterStandardSelections(fHistoWrapper, "AfterStandardSelections")
    // fTriggerEmulationEfficiency(iConfig.getUntrackedParameter<edm::ParameterSet>("TriggerEmulationEfficiency"))
    // ftransverseMassCutCount(eventCounter.addCounter("transverseMass cut")),
   {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms
    hVerticesBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesBeforeWeight", "Number of vertices without weighting;Vertices;N_{events} / 1 Vertex", 50, 0, 50);
    hVerticesAfterWeight =  fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "verticesAfterWeight", "Number of vertices with weighting; Vertices;N_{events} / 1 Vertex", 50, 0, 50);
    hVerticesTriggeredBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "verticesTriggeredBeforeWeight", "Number of vertices triggered without weighting;Vertices;N_{events} / 1 Vertex", 50, 0, 50);
    hVerticesTriggeredAfterWeight =  fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, *fs, "verticesTriggeredAfterWeight", "Number of vertices triggered with weighting; Vertices;N_{events} / 1 Vertex", 50, 0, 50);

    // Factorisation map
    int myTauPtBins = static_cast<int>(fTauPtBinLowEdges.size()) + 1;
    int myTauEtaBins = static_cast<int>(fTauEtaBinLowEdges.size()) + 1;
    int myNVerticesBins = static_cast<int>(fNVerticesBinLowEdges.size()) + 1;
    // Transverse mass bins
    if (fTransverseMassRange.size() != 3)
      throw cms::Exception("Configuration") << "QCDMeasurementBasic: need to provide config param. factorisationTransverseMassRange = (nbins, min, max)!";
    double myDelta = (fTransverseMassRange[2]-fTransverseMassRange[1]) / fTransverseMassRange[0];
    for (double i = 0; i < fTransverseMassRange[0]; ++i) {
      fTransverseMassBinLowEdges.push_back(i * myDelta);
    }
    // Full mass bins
    if (fFullMassRange.size() != 3)
      throw cms::Exception("Configuration") << "QCDMeasurementBasic: need to provide config param. factorisationFullMassRange = (nbins, min, max)!";
    myDelta = (fFullMassRange[2]-fFullMassRange[1]) / fFullMassRange[0];
    for (double i = 0; i < fFullMassRange[0]; ++i) {
      fFullMassRange.push_back(i * myDelta);
    }
    // Factorisation histograms
    TFileDirectory myDir = fs->mkdir("factorisation");
    hLeg1AfterMET = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg1AfterMET", "Leg1AfterMET", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    hLeg1AfterBTagging = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg1AfterBTagging", "Leg1AfterBTagging", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    hLeg1AfterDeltaPhiTauMET = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg1AfterDeltaPhiTauMET", "Leg1AfterDeltaPhiTauMET", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    hLeg1AfterTopSelection = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg1AfterTopSelection", "Leg1AfterTopSelection", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);
    hLeg2AfterTauID = fHistoWrapper.makeTH<TH3F>(HistoWrapper::kVital, myDir, "Leg2AfterTauID", "Leg2AfterTauID", myTauPtBins, 0., myTauPtBins, myTauEtaBins, 0., myTauEtaBins, myNVerticesBins, 0., myNVerticesBins);

    // Mt and full mass shape histograms
    createShapeHistograms(fs, hMtShapesAfterJetSelection, "MtShapesAfterJetSelection", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hMtShapesAfterFullMETLeg, "MtShapesAfterFullMETLeg", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    //createShapeHistograms(fs, hMtShapesAfterMetLegNoBtagging, "MtShapesAfterMetLegNoBtagging", fTransverseMassRange[0], fTransverseMassRange[1], fTransverseMassRange[2]);
    createShapeHistograms(fs, hFullMassShapesAfterJetSelection, "FullMassShapesAfterJetSelection", fFullMassRange[0], fFullMassRange[1], fFullMassRange[2]);
    createShapeHistograms(fs, hFullMassShapesAfterFullMETLeg, "FullMassShapesAfterFullMETLeg", fFullMassRange[0], fFullMassRange[1], fFullMassRange[2]);
    //createShapeHistograms(fs, hFullMassShapesAfterMetLegNoBtagging, "FullMassShapesAfterMetLegNoBtagging", fFullMassRange[0], fFullMassRange[1], fFullMassRange[2]);

    // Control plots
    createShapeHistograms(fs, hCtrlNjets, "CtrlLeg1AfterNjets", 10, 0., 10.);
    createShapeHistograms(fs, hCtrlMET, "CtrlLeg1AfterMET", 100, 0.0, 500.0);
    createShapeHistograms(fs, hCtrlNbjets, "CtrlLeg1AfterNbjets", 10, 0., 10.0);
    createShapeHistograms(fs, hCtrlDeltaPhiTauMET, "CtrlLeg1AfterDeltaPhiTauMET", 36, 0., 180.);
    createShapeHistograms(fs, hCtrlMaxDeltaPhiJetMET, "CtrlLeg1AfterMaxDeltaPhiJetMET", 36, 0., 180.);
    createShapeHistograms(fs, hCtrlTopMass, "CtrlLeg1AfterMaxDeltaPhiJetMET", 80, 0., 400.);

    // Other control histograms

    // Selection flow histogram
    hSelectionFlow = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "QCD_SelectionFlow", "QCD_SelectionFlow;;N_{events}", 12, 0, 12);
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderTrigger,"Trigger");
    //hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderVertexSelection,"Vertex");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderTauCandidateSelection,"#tau cand.");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderElectronVeto,"Isol. e veto");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderMuonVeto,"Isol. #mu veto");
    hSelectionFlow->GetXaxis()->SetBinLabel(1+kQCDOrderJetSelection,"N_{jets}");

    fTree.enableNonIsoLeptons(true);
    fTree.init(*fs);

   }

  QCDMeasurementBasic::~QCDMeasurementBasic() {}

  bool QCDMeasurementBasic::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    return analyze(iEvent, iSetup);
  }

  bool QCDMeasurementBasic::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
//------ Read the prescale for the event and set the event weight as the prescale
    fEventWeight.updatePrescale(iEvent);
    fTree.setPrescaleWeight(fEventWeight.getWeight());


//------ Vertex weight
    double myWeightBeforeVertexReweighting = fEventWeight.getWeight();
    if(!iEvent.isRealData()) {
      const double myVertexWeight = fVertexWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(myVertexWeight);
      fTree.setPileupWeight(myVertexWeight);
    }
    int nVertices = fVertexWeightReader.getNumberOfVertices(iEvent, iSetup);
    int myNVerticesBinIndex = getNVerticesBinIndex(nVertices);
    hVerticesBeforeWeight->Fill(nVertices, myWeightBeforeVertexReweighting);
    hVerticesAfterWeight->Fill(nVertices);
    fTree.setNvertices(nVertices);
    hSelectionFlow->Fill(kQCDOrderVertexSelection);
    increment(fAllCounter);


//------ Apply trigger and HLT_MET cut or trigger parametrisation
    TriggerSelection::Data triggerData = fTriggerSelection.analyze(iEvent, iSetup);
    if (!triggerData.passedEvent()) return false;
    increment(fTriggerCounter);
    hSelectionFlow->Fill(kQCDOrderTrigger);
    if(triggerData.hasTriggerPath()) // protection if TriggerSelection is disabled
      fTree.setHltTaus(triggerData.getTriggerTaus());

    hVerticesTriggeredBeforeWeight->Fill(nVertices, myWeightBeforeVertexReweighting);
    hVerticesTriggeredAfterWeight->Fill(nVertices);


//------ GenParticle analysis (must be done here when we effectively trigger all MC)
    if (!iEvent.isRealData()) {
      GenParticleAnalysis::Data genData = fGenparticleAnalysis.analyze(iEvent, iSetup);
      fTree.setGenMET(genData.getGenMET());
    }


//------ Primary vertex selection
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    if (!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    //hSelectionFlow->Fill(kQCDOrderVertexSelection);


//------ Tau candidate selection
    // Store weight of event
    double myWeightBeforeTauID = fEventWeight.getWeight();
    // Do tau candidate selection
    TauSelection::Data tauCandidateData = fTauSelection.analyze(iEvent, iSetup);
    if (!tauCandidateData.passedEvent()) return false;
    // note: do not require here that only one tau has been found; instead take first item from mySelectedTau as the tau in the event
    increment(fTausExistCounter);
    // Apply trigger scale factor here, because it depends only on tau
    TriggerEfficiencyScaleFactor::Data triggerWeight = fTriggerEfficiencyScaleFactor.applyEventWeight(*(tauCandidateData.getSelectedTau()), iEvent.isRealData(), fEventWeight);
    fTree.setTriggerWeight(triggerWeight.getEventWeight(), triggerWeight.getEventWeightAbsoluteUncertainty());
    increment(fTriggerScaleFactorCounter);
    hSelectionFlow->Fill(kQCDOrderTauCandidateSelection);
    // Obtain tau pT bin index
    int myTauPtBinIndex = getTauPtBinIndex(tauCandidateData.getSelectedTau()->pt());
    int myTauEtaBinIndex = getTauPtBinIndex(tauCandidateData.getSelectedTau()->eta());

    // Obtain boolean for rest of tauID for control plots
    bool myPassedTauIDStatus = tauCandidateData.selectedTauPassesFullTauID();
    // Count how many tau candidates actually pass tau ID
    if (myPassedTauIDStatus) {
      int myFullTauIDPassedCount = 0;
      for (edm::PtrVector<pat::Tau>::iterators it = tauCandidateData.getSelectedTaus().begin(); it != tauCandidateData.getSelectedTaus().end(); ++it) {
        if ((*it)->selectedTauPassesFullTauID())
          ++myFullTauIDPassedCount;
      }
      // Require exactly 1 tau
      if (myFullTauIDPassedCount > 1)
        myPassedTauIDStatus = false;
    }

//------ Veto against second tau in event
    VetoTauSelection::Data vetoTauData = fVetoTauSelection.analyze(iEvent, iSetup, tauCandidateData.getSelectedTau());
    //    if (vetoTauData.passedEvent()) return false;
    if (!vetoTauData.passedEvent()) increment(fVetoTauCounter);


//------ Global electron veto
    GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return false;
    increment(fElectronVetoCounter);
    hSelectionFlow->Fill(kQCDOrderElectronVeto);
    /*NonIsolatedElectronVeto::Data nonIsolatedElectronVetoData = fNonIsolatedElectronVeto.analyze(iEvent, iSetup);
    if (!nonIsolatedElectronVetoData.passedEvent())  return false;
    increment(fNonIsolatedElectronVetoCounter);*/
    // Control plot


//------ Global muon veto
    GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return false;
    increment(fMuonVetoCounter);
    hSelectionFlow->Fill(kQCDOrderMuonVeto);
    /*NonIsolatedMuonVeto::Data nonIsolatedMuonVetoData = fNonIsolatedMuonVeto.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!nonIsolatedMuonVetoData.passedEvent()) return; 
    increment(fNonIsolatedMuonVetoCounter);*/
    // Control plot


//------ Jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, tauCandidateData.getSelectedTau(), nVertices);
    hCtrlNjets[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(jetData.getHadronicJetCount());
    if (!jetData.passedEvent()) return false;
    increment(fNJetsCounter);
    hSelectionFlow->Fill(kQCDOrderJetSelection);
    hAfterJetSelection->Fill(myTauPtBinIndex);
    // Control plot
    hAfterJetSelection->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);


//------ Standard selections is done, obtain data objects, fill tree, and loop over analysis variations
    if (fTree.isActive()) {
      // Obtain MET data
      METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, tauCandidateData.getSelectedTau(), jetData.getAllJets());
      // Obtain btagging data
      BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
      // Obtain alphaT
      EvtTopology::Data evtTopologyData = fEvtTopology.analyze(*(tauCandidateData.getSelectedTau()), jetData.getSelectedJets());
      // Top reconstruction in different versions
      TopSelection::Data topSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
      BjetSelection::Data bjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), tauCandidateData.getSelectedTau(), metData.getSelectedMET());
      TopChiSelection::Data topChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
      TopWithBSelection::Data topWithBSelectionData = fTopWithBSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), bjetSelectionData.getBjetTopSide());

      // Fill tree
      if(metData.getRawMET().isNonnull())
        fTree.setRawMET(metData.getRawMET());
      if(metData.getType1MET().isNonnull())
        fTree.setType1MET(metData.getType1MET());
      if(metData.getType2MET().isNonnull())
        fTree.setType2MET(metData.getType2MET());
      if(metData.getCaloMET().isNonnull())
        fTree.setCaloMET(metData.getCaloMET());
      if(metData.getTcMET().isNonnull())
        fTree.setTcMET(metData.getTcMET());
      fTree.setFillWeight(fEventWeight.getWeight());
      if (!iEvent.isRealData()) {
        fEventWeight.multiplyWeight(btagData.getScaleFactor()); // needed to calculate the scale factor and the uncertainties
      }
      fTree.setBTagging(btagData.passedEvent(), btagData.getScaleFactor(), btagData.getScaleFactorAbsoluteUncertainty());
      //fTree.setTop(TopSelectionData.getTopP4());
      //fTree.setAlphaT(evtTopologyData.alphaT().fAlphaT);
      //fTree.setDeltaPhi(fakeMETData.closestDeltaPhi());
      edm::PtrVector<pat::Tau> mySelectedTaus;
      mySelectedTaus.push_back(tauCandidateData.getSelectedTau());
      fTree.fill(iEvent, mySelectedTaus, jetData.getSelectedJets());
      return true;
    }

// ----- Tau ID leg (factorisation
    if (tauCandidateData.selectedTauPassesFullTauID()) {
      hLeg2AfterTauID->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);
      
      // On purpose: No return statement for false (factorisation)
    }

// ----- MET, btag, deltaPhi(tau,MET), top reco leg
    // MET cut
    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, tauCandidateData.getSelectedTau(), jetData.getAllJets());
    hCtrlMET[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(metData.getSelectedMET()->et());
    if(!metData.passedEvent()) return false;
    increment(fMETCounter);
    hSelectionFlow->Fill(kQCDOrderMET);
    hLeg1AfterMET->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);

    // b tagging cut
    BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJets());
    if(!btagData.passedEvent()) return false;
    increment(fBTaggingCounter);
    // Apply scale factor as weight to event
    if (!iEvent.isRealData()) {
      btagData.fillScaleFactorHistograms(); // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }
    increment(fBTaggingScaleFactorCounter);
    hSelectionFlow->Fill(kQCDOrderBTag);
    hLeg1AfterBTagging->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);
    hCtrlNbjets[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(btagData.getBJetCount());

    // Delta phi(tau,MET) cut
    double deltaPhi = DeltaPhi::reconstruct(*(tauCandidateData.getSelectedTau()), *(metData.getSelectedMET())) * 57.3; // converted to degrees
    hCtrlDeltaPhiTauMET[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(deltaPhi);
    if (deltaPhi > fDeltaPhiCutValue) return false;
    increment(fDeltaPhiTauMETCounter);
    hSelectionFlow->Fill(kQCDOrderDeltaPhiTauMET);
    hLeg1AfterDeltaPhiTauMET->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);

    // Max Delta phi(jet/tau,MET) cut
    double myMaxDeltaPhiJetMET = deltaPhi;
    for(edm::PtrVector<pat::Jet>::const_iterator iJet = jetData.getSelectedJets().begin(); iJet != jetData.getSelectedJets().end(); ++iJet) {
      double jetDeltaPhi = DeltaPhi::reconstruct(**iJet, *(metData.getSelectedMET())) * 57.3;
      if (jetDeltaPhi > myMaxDeltaPhiJetMET)
        myMaxDeltaPhiJetMET = jetDeltaPhi;
    }
    hCtrlMaxDeltaPhiJetMET[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(myMaxDeltaPhiJetMET);
    hLeg1AfterMaxDeltaPhiJetMET->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);

    TopSelection::Data TopSelectionData = fTopSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    TopChiSelection::Data TopChiSelectionData = fTopChiSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets());
    bool myTopRecoWithWSelectionStatus = false;
    BjetSelection::Data BjetSelectionData = fBjetSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), btagData.getSelectedJets(), tauData.getSelectedTau(), metData.getSelectedMET());
    double myTopWithBSelectionTopMass = 0.0;
    if (BjetSelectionData.passedEvent() ) {
      TopWithBSelection::Data TopWithBSelectionData = fTopWithBSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());
      TopWithWSelection::Data TopWithWSelectionData = fTopWithWSelection.analyze(iEvent, iSetup, jetData.getSelectedJets(), BjetSelectionData.getBjetTopSide());
      if (TopWithWSelectionData.passedEvent() ) {
        myTopRecoWithWSelectionStatus = true;
        myTopWithBSelectionTopMass = TopWithWSelectionData.getTopMass();
      }
    }
    // Select events depending on top resonctruction
    bool myPassedTopRecoStatus = false;
    double myTopMass = 0.0;
    if (fTopRecoName == "None") {
      myPassedTopRecoStatus = true;
    } else if (fTopRecoName == "std") {
      myPassedTopRecoStatus = TopSelectionData.passedEvent();
      myTopMass = TopSelectionData.getTopMass();
    } else if (fTopRecoName == "chi") {
      myPassedTopRecoStatus = TopChiSelectionData.passedEvent();
      myTopMass = TopChiSelectionData.getTopMass();
    } else if (fTopRecoName == "Wselection") {
      myPassedTopRecoStatus = myTopRecoWithWSelectionStatus;
      myTopMass = myTopWithBSelectionTopMass;
    }
    hCtrlTopMass[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(myTopMass);
    if (!myPassedTopRecoStatus)
      return false;
    increment(fTopSelectionCounter);
    hLeg1AfterTopSelection->Fill(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex);

    // MET leg selection passed

    // Obtain transverseMass
    double transverseMass = TransverseMass::reconstruct(*(tauCandidateData.getSelectedTau()), *(metData.getSelectedMET()));
    hMtShapesAfterFullMETLeg[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(transverseMass);
    // Obtain full mass
    FullHiggsMassCalculator::Data fullMassData =  fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauCandidateData, btagData, metData);
    hFullMassShapesAfterFullMETLeg[getShapeBinIndex(myTauPtBinIndex, myTauEtaBinIndex, myNVerticesBinIndex)]->Fill(fullMassData.getHiggsMass());


    // Uncertainties after standard selections // FIXME: is this needed?
    fSFUncertaintyAfterStandardSelections.setScaleFactorUncertainties(fEventWeight.getWeight(),
                                                                      triggerWeight.getEventWeight(), triggerWeight.getEventWeightAbsoluteUncertainty(),
                                                                      1.0, 0.0); // these values are valid because btagging is not yet applied at this stage

//------ End of QCD measurement
    return true;
  }

  // Returns index to tau pT bin; 0 is underflow and size() is highest bin
  int QCDMeasurementBasic::getTauPtBinIndex(double pt) {
    size_t mySize = fTauPtBinLowEdges.size();
    for (size_t i = 0; i < mySize; ++i) {
      if (pt < fTauPtBinLowEdges[i])
        return static_cast<int>(i);
    }
    return static_cast<int>(mySize);
  }

  int QCDMeasurementBasic::getTauEtaBinIndex(double eta) {
    size_t mySize = fTauEtaBinLowEdges.size();
    for (size_t i = 0; i < mySize; ++i) {
      if (eta < fTauEtaBinLowEdges[i])
        return static_cast<int>(i);
    }
    return static_cast<int>(mySize);
  }

  int QCDMeasurementBasic::getNVerticesBinIndex(int nvtx) {
    size_t mySize = fNVerticesBinLowEdges.size();
    for (size_t i = 0; i < mySize; ++i) {
      if (nvtx < fNVerticesBinLowEdges[i])
        return static_cast<int>(i);
    }
    return static_cast<int>(mySize);
  }

  int QCDMeasurementBasic::getMtBinIndex(double mt) {
    size_t mySize = fTransverseMassRange.size();
    for (size_t i = 0; i < mySize; ++i) {
      if (mt < fTransverseMassRange[i])
        return static_cast<int>(i);
    }
    return static_cast<int>(mySize);
  }

  int QCDMeasurementBasic::getFullMassBinIndex(double mass) {
    size_t mySize = fFullMassRange.size();
    for (size_t i = 0; i < mySize; ++i) {
      if (mass < fFullMassRange[i])
        return static_cast<int>(i);
    }
    return static_cast<int>(mySize);
  }

  void QCDMeasurementBasic::createShapeHistograms(edm::Service<TFileService>& fs, std::vector<WrappedTH1*>& container, std::string title, int nbins, double min, double max) {
    std::stringstream myLabel;
    int myTauPtBins = static_cast<int>(fTauPtBinLowEdges.size()) + 1;
    int myTauEtaBins = static_cast<int>(fTauEtaBinLowEdges.size()) + 1;
    int myNVerticesBins = static_cast<int>(fNVerticesBinLowEdges.size()) + 1;
    std::string myTitle = "shape_"+title
    TFileDirectory myDir = fs->mkdir(myTitle.str().c_str());
    for (int i = 0; i < myTauPtBins; ++i) {
      for (int j = 0; j < myTauEtaBins; ++j) {
        for (int k = 0; k < myNVerticesBins; ++k) {
          myLabel.str("");
          myLabel << title << "_" << i << "_" << j << "_" << k;
          container.push_back(fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, myLabel.str().c_str(), myLabel.str().c_str(), nbins, min, max));
        }
      }
    }
  }

  int QCDMeasurementBasic::getShapeBinIndex(double tauPt, double tauEta, int nvtx) {
    int myTauEtaBins = static_cast<int>(fTauEtaBinLowEdges.size()) + 1;
    int myNVerticesBins = static_cast<int>(fNVerticesBinLowEdges.size()) + 1;
    int myTauPtBin = getTauPtBinIndex(tauPt);
    int myTauEtaBin = getTauEtaBinIndex(tauEta);
    int myVtxBin = getNVerticesBinIndex((nvtx);
    return myVtxBin + myTauEtaBin*myNVerticesBins + myTauPtBin*myNVerticesBins*myTauEtaBins;
  }
}

