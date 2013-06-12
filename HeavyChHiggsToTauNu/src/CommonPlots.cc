// -*- c++ -*-
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CommonPlots.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "FWCore/Framework/interface/Event.h"

namespace HPlus {
  HistogramSettings::HistogramSettings(const edm::ParameterSet& iConfig)
  : fBins(iConfig.getUntrackedParameter<uint32_t>("nBins")),
    fAxisMin(iConfig.getUntrackedParameter<double>("axisMin")),
    fAxisMax(iConfig.getUntrackedParameter<double>("axisMax")) { }
  HistogramSettings::~HistogramSettings() { }

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
    hFullMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "fullMass", "fullMass;m, GeV/c^{2};N_{events}", 100, 0., 500.);
  }

  CommonPlotsFilledAtEveryStep::~CommonPlotsFilledAtEveryStep() {}

  void CommonPlotsFilledAtEveryStep::fill() {
     // Safety check
     //if (!fDataObjectsCached)
     //  throw cms::Exception("Assert") << "CommonPlotsFilledAtEveryStep: data objects have not been cached! (did you forget to call CommonPlotsFilledAtEveryStep::cacheDataObjects from CommonPlots::initialize?)";
    if (!fVertexData) return;
    if (!fVertexData->passedEvent()) return; // Plots do not make sense if no PV has been found
    if (fMETData->getSelectedMET().isNull()) return; // If MET is not valid, do not plot events

    size_t nVertices = fVertexData->getNumberOfAllVertices();
    hNVertices->Fill(nVertices);

    if (fFakeTauData && fTauData) {
      if (fTauData->getSelectedTau().isNonnull()) {
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
    }
    if (fTauData) {
      if (fTauData->getSelectedTau().isNonnull()) {
        hTauPt->Fill(fTauData->getSelectedTau()->pt());
        hTauEta->Fill(fTauData->getSelectedTau()->eta());
        hTauPhi->Fill(fTauData->getSelectedTau()->phi());
        hRtau->Fill(fTauData->getSelectedTauRtauValue());
      }
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
    if (fJetData->getAllJets().size() == 0) return; // Safety for MET selection data to exist
    hMETRaw->Fill(fMETData->getRawMET()->et());
    hMET->Fill(fMETData->getSelectedMET()->et());
    hMETphi->Fill(fMETData->getSelectedMET()->phi());
    hNbjets->Fill(fBJetData->getBJetCount());
    if (!fTauData) return; // Require tau beyond this point to make sense
    if (fTauData->getSelectedTau().isNull()) return; // Require tau beyond this point to make sense
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
    // full mass
    if (!fTauData->getSelectedTau().isNull() && fBJetData->passedEvent()) { // Make sure FullHiggsMassData is available
      if (fFullHiggsMassData->passedEvent()) {
        hFullMass->Fill(fFullHiggsMassData->getHiggsMass());
      }
    }
  }

  void CommonPlotsFilledAtEveryStep::cacheDataObjects(const VertexSelection::Data* vertexData,
                                                      const TauSelection::Data* tauData,
                                                      const FakeTauIdentifier::Data* fakeTauData,
                                                      const ElectronSelection::Data* electronData,
                                                      const MuonSelection::Data* muonData,
                                                      const JetSelection::Data* jetData,
                                                      const METSelection::Data* metData,
                                                      const BTagging::Data* bJetData,
                                                      const QCDTailKiller::Data* qcdTailKillerData,
                                                      const TopChiSelection::Data* topData,
                                                      const FullHiggsMassCalculator::Data* fullHiggsMassData) {
    fVertexData = vertexData;
    fTauData = tauData;
    fFakeTauData = fakeTauData;
    fElectronData = electronData;
    fMuonData = muonData;
    fJetData = jetData;
    fMETData = metData;
    fBJetData = bJetData;
    fQCDTailKillerData = qcdTailKillerData;
    fTopData = topData;
    fFullHiggsMassData = fullHiggsMassData;
    //fEvtTopology = evtTopology;
  }

  // ====================================================================================================

  CommonPlots::CommonPlots(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, AnalysisType analysisType, bool isEmbeddedData) :
    bOptionEnableNormalisationAnalysis(iConfig.getUntrackedParameter<bool>("enableNormalisationAnalysis")),
    bOptionEnableMETOscillationAnalysis(iConfig.getUntrackedParameter<bool>("enableMETOscillationAnalysis")),
    fAnalysisType(analysisType),
    fEventCounter(eventCounter),
    fHistoWrapper(histoWrapper),
    fSplittedHistogramHandler(iConfig.getUntrackedParameter<edm::ParameterSet>("histogramSplitting"), histoWrapper),
    fCommonBaseDirectory(fs->mkdir("CommonPlots")),
    fEveryStepDirectory(fCommonBaseDirectory.mkdir("AtEveryStep")),
    fNormalisationAnalysis(0),
    fTauSelection(0), fFakeTauIdentifier(0),
    fPtBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("ptBins")),
    fEtaBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("etaBins")),
    fPhiBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("phiBins")),
    fRtauBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("rtauBins")),
    fNjetsBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("njetsBins")),
    fMetBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("metBins")),
    fTailKiller1DSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("tailKiller1DBins")),
    fMtBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("mtBins")),
    fInvmassBinSettings(iConfig.getUntrackedParameter<edm::ParameterSet>("invmassBins")),
    fMETPhiOscillationCorrectionAfterTaus(0),
    fMETPhiOscillationCorrectionAfterLeptonVeto(0),
    fMETPhiOscillationCorrectionAfterNjets(0),
    fMETPhiOscillationCorrectionAfterBjets(0),
    fMETPhiOscillationCorrectionAfterAllSelections(0),
    fMETPhiOscillationCorrectionEWKControlRegion(0) {
    // Update analysis type for embedding
    if (isEmbeddedData)
      fAnalysisType = kEmbedding;
    // Create histograms
    createHistograms();
    // Create objects for normalisation analysis
    if (bOptionEnableNormalisationAnalysis) {
      fNormalisationAnalysis = new NormalisationAnalysis(eventCounter, histoWrapper);
    }
    // Create objects for MET phi oscillation analysis
    if (bOptionEnableMETOscillationAnalysis) {
      fMETPhiOscillationCorrectionAfterTaus = new METPhiOscillationCorrection(eventCounter, fHistoWrapper, "AfterTaus");
      fMETPhiOscillationCorrectionAfterLeptonVeto = new METPhiOscillationCorrection(eventCounter, fHistoWrapper, "AfterLeptonVeto");
      fMETPhiOscillationCorrectionAfterNjets = new METPhiOscillationCorrection(eventCounter, fHistoWrapper, "AfterNjets");
      fMETPhiOscillationCorrectionAfterBjets = new METPhiOscillationCorrection(eventCounter, fHistoWrapper, "AfterBjets");
      fMETPhiOscillationCorrectionAfterAllSelections = new METPhiOscillationCorrection(eventCounter, fHistoWrapper, "AfterAllSelections");
      fMETPhiOscillationCorrectionEWKControlRegion = new METPhiOscillationCorrection(eventCounter, fHistoWrapper, "AfterAllSelections_EKWControlRegion");
    }
  }

  void CommonPlots::createHistograms() {
    // Create directories for data driven control plots
    TFileDirectory myCtrlDir = fs->mkdir("ForDataDrivenCtrlPlots");
    TFileDirectory myCtrlEWKFakeTausDir = fs->mkdir("ForDataDrivenCtrlPlotsFakeTaus");

    // Create histograms

    // vertex

    // tau selection

    // tau trigger SF
    TFileDirectory myTauDir = fCommonBaseDirectory.mkdir("TausWithSF");
    hTauPhiOscillationX = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myTauDir, "TauPhiOscillationX", "TauPhiOscillationX;N_{vertices};#tau p_{x}, GeV/c", 60, 0., 60., 1200, -300, 300);
    hTauPhiOscillationY = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myTauDir, "TauPhiOscillationY", "TauPhiOscillationY;N_{vertices};#tau p_{y}, GeV/c", 60, 0., 60., 1200, -300, 300);

    // veto tau selection

    // electron veto

    // muon veto

    // jet selection
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlNjets,            "Njets", "Number of selected jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
    if (fAnalysisType == kSignalAnalysis)
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausNjets, "Njets", "Number of selected jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());

    // MET trigger SF
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlNjetsAfterJetSelectionAndMETSF,            "NjetsAfterJetSelectionAndMETSF", "Number of selected jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
    if (fAnalysisType == kSignalAnalysis)
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausNjetsAfterJetSelectionAndMETSF, "NjetsAfterJetSelectionAndMETSF", "Number of selected jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());

    // improved delta phi collinear cuts (currently the point of the std. selections)
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerCollinearJet1,            "ImprovedDeltaPhiCutsJet1Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{1},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerCollinearJet2,            "ImprovedDeltaPhiCutsJet2Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{2},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerCollinearJet3,            "ImprovedDeltaPhiCutsJet3Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{3},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerCollinearJet4,            "ImprovedDeltaPhiCutsJet4Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{4},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    if (fAnalysisType == kSignalAnalysis) {
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerCollinearJet1, "ImprovedDeltaPhiCutsJet1Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{1},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerCollinearJet2, "ImprovedDeltaPhiCutsJet2Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{2},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerCollinearJet3, "ImprovedDeltaPhiCutsJet3Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{3},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerCollinearJet4, "ImprovedDeltaPhiCutsJet4Collinear", "#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{4},MET))^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    }

    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlSelectedTauPtAfterStandardSelections, "SelectedTau_pT_AfterStandardSelections", "#tau p_{T}, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlSelectedTauEtaAfterStandardSelections, "SelectedTau_eta_AfterStandardSelections", "#tau #eta;N_{events} / 0.1", fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlSelectedTauPhiAfterStandardSelections, "SelectedTau_phi_AfterStandardSelections", "#tau #phi;N_{events} / 0.087", fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
    hSelectedTauEtaVsPhiAfterStandardSelections = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myCtrlDir, "SelectedTau_etavsphi_AfterStandardSelections", "SelectedTau_etavsphi_AfterStandardSelections;#tau #eta;#tau #phi", fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(), fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlSelectedTauLeadingTrkPtAfterStandardSelections, "SelectedTau_LeadingTrackPt_AfterStandardSelections", "#tau ldg.ch.particle p_{T}, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlSelectedTauRtauAfterStandardSelections, "SelectedTau_Rtau_AfterStandardSelections", "R_{#tau};N_{events} / 0.1", fRtauBinSettings.bins(), fRtauBinSettings.min(), fRtauBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlSelectedTauPAfterStandardSelections, "SelectedTau_p_AfterStandardSelections", "#tau p, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlSelectedTauLeadingTrkPAfterStandardSelections, "SelectedTau_LeadingTrackP_AfterStandardSelections", "#tau ldg.ch.particle p, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlDir, hCtrlNjetsAfterStandardSelections, "Njets_AfterStandardSelections", "Number of selected jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
    if (fAnalysisType == kSignalAnalysis) {
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausSelectedTauPtAfterStandardSelections, "SelectedTau_pT_AfterStandardSelections", "#tau p_{T}, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausSelectedTauEtaAfterStandardSelections, "SelectedTau_eta_AfterStandardSelections", "#tau #eta;N_{events} / 0.1", fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausSelectedTauPhiAfterStandardSelections, "SelectedTau_phi_AfterStandardSelections", "#tau #phi;N_{events} / 0.087", fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
      hEWKFakeTausSelectedTauEtaVsPhiAfterStandardSelections = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, "SelectedTau_etavsphi_AfterStandardSelections", "#tau #eta;#tau #phi", fEtaBinSettings.bins(), fEtaBinSettings.min(), fEtaBinSettings.max(), fPhiBinSettings.bins(), fPhiBinSettings.min(), fPhiBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausSelectedTauLeadingTrkPtAfterStandardSelections, "SelectedTau_LeadingTrackPt_AfterStandardSelections", "#tau ldg.ch.particle p_{T}, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausSelectedTauRtauAfterStandardSelections, "SelectedTau_Rtau_AfterStandardSelections", "R_{#tau};N_{events} / 0.1", fRtauBinSettings.bins(), fRtauBinSettings.min(), fRtauBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausSelectedTauPAfterStandardSelections, "SelectedTau_p_AfterStandardSelections", "#tau p, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausSelectedTauLeadingTrkPAfterStandardSelections, "SelectedTau_LeadingTrackP_AfterStandardSelections", "#tau ldg.ch.particle p, GeV/c;N_{events} / 5 GeV/c", fPtBinSettings.bins(), fPtBinSettings.min(), fPtBinSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausNjetsAfterStandardSelections, "Njets_AfterStandardSelections", "Number of selected jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
    }

    // MET selection
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlMET,            "MET", "MET, GeV;N_{events}", fMetBinSettings.bins(), fMetBinSettings.min(), fMetBinSettings.max());
    if (fAnalysisType == kSignalAnalysis)
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausMET, "MET", "MET, GeV;N_{events}", fMetBinSettings.bins(), fMetBinSettings.min(), fMetBinSettings.max());

    // b tagging
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlNbjets,            "NBjets", "Number of identified b jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());
    if (fAnalysisType == kSignalAnalysis)
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausNbjets, "NBjets", "Number of identified b jets;N_{events}", fNjetsBinSettings.bins(), fNjetsBinSettings.min(), fNjetsBinSettings.max());

    // improved delta phi back to back cuts
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerBackToBackJet1,           "ImprovedDeltaPhiCutsJet1BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerBackToBackJet2,           "ImprovedDeltaPhiCutsJet2BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{2},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerBackToBackJet3,           "ImprovedDeltaPhiCutsJet3BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{3},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlDir,            hCtrlQCDTailKillerBackToBackJet4,           "ImprovedDeltaPhiCutsJet4BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{4},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    if (fAnalysisType == kSignalAnalysis) {
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerBackToBackJet1,"ImprovedDeltaPhiCutsJet1BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerBackToBackJet2,"ImprovedDeltaPhiCutsJet2BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{2},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerBackToBackJet3,"ImprovedDeltaPhiCutsJet3BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{3},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, myCtrlEWKFakeTausDir, hCtrlEWKFakeTausQCDTailKillerBackToBackJet4,"ImprovedDeltaPhiCutsJet4BackToBack", "#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{4},MET)^{2}}, ^{o};N_{events}", fTailKiller1DSettings.bins(), fTailKiller1DSettings.min(), fTailKiller1DSettings.max());
    }

    // top selection

    // evt topology

    // all selections
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, *fs, hShapeTransverseMass,            "shapeTransverseMass", "m_{T}(tau,MET), GeV/c^{2};N_{events}", fMtBinSettings.bins(), fMtBinSettings.min(), fMtBinSettings.max());
    if (fAnalysisType == kSignalAnalysis)
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, *fs, hShapeEWKFakeTausTransverseMass, "shapeEWKFakeTausTransverseMass", "m_{T}(tau,MET), GeV/c^{2};N_{events}", fMtBinSettings.bins(), fMtBinSettings.min(), fMtBinSettings.max());

    // all selections with full mass
    fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, *fs, hShapeFullMass,            "shapeInvariantMass", "m_{H+}, GeV/c^{2};N_{events}", fInvmassBinSettings.bins(), fInvmassBinSettings.min(), fInvmassBinSettings.max());
    if (fAnalysisType == kSignalAnalysis)
      fSplittedHistogramHandler.createShapeHistogram(HistoWrapper::kVital, *fs, hShapeEWKFakeTausFullMass, "shapeEWKFakeTausInvariantMass", "m_{H+}, GeV/c^{2};N_{events}", fInvmassBinSettings.bins(), fInvmassBinSettings.min(), fInvmassBinSettings.max());
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
                               QCDTailKiller& qcdTailKiller,
                               TopChiSelection& topChiSelection,
                               EvtTopology& evtTopology,
                               FullHiggsMassCalculator& fullHiggsMassCalculator) {
    if (!vertexData.passedEvent()) return; // Require valid vertex
    fTauSelection = &tauSelection;
    fTauData = tauSelection.silentAnalyze(iEvent, iSetup, vertexData.getSelectedVertex()->z());
    initialize(iEvent,iSetup,
               vertexData,
               fTauData,
               fakeTauIdentifier,
               eVeto,
               muonVeto,
               jetSelection,
               metSelection,
               bJetSelection,
               qcdTailKiller,
               topChiSelection,
               evtTopology,
               fullHiggsMassCalculator);
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
                               QCDTailKiller& qcdTailKiller,
                               TopChiSelection& topChiSelection,
                               EvtTopology& evtTopology,
                               FullHiggsMassCalculator& fullHiggsMassCalculator) {
    fSplittedHistogramHandler.initialize();

    fFakeTauIdentifier = &fakeTauIdentifier;
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
    fBJetData = bJetSelection.silentAnalyze(iEvent, iSetup, fJetData.getSelectedJets());
    fTopData = topChiSelection.silentAnalyze(iEvent, iSetup, fJetData.getSelectedJets(), fBJetData.getSelectedJets());
    // Need to require one tau in the event
    if (fTauData.getSelectedTau().isNull()) {
      fMETData = metSelection.silentAnalyzeNoIsolatedTaus(iEvent, iSetup);
      // Plots do not make sense if no tau has been found
      edm::Ptr<pat::Tau> myZeroTauPointer;
      for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it != hEveryStepHistograms.end(); ++it) {
        (*it)->cacheDataObjects(&fVertexData, 0, 0, &fElectronData, &fMuonData, &fJetData, &fMETData, &fBJetData, 0, &fTopData, 0);
      }
      return;
    }
    // A tau exists beyond this point, now obtain MET with residual type I MET
    fMETData = metSelection.silentAnalyze(iEvent, iSetup, vertexData.getNumberOfAllVertices(), fTauData.getSelectedTau(), fJetData.getAllJets());
    // Obtain improved delta phi cut data object
    fQCDTailKillerData = qcdTailKiller.silentAnalyze(iEvent, iSetup, fTauData.getSelectedTau(), fJetData.getSelectedJetsIncludingTau(), fMETData.getSelectedMET());
    // Do full higgs mass only if tau and b jet was found
    if (fBJetData.passedEvent()) {
      fFullHiggsMassData = fullHiggsMassCalculator.silentAnalyze(iEvent, iSetup, fTauData.getSelectedTau(), fBJetData, fMETData);
    }

    // Pass pointer to cached data objects to CommonPlotsFilledAtEveryStep
    if (!hEveryStepHistograms.size())
      throw cms::Exception("Assert") << "CommonPlots::initialize() was called before creating CommonPlots::createCommonPlotsFilledAtEveryStep()!" << endl<<  "  make first all CommonPlots::createCommonPlotsFilledAtEveryStep() and then call CommonPlots::initialize()";
    for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it != hEveryStepHistograms.end(); ++it) {
      (*it)->cacheDataObjects(&fVertexData, &fTauData, &fFakeTauData, &fElectronData, &fMuonData, &fJetData, &fMETData, &fBJetData, &fQCDTailKillerData, &fTopData, &fFullHiggsMassData);
    }
  }

  CommonPlotsFilledAtEveryStep* CommonPlots::createCommonPlotsFilledAtEveryStep(std::string label, bool enterSelectionFlowPlot, std::string selectionFlowPlotLabel) {
    // Create and return object, but sneakily save the pointer for later use
    CommonPlotsFilledAtEveryStep* myObject = new CommonPlotsFilledAtEveryStep(fHistoWrapper, fEveryStepDirectory, label, enterSelectionFlowPlot, selectionFlowPlotLabel);
    hEveryStepHistograms.push_back(myObject);
    return myObject;
  }

