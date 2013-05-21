#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EWKMatching.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"

#include "TLorentzVector.h"

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TNamed.h"

namespace HPlus {
  EWKMatching::EWKMatching(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight, HistoWrapper& histoWrapper):
    fEventWeight(eventWeight),
    fHistoWrapper(fHistoWrapper),
    fDeltaPhiCutValue(iConfig.getUntrackedParameter<double>("deltaPhiTauMET")),
    //    fmetEmulationCut(iConfig.getUntrackedParameter<double>("metEmulationCut")),
    fAllCounter(eventCounter.addCounter("Offline selection begins")),
    fPrimaryVertexCounter(eventCounter.addCounter("primary vertex")),
    fOneTauCounter(eventCounter.addCounter("one embedded tau")),
    fElectronVetoCounter(eventCounter.addCounter("electron veto")),
    fMuonVetoCounter(eventCounter.addCounter("muon veto")),
    fNJetsCounter(eventCounter.addCounter("njets")),
    fMETCounter(eventCounter.addCounter("MET")),
    fBTaggingCounter(eventCounter.addCounter("btagging")),
    fBTaggingScaleFactorCounter(eventCounter.addCounter("btagging scale factor")),
    fDeltaPhiTauMETCounter(eventCounter.addCounter("DeltaPhi(Tau,MET) upper limit")),
    fSelectedEventsCounter(eventCounter.addCounter("Selected events")),
    fSelectedEventsCounterWithGenuineBjets(eventCounter.addCounter("Selected events with genuine b-jet selected")),
//    fTriggerSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("trigger"), eventCounter, fHistoWrapper),
    fPrimaryVertexSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("primaryVertexSelection"), eventCounter, fHistoWrapper),
    fElectronSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("ElectronSelection"), fPrimaryVertexSelection.getSelectedSrc(), eventCounter, fHistoWrapper),
    fMuonSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MuonSelection"), eventCounter, fHistoWrapper),
    fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, fHistoWrapper),
    fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, fHistoWrapper, "MET", "FIXME_NOT_AVAILABLE!"),
    fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("bTagging"), eventCounter, fHistoWrapper),
//    fFullHiggsMassCalculator(eventCounter, fHistoWrapper),
    fPrescaleWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("prescaleWeightReader"), fHistoWrapper, "PrescaleWeight"),
    fPileupWeightReader(iConfig.getUntrackedParameter<edm::ParameterSet>("pileupWeightReader"), fHistoWrapper, "PileupWeight")
  {
    edm::Service<TFileService> fs;
    // Save the module configuration to the output ROOT file as a TNamed object
    fs->make<TNamed>("parameterSet", iConfig.dump().c_str());

    // Book histograms filled in the analysis body
    
    // Vertex histograms
    TFileDirectory myVertexDir = fs->mkdir("Vertices");
    hVerticesBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myVertexDir, "verticesBeforeWeight", "Number of vertices without weighting", 40, 0, 40);
    hVerticesAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myVertexDir, "verticesAfterWeight", "Number of vertices with weighting", 40, 0, 40);
    hVerticesTriggeredBeforeWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myVertexDir, "verticesTriggeredBeforeWeight", "Number of vertices without weighting", 40, 0, 40);
    hVerticesTriggeredAfterWeight = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myVertexDir, "verticesTriggeredAfterWeight", "Number of vertices with weighting", 40, 0, 40);

    hWjetsNormalisationAfterJets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "WjetsNormalisationAfterJets", "WjetsNormalisationAfterJets; not passed / passed b tag", 2, 0., 2.);
    hWjetsNormalisationAfterMET20 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "WjetsNormalisationAfterMET20", "WjetsNormalisationAfterJetsMET20; not passed / passed b tag", 2, 0., 2.);
    hWjetsNormalisationAfterMET30 = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "WjetsNormalisationAfterMET30", "WjetsNormalisationAfterJetsMET30; not passed / passed b tag", 2, 0., 2.);
    hWjetsNormalisationAfterMET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "WjetsNormalisationAfterMET", "WjetsNormalisationAfterJetsMET; not passed / passed b tag", 2, 0., 2.);

    hDeltaPhi = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "deltaPhi", "deltaPhi;#Delta#phi(tau,MET);N_{events} / 10 degrees", 180, 0., 180.);
    hTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "transverseMass", "transverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 10 GeV/c^{2}", 200, 0., 400.);
