// -*- c++ -*-
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CommonPlots.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"

namespace HPlus {
  CommonPlotsFilledAtEveryStep::CommonPlotsFilledAtEveryStep(HistoWrapper& histoWrapper, TFileDirectory& dir, std::string label, bool enterSelectionFlowPlot, std::string selectionFlowPlotLabel) :
    fDataObjectsCached(false),
    fEnterSelectionFlowPlot(enterSelectionFlowPlot),
    fSelectionFlowPlotLabel(selectionFlowPlotLabel) {
    // Create directory for histogram
    TFileDirectory myDir = dir.mkdir(label.c_str());
    // Create histograms
    hNVertices = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "nVertices", "Number of vertices;N_{vertices};N_{events}", 60, 0, 60);
    hFakeTauStatus = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "tau_fakeStatus", "tau_fakeStatus;N_{events}", 11, 0, 11);
    if (hFakeTauStatus->isActive()) {
      // items labeled 'main count' sum up to Nevents (useful if you want to know the fractions)
      hFakeTauStatus->GetXaxis()->SetBinLabel(1, "All events"); // control to give Nevents
      hFakeTauStatus->GetXaxis()->SetBinLabel(2, "1-prong #tau"); // main count
      hFakeTauStatus->GetXaxis()->SetBinLabel(3, "3-prong #tau"); // main count
      hFakeTauStatus->GetXaxis()->SetBinLabel(4, "e#rightarrow#tau"); // main count
      hFakeTauStatus->GetXaxis()->SetBinLabel(5, "#mu#rightarrow#tau"); // main count
      hFakeTauStatus->GetXaxis()->SetBinLabel(6, "jet#rightarrow#tau"); // main count
      hFakeTauStatus->GetXaxis()->SetBinLabel(7, "uds#rightarrow#tau"); // subcount
      hFakeTauStatus->GetXaxis()->SetBinLabel(8, "cb#rightarrow#tau"); // subcount
      hFakeTauStatus->GetXaxis()->SetBinLabel(9, "g#rightarrow#tau"); // subcount
      hFakeTauStatus->GetXaxis()->SetBinLabel(10, "#tau#rightarrowe#rightarrow#tau"); // subcount
      hFakeTauStatus->GetXaxis()->SetBinLabel(11, "#tau#rightarrow#mu#rightarrow#tau"); // subcount
    }
    hTauPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "tau_pT", "tau_pT;#tau p_{T}, GeV/c;N_{events}", 100, 0.0, 500.0);
    hTauEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "tau_eta", "tau_eta;#tau #eta;N_{events}", 50, -2.5, 2.5);
    hTauPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "tau_phi", "tau_phi;#tau #phi;N_{events}", 72, -3.1415926, 3.1415926);
    hRtau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "tau_Rtau", "tau_Rtau;R_{#tau};N_{events}", 60, 0.0, 1.2);
    hSelectedElectrons = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "electrons_N", "electrons_N;N_{electrons};N_{events}", 40, 0.0, 40.);
    hSelectedMuons = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "muons_N", "muons_N;N_{muons};N_{events}", 40, 0.0, 40.);
    hNjets = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jets_N", "jets_N;N_{jets};N_{events}", 20, 0.0, 20.);
    hNjetsAllIdentified = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jets_N_allIdentified", "jets_N_allIdentified;N_{jets};N_{events}", 20, 0.0, 20.);
    hMETRaw = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MET_Raw", "MET_Raw;Raw MET, GeV;N_{events}", 100, 0.0, 500.);
    hMET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MET_MET", "MET;MET, GeV;N_{events}", 100, 0.0, 500.);
    hMETphi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MET_phi", "MET_phi;MET #phi;N_{events}", 72, -3.1415926, 3.1415926);
    hNbjets = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "bjets_N", "bjets_N;N_{b jets};N_{events}", 20, 0.0, 20.);
    hDeltaPhiTauMET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaPhi_TauMET", "DeltaPhi_TauMET;#Delta#phi(#tau,MET);N_{events}", 36, 0.0, 180.);
    hDeltaR_TauMETJet1MET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "hDeltaR_TauMETJet1MET", "hDeltaR_TauMETJet1MET;#sqrt((180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1},MET)^{2}), ^{o};N_{events}", 52, 0.0, 260.);
    hDeltaR_TauMETJet2MET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "hDeltaR_TauMETJet2MET", "hDeltaR_TauMETJet1MET;#sqrt((180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{2},MET)^{2}), ^{o};N_{events}", 52, 0.0, 260.);
    hDeltaR_TauMETJet3MET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "hDeltaR_TauMETJet3MET", "hDeltaR_TauMETJet1MET;#sqrt((180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{3},MET)^{2}), ^{o};N_{events}", 52, 0.0, 260.);
    hDeltaR_TauMETJet4MET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "hDeltaR_TauMETJet4MET", "hDeltaR_TauMETJet1MET;#sqrt((180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{4},MET)^{2}), ^{o};N_{events}", 52, 0.0, 260.);
    hTransverseMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "transverseMass", "transverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events}", 80, 0., 400.);
  }

  CommonPlotsFilledAtEveryStep::~CommonPlotsFilledAtEveryStep() {}

  void CommonPlotsFilledAtEveryStep::fill() {
     // Safety check
     //if (!fDataObjectsCached)
     //  throw cms::Exception("Assert") << "CommonPlotsFilledAtEveryStep: data objects have not been cached! (did you forget to call CommonPlotsFilledAtEveryStep::cacheDataObjects from CommonPlots::initialize?)";
    size_t nVertices = fVertexData->getNumberOfAllVertices();
    hNVertices->Fill(nVertices);
    if (!fVertexData) return;
    if (!fVertexData->passedEvent()) return; // Plots do not make sense if no PV has been found

    if (fFakeTauData) {
      // Fill fake tau breakdown
      hFakeTauStatus->Fill(0); // control for Nevents
      if (fFakeTauData->isGenuineOneProngTau())
        hFakeTauStatus->Fill(1);
      else if (!fFakeTauData->isGenuineOneProngTau() && fFakeTauData->isGenuineTau())
        hFakeTauStatus->Fill(2);
      else if (fFakeTauData->isElectronToTau()) {
        hFakeTauStatus->Fill(3);
        if (fFakeTauData->isEmbeddingGenuineTau())
          hFakeTauStatus->Fill(9);
      } else if (fFakeTauData->isMuonToTau()) {
        hFakeTauStatus->Fill(4);
        if (fFakeTauData->isEmbeddingGenuineTau())
          hFakeTauStatus->Fill(10);
      } else if (fFakeTauData->isJetToTau()) {
        hFakeTauStatus->Fill(5);
        if (fJetData->getReferenceJetToTau().isNonnull()) {
          if (fJetData->getReferenceJetToTauPartonFlavour() >= 1 && fJetData->getReferenceJetToTauPartonFlavour() <= 3)
            hFakeTauStatus->Fill(6);
          else if (fJetData->getReferenceJetToTauPartonFlavour() >= 4 && fJetData->getReferenceJetToTauPartonFlavour() <= 5)
            hFakeTauStatus->Fill(7);
          if (fJetData->getReferenceJetToTauPartonFlavour() == 21)
            hFakeTauStatus->Fill(8);
        }
      }
    }
    if (fTauData) {
      hTauPt->Fill(fTauData->getSelectedTau()->pt());
      hTauEta->Fill(fTauData->getSelectedTau()->eta());
      hTauPhi->Fill(fTauData->getSelectedTau()->phi());
      hRtau->Fill(fTauData->getSelectedTauRtauValue());
    }
    if (fElectronData->eventContainsElectronFromCorBJet()) {
      hSelectedElectrons->Fill(fElectronData->getSelectedElectrons().size()+10);
      hSelectedElectrons->Fill(fElectronData->getNonIsolatedElectrons().size()+30);
    } else {
      hSelectedElectrons->Fill(fElectronData->getSelectedElectrons().size());
      hSelectedElectrons->Fill(fElectronData->getNonIsolatedElectrons().size()+20);
    }
    if (fMuonData->eventContainsMuonFromCorBJet()) {
      hSelectedMuons->Fill(fMuonData->getSelectedMuons().size()+10);
      hSelectedMuons->Fill(fMuonData->getSelectedMuonsBeforeIsolation().size()+30);
    } else {
      hSelectedMuons->Fill(fMuonData->getSelectedMuons().size());
      hSelectedMuons->Fill(fMuonData->getSelectedMuonsBeforeIsolation().size()+20);
    }
    hNjets->Fill(fJetData->getHadronicJetCount());
    hNjetsAllIdentified->Fill(fJetData->getAllIdentifiedJets().size());
    if (!fTauData) return; // Need a tau for MET::Data
    if (fJetData->getAllJets().size() == 0) return; // Safety for MET selection data to exist
    hMETRaw->Fill(fMETData->getRawMET()->et());
    hMET->Fill(fMETData->getSelectedMET()->et());
    hMETphi->Fill(fMETData->getSelectedMET()->phi());
    hNbjets->Fill(fBJetData->getBJetCount());
    double myDeltaPhiTauMET = DeltaPhi::reconstruct(*(fTauData->getSelectedTau()), *(fMETData->getSelectedMET())) * 57.3; // converted to degrees
    hDeltaPhiTauMET->Fill(myDeltaPhiTauMET);
    // DeltaR_TauMETJetnMET
    int njets = 0;
    for (size_t i = 0; i < fJetData->getAllIdentifiedJets().size(); ++i) {
      if (!(fJetData->getAllIdentifiedJets()[i]->pt() > 30. && (std::abs(fJetData->getAllIdentifiedJets()[i]->eta()) < 2.5))) continue;
      double myDeltaPhi = reco::deltaPhi(*(fMETData->getSelectedMET()), *(fJetData->getAllIdentifiedJets()[i])) * 57.3;
      double myDeltaR = std::sqrt(std::pow(180. - myDeltaPhiTauMET,2)+std::pow(myDeltaPhi,2));
      if (njets == 0) {
        hDeltaR_TauMETJet1MET->Fill(myDeltaR);
      } else if (njets == 1) {
        hDeltaR_TauMETJet2MET->Fill(myDeltaR);
      } else if (njets == 2) {
        hDeltaR_TauMETJet3MET->Fill(myDeltaR);
      } else if (njets == 3) {
        hDeltaR_TauMETJet4MET->Fill(myDeltaR);
      }
      ++njets;
    }

    // transverse mass
    double myMT = TransverseMass::reconstruct(*(fTauData->getSelectedTau()), *(fMETData->getSelectedMET()) );
    hTransverseMass->Fill(myMT);
  }

  void CommonPlotsFilledAtEveryStep::cacheDataObjects(const VertexSelection::Data* vertexData,
                                                      const TauSelection::Data* tauData,
                                                      const FakeTauIdentifier::Data* fakeTauData,
                                                      const ElectronSelection::Data* electronData,
                                                      const MuonSelection::Data* muonData,
                                                      const JetSelection::Data* jetData,
                                                      const METSelection::Data* metData,
                                                      const BTagging::Data* bJetData,
                                                      const TopChiSelection::Data* topData) {
    fVertexData = vertexData;
    fTauData = tauData;
    fFakeTauData = fakeTauData;
    fElectronData = electronData;
    fMuonData = muonData;
    fJetData = jetData;
    fMETData = metData;
    fBJetData = bJetData;
    fTopData = topData;
    //fEvtTopology = evtTopology;
  }

  // ====================================================================================================

  CommonPlots::CommonPlots(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper) :
    bDataObjectsCached(false),
    fEventCounter(eventCounter),
    fHistoWrapper(histoWrapper),
    fCommonBaseDirectory(fs->mkdir("CommonPlots")),
    fEveryStepDirectory(fCommonBaseDirectory.mkdir("AtEveryStep")),
    fNormalisationAnalysis(eventCounter, histoWrapper),
    fTauSelection(0), fFakeTauIdentifier(0) {
      createHistograms();
  }

  CommonPlots::CommonPlots(EventCounter& eventCounter, HistoWrapper& histoWrapper) :
    bDataObjectsCached(false),
    fEventCounter(eventCounter),
    fHistoWrapper(histoWrapper),
    fCommonBaseDirectory(fs->mkdir("CommonPlots")),
    fEveryStepDirectory(fCommonBaseDirectory.mkdir("AtEveryStep")),
    fNormalisationAnalysis(eventCounter, histoWrapper),
    fTauSelection(0), fFakeTauIdentifier(0) {
      createHistograms();
  }

  void CommonPlots::createHistograms() {
    // Create histograms
    TFileDirectory myTauDir = fCommonBaseDirectory.mkdir("Taus");
    hTauPhiOscillationX = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myTauDir, "TauPhiOscillationX", "TauPhiOscillationX;N_{vertices};#tau p_{x}, GeV/c", 60, 0., 60., 500, 0, 500);
    hTauPhiOscillationY = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myTauDir, "TauPhiOscillationY", "TauPhiOscillationY;N_{vertices};#tau p_{y}, GeV/c", 60, 0., 60., 500, 0, 500);


    // final
    TFileDirectory myFinalDir = fCommonBaseDirectory.mkdir("Final");
    hDphiTauMetVsDphiJet1MHT = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFinalDir, "hDphiTauMetVsDphiJet1MHT", "hDphiTauMetVsDphiJet1MHT;#Delta#phi(#tau,MET), ^{o};#Delta#phi(jet_{1},MHT), ^{o}", 36, 0, 180, 36, 0, 180);
    hDphiTauMetVsDphiJet2MHT = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFinalDir, "hDphiTauMetVsDphiJet2MHT", "hDphiTauMetVsDphiJet2MHT;#Delta#phi(#tau,MET), ^{o};#Delta#phi(jet_{2},MHT), ^{o}", 36, 0, 180, 36, 0, 180);
    hDphiTauMetVsDphiJet3MHT = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFinalDir, "hDphiTauMetVsDphiJet3MHT", "hDphiTauMetVsDphiJet3MHT;#Delta#phi(#tau,MET), ^{o};#Delta#phi(jet_{3},MHT), ^{o}", 36, 0, 180, 36, 0, 180);
    hDphiTauMetVsDphiJet4MHT = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFinalDir, "hDphiTauMetVsDphiJet4MHT", "hDphiTauMetVsDphiJet4MHT;#Delta#phi(#tau,MET), ^{o};#Delta#phi(jet_{4},MHT), ^{o}", 36, 0, 180, 36, 0, 180);
    hDphiTauMetVsDphiTauMHT = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFinalDir, "hDphiTauMetVsDphiTauMHT", "hDphiTauMetVsDphiTauMHT;#Delta#phi(#tau,MET), ^{o};#Delta#phi(#tau,MHT), ^{o}", 36, 0, 180, 36, 0, 180);
    // final for fake taus
    TFileDirectory myFinalFakeDir = fCommonBaseDirectory.mkdir("FakeTaus_Final");
    hDphiTauMetVsDphiJet1MHTFakeTaus = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFinalFakeDir, "hDphiTauMetVsDphiJet1MHT", "hDphiTauMetVsDphiJet1MHT;#Delta#phi(#tau,MET), ^{o};#Delta#phi(jet_{1},MHT), ^{o}", 36, 0, 180, 36, 0, 180);
    hDphiTauMetVsDphiJet2MHTFakeTaus = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFinalFakeDir, "hDphiTauMetVsDphiJet2MHT", "hDphiTauMetVsDphiJet2MHT;#Delta#phi(#tau,MET), ^{o};#Delta#phi(jet_{2},MHT), ^{o}", 36, 0, 180, 36, 0, 180);
    hDphiTauMetVsDphiJet3MHTFakeTaus = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFinalFakeDir, "hDphiTauMetVsDphiJet3MHT", "hDphiTauMetVsDphiJet3MHT;#Delta#phi(#tau,MET), ^{o};#Delta#phi(jet_{3},MHT), ^{o}", 36, 0, 180, 36, 0, 180);
    hDphiTauMetVsDphiJet4MHTFakeTaus = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFinalFakeDir, "hDphiTauMetVsDphiJet4MHT", "hDphiTauMetVsDphiJet4MHT;#Delta#phi(#tau,MET), ^{o};#Delta#phi(jet_{4},MHT), ^{o}", 36, 0, 180, 36, 0, 180);
    hDphiTauMetVsDphiTauMHTFakeTaus = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myFinalFakeDir, "hDphiTauMetVsDphiTauMHT", "hDphiTauMetVsDphiTauMHT;#Delta#phi(#tau,MET), ^{o};#Delta#phi(#tau,MHT), ^{o}", 36, 0, 180, 36, 0, 180);

  }

  CommonPlots::~CommonPlots() {
    for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it < hEveryStepHistograms.end(); ++it)
      delete (*it);
    hEveryStepHistograms.clear();
  }

  void CommonPlots::initialize(const edm::Event& iEvent,
                               const edm::EventSetup& iSetup,
                               VertexSelection::Data& vertexData,
                               TauSelection& tauSelection,
                               FakeTauIdentifier& fakeTauIdentifier,
                               ElectronSelection& eVeto,
                               MuonSelection& muonVeto,
                               JetSelection& jetSelection,
                               METSelection& metSelection,
                               BTagging& bJetSelection,
                               TopChiSelection& topChiSelection,
                               EvtTopology& evtTopology) {
    if (!vertexData.passedEvent()) return; // Require valid vertex
    fTauSelection = &tauSelection;
    TauSelection::Data tauData = tauSelection.silentAnalyze(iEvent, iSetup, vertexData.getSelectedVertex()->z());
    initialize(iEvent,iSetup,
               vertexData,
               tauData,
               fakeTauIdentifier,
               eVeto,
               muonVeto,
               jetSelection,
               metSelection,
               bJetSelection,
               topChiSelection,
               evtTopology);
  }

  void CommonPlots::initialize(const edm::Event& iEvent,
                               const edm::EventSetup& iSetup,
                               VertexSelection::Data& vertexData,
                               TauSelection::Data& tauData,
                               FakeTauIdentifier& fakeTauIdentifier,
                               ElectronSelection& eVeto,
                               MuonSelection& muonVeto,
                               JetSelection& jetSelection,
                               METSelection& metSelection,
                               BTagging& bJetSelection,
                               TopChiSelection& topChiSelection,
                               EvtTopology& evtTopology) {
    //fTauSelection = &tauSelection;
    fFakeTauIdentifier = &fakeTauIdentifier;
    // Obtain data objects only, if they have not yet been cached
    //if (bDataObjectsCached) return;
    //bDataObjectsCached = true;
    // Obtain data objects
    fVertexData = vertexData;
    if (!vertexData.passedEvent()) return; // Require valid vertex
    fTauData = tauData;
    if (fTauData.passedEvent())
      fFakeTauData = fakeTauIdentifier.silentMatchTauToMC(iEvent, *(fTauData.getSelectedTau()));
    fElectronData = eVeto.silentAnalyze(iEvent, iSetup);
    fMuonData = muonVeto.silentAnalyze(iEvent, iSetup, fVertexData.getSelectedVertex());
    if (fTauData.passedEvent())
      fJetData = jetSelection.silentAnalyze(iEvent, iSetup, fTauData.getSelectedTau(), fVertexData.getNumberOfAllVertices());
    else
      fJetData = jetSelection.silentAnalyze(iEvent, iSetup, fVertexData.getNumberOfAllVertices());
    // Need to require one tau in the event
    if (!fTauData.passedEvent()) {
      // Plots do not make sense if no tau has been found
      for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it != hEveryStepHistograms.end(); ++it) {
        (*it)->cacheDataObjects(&fVertexData, 0, 0, &fElectronData, &fMuonData, &fJetData, 0, 0, 0);
      }
      return;
    }
    fMETData = metSelection.silentAnalyze(iEvent, iSetup, fTauData.getSelectedTau(), fJetData.getAllJets());
    fBJetData = bJetSelection.silentAnalyze(iEvent, iSetup, fJetData.getSelectedJets());
    fTopData = topChiSelection.silentAnalyze(iEvent, iSetup, fJetData.getSelectedJets(), fBJetData.getSelectedJets());

    // Pass pointer to cached data objects to CommonPlotsFilledAtEveryStep
    if (!hEveryStepHistograms.size())
      throw cms::Exception("Assert") << "CommonPlots::initialize() was called before creating CommonPlots::createCommonPlotsFilledAtEveryStep()!" << endl<<  "  make first all CommonPlots::createCommonPlotsFilledAtEveryStep() and then call CommonPlots::initialize()";
    for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it != hEveryStepHistograms.end(); ++it) {
      (*it)->cacheDataObjects(&fVertexData, &fTauData, &fFakeTauData, &fElectronData, &fMuonData, &fJetData, &fMETData, &fBJetData, &fTopData);
    }
  }

  CommonPlotsFilledAtEveryStep* CommonPlots::createCommonPlotsFilledAtEveryStep(std::string label, bool enterSelectionFlowPlot, std::string selectionFlowPlotLabel) {
    // Create and return object, but sneakily save the pointer for later use
    CommonPlotsFilledAtEveryStep* myObject = new CommonPlotsFilledAtEveryStep(fHistoWrapper, fEveryStepDirectory, label, enterSelectionFlowPlot, selectionFlowPlotLabel);
    hEveryStepHistograms.push_back(myObject);
    return myObject;
  }

  void CommonPlots::fillControlPlots(const TriggerSelection::Data& data) {
    
  }

  void CommonPlots::fillControlPlots(const edm::Event& iEvent, const VertexSelection::Data& data) {
    //fVertexData = data;
    if(fTauSelection && fFakeTauIdentifier) {
      fNormalisationAnalysis.analyseTauFakeRate(iEvent, fVertexData, *fTauSelection, fTauData, *fFakeTauIdentifier, fJetData);
    }
  }

  void CommonPlots::fillControlPlots(const TauSelection::Data& tauData, const FakeTauIdentifier::Data& fakeTauData) {
    //fTauData = data;
    hTauPhiOscillationX->Fill(fVertexData.getNumberOfAllVertices(), tauData.getSelectedTau()->px());
    hTauPhiOscillationY->Fill(fVertexData.getNumberOfAllVertices(), tauData.getSelectedTau()->py());
    
    // e->tau normalisation
    fNormalisationAnalysis.analyseEToTauFakes(fVertexData, tauData, fakeTauData, fElectronData, fMuonData, fJetData, fMETData);
  }

  void CommonPlots::fillControlPlots(const ElectronSelection::Data& data) {
    //fElectronData = data;
    
  }

  void CommonPlots::fillControlPlots(const MuonSelection::Data& data) {
    //fMuonData = data;
    
  }

  void CommonPlots::fillControlPlots(const JetSelection::Data& data) {
    //fJetData = data;
    
  }

  void CommonPlots::fillControlPlots(const METSelection::Data& data) {
    
  }

  void CommonPlots::fillControlPlots(const BTagging::Data& data) {
    
  }

  void CommonPlots::fillControlPlots(const TopChiSelection::Data& data) {
    
  }

   void CommonPlots::fillControlPlots(const EvtTopology::Data& data) {
    
  }

  void CommonPlots::fillFinalPlots() {
    double myDeltaPhiTauMET = DeltaPhi::reconstruct(*(fTauData.getSelectedTau()), *(fMETData.getSelectedMET())) * 57.3; // converted to degrees

    hDphiTauMetVsDphiJet1MHT->Fill(myDeltaPhiTauMET, fJetData.getDeltaPhiMHTJet1());
    hDphiTauMetVsDphiJet2MHT->Fill(myDeltaPhiTauMET, fJetData.getDeltaPhiMHTJet2());
    hDphiTauMetVsDphiJet3MHT->Fill(myDeltaPhiTauMET, fJetData.getDeltaPhiMHTJet3());
    hDphiTauMetVsDphiJet4MHT->Fill(myDeltaPhiTauMET, fJetData.getDeltaPhiMHTJet4());
    hDphiTauMetVsDphiTauMHT->Fill(myDeltaPhiTauMET, fJetData.getDeltaPhiMHTTau());
  }

  void CommonPlots::fillFinalPlotsForFakeTaus() {
    double myDeltaPhiTauMET = DeltaPhi::reconstruct(*(fTauData.getSelectedTau()), *(fMETData.getSelectedMET())) * 57.3; // converted to degrees

    hDphiTauMetVsDphiJet1MHTFakeTaus->Fill(myDeltaPhiTauMET, fJetData.getDeltaPhiMHTJet1());
    hDphiTauMetVsDphiJet2MHTFakeTaus->Fill(myDeltaPhiTauMET, fJetData.getDeltaPhiMHTJet2());
    hDphiTauMetVsDphiJet3MHTFakeTaus->Fill(myDeltaPhiTauMET, fJetData.getDeltaPhiMHTJet3());
    hDphiTauMetVsDphiJet4MHTFakeTaus->Fill(myDeltaPhiTauMET, fJetData.getDeltaPhiMHTJet4());
    hDphiTauMetVsDphiTauMHTFakeTaus->Fill(myDeltaPhiTauMET, fJetData.getDeltaPhiMHTTau());
  }
}