//------ Control plot filling
  void CommonPlots::fillControlPlotsAfterVertexSelection(const edm::Event& iEvent, const VertexSelection::Data& data) {
    //----- MET phi oscillation
    //fMETData = metSelection.silentAnalyzeNoIsolatedTaus(iEvent, iSetup, fJetData.getAllJets());
    if(bOptionEnableNormalisationAnalysis && fTauSelection && fFakeTauIdentifier) {
      fNormalisationAnalysis->analyseTauFakeRate(iEvent, fVertexData, *fTauSelection, fTauData, *fFakeTauIdentifier, fJetData);
    }
  }

  void CommonPlots::fillControlPlotsAfterTauSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, const FakeTauIdentifier::Data& fakeTauData, METSelection& metSelection) {
    fTauData = tauData;
    fFakeTauData = fakeTauData;
    // Set splitted bin info
    fSplittedHistogramHandler.setFactorisationBinForEvent(fTauData.getSelectedTau()->pt(), fTauData.getSelectedTau()->eta(), fVertexData.getNumberOfAllVertices());
    // Obtain new MET object corresponding to the selected tau
    fMETData = metSelection.silentAnalyze(iEvent, iSetup, fVertexData.getNumberOfAllVertices(), fTauData.getSelectedTau(), fJetData.getAllJets());
    if (bOptionEnableNormalisationAnalysis) {
      // e->tau normalisation // FIXME tau trg scale factor needs to be applied!
      fNormalisationAnalysis->analyseEToTauFakes(fVertexData, tauData, fakeTauData, fElectronData, fMuonData, fJetData, fMETData);
    }
  }

  void CommonPlots::fillControlPlotsAfterTauTriggerScaleFactor(const edm::Event& iEvent) {
    if (bOptionEnableMETOscillationAnalysis) fMETPhiOscillationCorrectionAfterTaus->analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
    hTauPhiOscillationX->Fill(fVertexData.getNumberOfAllVertices(), fTauData.getSelectedTau()->px());
    hTauPhiOscillationY->Fill(fVertexData.getNumberOfAllVertices(), fTauData.getSelectedTau()->py());
  }

  void CommonPlots::fillControlPlotsAtTauVetoSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const VetoTauSelection::Data& tauVetoData) {

  }

  void CommonPlots::fillControlPlotsAtElectronSelection(const edm::Event& iEvent, const ElectronSelection::Data& data) {
    fElectronData = data;
  }

  void CommonPlots::fillControlPlotsAtMuonSelection(const edm::Event& iEvent, const MuonSelection::Data& data) {
    fMuonData = data;
    if (bOptionEnableMETOscillationAnalysis) fMETPhiOscillationCorrectionAfterLeptonVeto->analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
  }

  void CommonPlots::fillControlPlotsAtJetSelection(const edm::Event& iEvent, const JetSelection::Data& data) {
    fJetData = data;
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlNjets, data.getHadronicJetCount());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausNjets, data.getHadronicJetCount());
    if (bOptionEnableMETOscillationAnalysis) fMETPhiOscillationCorrectionAfterNjets->analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
  }

  void CommonPlots::fillControlPlotsAfterMETTriggerScaleFactor(const edm::Event& iEvent) {
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlNjetsAfterJetSelectionAndMETSF, fJetData.getHadronicJetCount());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausNjetsAfterJetSelectionAndMETSF, fJetData.getHadronicJetCount());
  }

  void CommonPlots::fillControlPlotsAtCollinearDeltaPhiCuts(const edm::Event& iEvent, const QCDTailKiller::Data& data) {
    fQCDTailKillerData = data;
    bool myPassStatus = true;
    for (int i = 0; i < data.getNConsideredJets(); ++i) {
      if (i == 0 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerCollinearJet1, data.getRadiusFromCollinearCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerCollinearJet1, data.getRadiusFromCollinearCorner(i)); // Make control pl
      } else if (i == 1 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerCollinearJet2, data.getRadiusFromCollinearCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerCollinearJet2, data.getRadiusFromCollinearCorner(i)); // Make control pl
      } else if (i == 2 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerCollinearJet3, data.getRadiusFromCollinearCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerCollinearJet3, data.getRadiusFromCollinearCorner(i)); // Make control pl
      } else if (i == 3 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerCollinearJet4, data.getRadiusFromCollinearCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerCollinearJet4, data.getRadiusFromCollinearCorner(i)); // Make control pl
      }
      if (!data.passCollinearCutForJet(i))
        myPassStatus = false;
    }
    // Fill control plots for selected taus after standard selections
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlSelectedTauRtauAfterStandardSelections, fTauData.getSelectedTauRtauValue());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlSelectedTauLeadingTrkPtAfterStandardSelections, fTauData.getSelectedTau()->leadPFChargedHadrCand()->pt());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlSelectedTauPtAfterStandardSelections, fTauData.getSelectedTau()->pt());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlSelectedTauEtaAfterStandardSelections, fTauData.getSelectedTau()->eta());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlSelectedTauPhiAfterStandardSelections, fTauData.getSelectedTau()->phi());
    hSelectedTauEtaVsPhiAfterStandardSelections->Fill(fTauData.getSelectedTau()->eta(), fTauData.getSelectedTau()->phi());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlSelectedTauPAfterStandardSelections, fTauData.getSelectedTau()->p());
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlSelectedTauLeadingTrkPAfterStandardSelections, fTauData.getSelectedTau()->leadPFChargedHadrCand()->p());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) {
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausSelectedTauRtauAfterStandardSelections, fTauData.getSelectedTauRtauValue());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausSelectedTauLeadingTrkPtAfterStandardSelections, fTauData.getSelectedTau()->leadPFChargedHadrCand()->pt());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausSelectedTauPtAfterStandardSelections, fTauData.getSelectedTau()->pt());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausSelectedTauEtaAfterStandardSelections, fTauData.getSelectedTau()->eta());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausSelectedTauPhiAfterStandardSelections, fTauData.getSelectedTau()->phi());
      hEWKFakeTausSelectedTauEtaVsPhiAfterStandardSelections->Fill(fTauData.getSelectedTau()->eta(), fTauData.getSelectedTau()->phi());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausSelectedTauPAfterStandardSelections, fTauData.getSelectedTau()->p());
      fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausSelectedTauLeadingTrkPAfterStandardSelections, fTauData.getSelectedTau()->leadPFChargedHadrCand()->p());
    }
    // Fill other control plots
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlNjetsAfterStandardSelections, fJetData.getHadronicJetCount());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausNjetsAfterStandardSelections, fJetData.getHadronicJetCount());
  }

  void CommonPlots::fillControlPlotsAtMETSelection(const edm::Event& iEvent, const METSelection::Data& data) {
    fMETData = data;
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlMET, data.getSelectedMET()->et());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausMET, data.getSelectedMET()->et());
  }

  void CommonPlots::fillControlPlotsAtBtagging(const edm::Event& iEvent, const BTagging::Data& data) {
    fBJetData = data;
    fSplittedHistogramHandler.fillShapeHistogram(hCtrlNbjets, data.getBJetCount());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausNbjets, data.getBJetCount());
    if (bOptionEnableMETOscillationAnalysis) fMETPhiOscillationCorrectionAfterBjets->analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
  }

  void CommonPlots::fillControlPlotsAtBackToBackDeltaPhiCuts(const edm::Event& iEvent, const QCDTailKiller::Data& data) {
    fQCDTailKillerData = data;
    bool myPassStatus = true;
    for (int i = 0; i < data.getNConsideredJets(); ++i) {
      if (i == 0 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerBackToBackJet1, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerBackToBackJet1, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
      } else if (i == 1 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerBackToBackJet2, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerBackToBackJet2, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
      } else if (i == 2 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerBackToBackJet3, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerBackToBackJet3, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
      } else if (i == 3 && myPassStatus) {
        fSplittedHistogramHandler.fillShapeHistogram(hCtrlQCDTailKillerBackToBackJet4, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis)
          fSplittedHistogramHandler.fillShapeHistogram(hCtrlEWKFakeTausQCDTailKillerBackToBackJet4, data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
      }
    }
  }

  void CommonPlots::fillControlPlotsAtTopSelection(const edm::Event& iEvent, const TopChiSelection::Data& data) {
    
  }

  void CommonPlots::fillControlPlotsAtEvtTopology(const edm::Event& iEvent, const EvtTopology::Data& data) {
    
  }

  void CommonPlots::fillControlPlotsAfterAllSelections(const edm::Event& iEvent, double transverseMass) {
    if (bOptionEnableMETOscillationAnalysis) {
      fMETPhiOscillationCorrectionAfterAllSelections->analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
      if (transverseMass < 80.0) {
        fMETPhiOscillationCorrectionEWKControlRegion->analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
      }
    }
    //double myDeltaPhiTauMET = DeltaPhi::reconstruct(*(fTauData.getSelectedTau()), *(fMETData.getSelectedMET())) * 57.3; // converted to degrees
    fSplittedHistogramHandler.fillShapeHistogram(hShapeTransverseMass, transverseMass);
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) fSplittedHistogramHandler.fillShapeHistogram(hShapeEWKFakeTausTransverseMass, transverseMass);
  }

  void CommonPlots::fillControlPlotsAfterAllSelectionsWithFullMass(const edm::Event& iEvent, FullHiggsMassCalculator::Data& data) {
    fFullHiggsMassData = data;
    fSplittedHistogramHandler.fillShapeHistogram(hShapeFullMass, data.getHiggsMass());
    if (fFakeTauData.isFakeTau() && fAnalysisType == kSignalAnalysis) fSplittedHistogramHandler.fillShapeHistogram(hShapeEWKFakeTausFullMass, data.getHiggsMass());
  }
}