//    hFullMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, *fs, "fullMass", "fullMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 5 GeV/c^{2}", 100, 0., 500.);
    // Control histograms
    TFileDirectory myCtrlDir = fs->mkdir("ControlPlots");
    hCtrlNjets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "Njets", "Njets;Number of selected jets;N_{events}", 10, 0., 10.);
    hCtrlNjetsAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "Njets_AfterStandardSelections", "Njets_AfterStandardSelections;Number of selected jets;N_{events}", 7, 3., 10.);
    hCtrlMET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "MET", "MET;MET, GeV;N_{events} / 10 GeV", 100, 0., 500.);
    hCtrlNbjets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "NBjets", "NBjets;Number of identified b-jets;N_{events}", 10, 0., 10.);
    hCtrlJetMatrixAfterJetSelection = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, myCtrlDir, "JetMatrixAfterJetSelection", "JetMatrixAfterJetSelection;Number of selected jets;Number of selected b jets", 7, 3., 10.,7, 0., 7.);
    hCtrlJetMatrixAfterMET = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, myCtrlDir, "JetMatrixAfterMET", "JetMatrixAfterMET;Number of selected jets;Number of selected b jets", 7, 3., 10.,7, 0., 7.);
    hCtrlJetMatrixAfterMET100 = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kVital, myCtrlDir, "JetMatrixAfterMET100", "JetMatrixAfterMET100;Number of selected jets;Number of selected b jets", 7, 3., 10.,7, 0., 7.);
  }

  EWKMatching::~EWKMatching() { }

  void EWKMatching::produces(edm::EDFilter *producer) const {
  }

  bool EWKMatching::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    fEventWeight.beginEvent();
    fEventWeight.multiplyWeight(fPrescaleWeightReader.getWeight(iEvent, iSetup));

//------ Pileup weight
    double myWeightBeforePileupReweighting = fEventWeight.getWeight();
    if(!iEvent.isRealData()) {
      const double myPileupWeight = fPileupWeightReader.getWeight(iEvent, iSetup);
      fEventWeight.multiplyWeight(myPileupWeight);
    }

//------ Primary vertex
    VertexSelection::Data pvData = fPrimaryVertexSelection.analyze(iEvent, iSetup);
    size_t nVertices = pvData.getNumberOfAllVertices();
    hVerticesBeforeWeight->Fill(nVertices, myWeightBeforePileupReweighting);
    hVerticesAfterWeight->Fill(nVertices);
    increment(fAllCounter);

    hVerticesTriggeredBeforeWeight->Fill(nVertices, myWeightBeforePileupReweighting);
    hVerticesTriggeredAfterWeight->Fill(nVertices);

    if(!pvData.passedEvent()) return false;
    increment(fPrimaryVertexCounter);
    //hSelectionFlow->Fill(kSignalOrderVertexSelection);

//------ TauID
    // Store weight of event
    // TauID
    edm::Handle<edm::View<pat::Tau> > htaus;
    iEvent.getByLabel("patTausPFlowTauEmbeddingMuonMatched", htaus);
    if (htaus->ptrVector().size() == 0) return false;
    edm::Ptr<pat::Tau> myTau = htaus->ptrVector()[0];

//     edm::Handle<edm::View<pat::Muon> > htaus;
//     iEvent.getByLabel("tauEmbeddingMuons", htaus);
//     std::cout << "embedded muons size = " << htaus->ptrVector().size() << std::endl;
//     if (htaus->ptrVector().size() == 0) return false;
//     edm::Ptr<pat::Muon> myTau = htaus->ptrVector()[0];
//     float myTrackIso =  myTau->trackIso(); // isolation cones are dR=0.3 
//     float myEcalIso  =  myTau->ecalIso();  // isolation cones are dR=0.3 
//     float myHcalIso  =  myTau->hcalIso();  // isolation cones are dR=0.3 
//     float myMuonPt   =  myTau->pt();
//     if (myMuonPt<10) return false;
//     float relIsol = ( myTrackIso + myEcalIso + myHcalIso )/(myMuonPt);
//     // std::cout << "relIsol = " << (*iMuon).isolationR03().sumPt << "/" << myMuonPt << " = " << relIsol << std::endl;
//     if( relIsol > 0.15 ) return false;

    
    increment(fOneTauCounter);

