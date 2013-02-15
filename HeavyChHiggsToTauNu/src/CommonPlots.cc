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
    hFakeTauStatus = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "tau_fakeStatus", "tau_fakeStatus;N_{events}", 11, 0, 11);
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
    hTransverseMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "transverseMass", "transverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events}", 80, 0., 400.);

  }

  CommonPlotsFilledAtEveryStep::~CommonPlotsFilledAtEveryStep() {}

  void CommonPlotsFilledAtEveryStep::fill() {
     // Safety check
     //if (!fDataObjectsCached)
     //  throw cms::Exception("Assert") << "CommonPlotsFilledAtEveryStep: data objects have not been cached! (did you forget to call CommonPlotsFilledAtEveryStep::cacheDataObjects from CommonPlots::initialize?)";
    hNVertices->Fill(fNVertices);
    if (!fVertexData) return;
    if (!fVertexData->passedEvent()) return; // Plots do not make sense if no PV has been found

    if (!fTauData) return;
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
    if (fJetData->getAllJets().size() == 0) return; // Safety for MET selection data to exist
    // transverse mass
    double myMT = TransverseMass::reconstruct(*(fTauData->getSelectedTau()), *(fMETData->getSelectedMET()) );
    hTransverseMass->Fill(myMT);
  }

  void CommonPlotsFilledAtEveryStep::cacheDataObjects(int nVertices,
                                                      const VertexSelection::Data* vertexData,
                                                      const TauSelection::Data* tauData,
                                                      const FakeTauIdentifier::Data* fakeTauData,
                                                      const ElectronSelection::Data* electronData,
                                                      const MuonSelection::Data* muonData,
                                                      const JetSelection::Data* jetData,
                                                      const METSelection::Data* metData,
                                                      const BTagging::Data* bJetData,
                                                      const TopChiSelection::Data* topData) {
    fNVertices = nVertices;
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
    fNormalisationAnalysis(eventCounter, histoWrapper) {
      createHistograms();
  }

  CommonPlots::CommonPlots(EventCounter& eventCounter, HistoWrapper& histoWrapper) :
    bDataObjectsCached(false),
    fEventCounter(eventCounter),
    fHistoWrapper(histoWrapper),
    fCommonBaseDirectory(fs->mkdir("CommonPlots")),
    fEveryStepDirectory(fCommonBaseDirectory.mkdir("AtEveryStep")),
    fNormalisationAnalysis(eventCounter, histoWrapper) {
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
                               int nVertices,
                               VertexSelection& vertexSelection,
                               TauSelection& tauSelection,
                               FakeTauIdentifier& fakeTauIdentifier,
                               ElectronSelection& eVeto,
                               MuonSelection& muonVeto,
                               JetSelection& jetSelection,
                               METSelection& metSelection,
                               BTagging& bJetSelection,
                               TopChiSelection& topChiSelection,
                               EvtTopology& evtTopology) {
    // Obtain data objects only, if they have not yet been cached
    //if (bDataObjectsCached) return;
    //bDataObjectsCached = true;
    fNVertices = nVertices;
    // Obtain data objects
    fVertexData = vertexSelection.silentAnalyze(iEvent, iSetup);
    if (!fVertexData.passedEvent()) {
      // Plots do not make sense if no PV has been found
      for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it != hEveryStepHistograms.end(); ++it) {
        (*it)->cacheDataObjects(fNVertices, 0, 0, 0, 0, 0, 0, 0, 0, 0);
      }
      return;
    }
    fTauData = tauSelection.silentAnalyze(iEvent, iSetup, fVertexData.getSelectedVertex()->z());
    // Need to require one tau in the event
    if (!fTauData.passedEvent()) {
      // Plots do not make sense if no PV has been found
      for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it != hEveryStepHistograms.end(); ++it) {
        (*it)->cacheDataObjects(fNVertices, &fVertexData, 0, 0, 0, 0, 0, 0, 0, 0);
      }
      return;
    }
    fFakeTauData = fakeTauIdentifier.silentMatchTauToMC(iEvent, *(fTauData.getSelectedTau()));
    fElectronData = eVeto.silentAnalyze(iEvent, iSetup);
    fMuonData = muonVeto.silentAnalyze(iEvent, iSetup, fVertexData.getSelectedVertex());
    fJetData = jetSelection.silentAnalyze(iEvent, iSetup, fTauData.getSelectedTau(), fNVertices);
    fMETData = metSelection.silentAnalyze(iEvent, iSetup, fTauData.getSelectedTau(), fJetData.getAllJets());
    fBJetData = bJetSelection.silentAnalyze(iEvent, iSetup, fJetData.getSelectedJets());
    fTopData = topChiSelection.silentAnalyze(iEvent, iSetup, fJetData.getSelectedJets(), fBJetData.getSelectedJets());

    // Pass pointer to cached data objects to CommonPlotsFilledAtEveryStep
    if (!hEveryStepHistograms.size())
      throw cms::Exception("Assert") << "CommonPlots::initialize() was called before creating CommonPlots::createCommonPlotsFilledAtEveryStep()!" << endl<<  "  make first all CommonPlots::createCommonPlotsFilledAtEveryStep() and then call CommonPlots::initialize()";
    for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it != hEveryStepHistograms.end(); ++it) {
      (*it)->cacheDataObjects(fNVertices, &fVertexData, &fTauData, &fFakeTauData, &fElectronData, &fMuonData, &fJetData, &fMETData, &fBJetData, &fTopData);
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

  void CommonPlots::fillControlPlots(const VertexSelection::Data& data) {
    //fVertexData = data;
    
  }

  void CommonPlots::fillControlPlots(const TauSelection::Data& tauData, const FakeTauIdentifier::Data& fakeTauData) {
    //fTauData = data;
    hTauPhiOscillationX->Fill(fNVertices, tauData.getSelectedTau()->px());
    hTauPhiOscillationY->Fill(fNVertices, tauData.getSelectedTau()->py());
    
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