//------ Global electron veto
    ElectronSelection::Data electronVetoData = fElectronSelection.analyze(iEvent, iSetup);
    if (!electronVetoData.passedEvent()) return false;
    increment(fElectronVetoCounter);

//------ Global muon veto
    MuonSelection::Data muonVetoData = fMuonSelection.analyze(iEvent, iSetup, pvData.getSelectedVertex());
    if (!muonVetoData.passedEvent()) return false;
    increment(fMuonVetoCounter);

//------ Hadronic jet selection
    JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, myTau, nVertices);
    hCtrlNjets->Fill(jetData.getHadronicJetCount());
    if(!jetData.passedEvent()) return false;
    increment(fNJetsCounter);
    hCtrlNjetsAfterStandardSelections->Fill(jetData.getHadronicJetCount());

    METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, myTau, jetData.getAllJets());
    hCtrlMET->Fill(metData.getSelectedMET()->et());
    // Obtain delta phi and transverse mass here, but do not yet cut on them
    BTagging::Data btagData = fBTagging.silentAnalyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    int nBjets = btagData.getBJetCount();
    double myBWeight = btagData.getScaleFactor();
    double deltaPhi = DeltaPhi::reconstruct(*myTau, *(metData.getSelectedMET())) * 57.3; // converted to degrees
    double transverseMass = TransverseMass::reconstruct(*myTau, *(metData.getSelectedMET()));
    if (transverseMass > 40 && transverseMass < 100) {
      hCtrlJetMatrixAfterJetSelection->Fill(jetData.getHadronicJetCount(), nBjets);
      if (nBjets > 0)
        hWjetsNormalisationAfterJets->Fill(1,myBWeight);
      else
        hWjetsNormalisationAfterJets->Fill(0);
      if (metData.getSelectedMET()->et() > 20) {
        if (nBjets > 0)
          hWjetsNormalisationAfterMET20->Fill(1,myBWeight);
        else
          hWjetsNormalisationAfterMET20->Fill(0);
        if (metData.getSelectedMET()->et() > 30) {
          if (nBjets > 0)
            hWjetsNormalisationAfterMET30->Fill(1,myBWeight);
          else
            hWjetsNormalisationAfterMET30->Fill(0);
        }
      }
    }
    // MET selection
    
    // Now cut on MET
    if(!metData.passedEvent()) return false;
    increment(fMETCounter);
    // Plot jet matrix
    if (transverseMass > 40 && transverseMass < 100) {
      hCtrlJetMatrixAfterMET->Fill(jetData.getHadronicJetCount(), nBjets);
      if (metData.getSelectedMET()->et() > 100.0)
        hCtrlJetMatrixAfterMET100->Fill(jetData.getHadronicJetCount(), nBjets);
      if (nBjets > 0)
        hWjetsNormalisationAfterMET->Fill(1,myBWeight);
      else
        hWjetsNormalisationAfterMET->Fill(0);
    }
//------ b tagging cut
    btagData = fBTagging.analyze(iEvent, iSetup, jetData.getSelectedJetsPt20());
    hCtrlNbjets->Fill(btagData.getBJetCount());
    if(!btagData.passedEvent()) return false;
    increment(fBTaggingCounter);
    // Apply scale factor as weight to event
    if (!iEvent.isRealData()) {
      fBTagging.fillScaleFactorHistograms(btagData); // Important!!! Needs to be called before scale factor is applied as weight to the event; Uncertainty is determined from these histograms
      fEventWeight.multiplyWeight(btagData.getScaleFactor());
    }
    increment(fBTaggingScaleFactorCounter);

//------ Delta phi(tau,MET) cut
    hDeltaPhi->Fill(deltaPhi);
    if (deltaPhi > fDeltaPhiCutValue) return false;
    increment(fDeltaPhiTauMETCounter);

//------ Transverse mass and control plots
    increment(fSelectedEventsCounter);
    if (btagData.hasGenuineBJets()) increment(fSelectedEventsCounterWithGenuineBjets);
    hTransverseMass->Fill(transverseMass);
    //FullHiggsMassCalculator::Data FullHiggsMassData = fFullHiggsMassCalculator.analyze(iEvent, iSetup, tauData, btagData, metData);
    //double HiggsMass = FullHiggsMassData.getHiggsMass();
    //hFullMass->Fill(HiggsMass);

    return true;
  }
}
