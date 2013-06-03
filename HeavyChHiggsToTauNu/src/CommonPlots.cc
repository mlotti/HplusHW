// -*- c++ -*-
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CommonPlots.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "FWCore/Framework/interface/Event.h"

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
    if (fTauData && !fSelectedTau.isNull()) {
      hTauPt->Fill(fSelectedTau->pt());
      hTauEta->Fill(fSelectedTau->eta());
      hTauPhi->Fill(fSelectedTau->phi());
      //hRtau->Fill(fSelectedTauRtauValue()); // Note: will be bogus for QCD measurements
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
    if (fSelectedTau.isNull()) return; // Require tau beyond this point to make sense
    double myDeltaPhiTauMET = DeltaPhi::reconstruct(*(fSelectedTau), *(fMETData->getSelectedMET())) * 57.3; // converted to degrees
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
    double myMT = TransverseMass::reconstruct(*(fSelectedTau), *(fMETData->getSelectedMET()) );
    hTransverseMass->Fill(myMT);
    // full mass
    if (!fSelectedTau.isNull() && fBJetData->passedEvent()) { // Make sure FullHiggsMassData is available
      if (fFullHiggsMassData->passedEvent()) {
        hFullMass->Fill(fFullHiggsMassData->getHiggsMass());
      }
    }
  }

  void CommonPlotsFilledAtEveryStep::cacheDataObjects(const VertexSelection::Data* vertexData,
                                                      const TauSelection::Data* tauData,
                                                      edm::Ptr<pat::Tau>& selectedTau,
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
    fSelectedTau = selectedTau;
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

  CommonPlots::CommonPlots(const edm::ParameterSet& iConfig, EventCounter& eventCounter, HistoWrapper& histoWrapper, bool plotSeparatelyFakeTaus) :
    fPlotSeparatelyFakeTaus(plotSeparatelyFakeTaus),
    fEventCounter(eventCounter),
    fHistoWrapper(histoWrapper),
    fCommonBaseDirectory(fs->mkdir("CommonPlots")),
    fEveryStepDirectory(fCommonBaseDirectory.mkdir("AtEveryStep")),
    fNormalisationAnalysis(eventCounter, histoWrapper),
    fTauSelection(0), fFakeTauIdentifier(0),
    fMETPhiOscillationCorrectionAfterTaus(eventCounter, fHistoWrapper, "AfterTaus"),
    fMETPhiOscillationCorrectionAfterLeptonVeto(eventCounter, fHistoWrapper, "AfterLeptonVeto"),
    fMETPhiOscillationCorrectionAfterNjets(eventCounter, fHistoWrapper, "AfterNjets"),
    fMETPhiOscillationCorrectionAfterBjets(eventCounter, fHistoWrapper, "AfterBjets"),
    fMETPhiOscillationCorrectionAfterAllSelections(eventCounter, fHistoWrapper, "AfterAllSelections") {
      createHistograms();
  }

  CommonPlots::CommonPlots(EventCounter& eventCounter, HistoWrapper& histoWrapper, bool plotSeparatelyFakeTaus) :
    fPlotSeparatelyFakeTaus(plotSeparatelyFakeTaus),
    fEventCounter(eventCounter),
    fHistoWrapper(histoWrapper),
    fCommonBaseDirectory(fs->mkdir("CommonPlots")),
    fEveryStepDirectory(fCommonBaseDirectory.mkdir("AtEveryStep")),
    fNormalisationAnalysis(eventCounter, histoWrapper),
    fTauSelection(0), fFakeTauIdentifier(0),
    fMETPhiOscillationCorrectionAfterTaus(eventCounter, fHistoWrapper, "AfterTaus"),
    fMETPhiOscillationCorrectionAfterLeptonVeto(eventCounter, fHistoWrapper, "AfterLeptonVeto"),
    fMETPhiOscillationCorrectionAfterNjets(eventCounter, fHistoWrapper, "AfterNjets"),
    fMETPhiOscillationCorrectionAfterBjets(eventCounter, fHistoWrapper, "AfterBjets"),
    fMETPhiOscillationCorrectionAfterAllSelections(eventCounter, fHistoWrapper, "AfterAllSelections") {
      createHistograms();
  }

  void CommonPlots::createHistograms() {
    // Create directories for data driven control plots
    TFileDirectory myCtrlDir = fs->mkdir("ForDataDrivenCtrlPlots");
    TFileDirectory myCtrlEWKFakeTausDir = fs->mkdir("ForDataDrivenCtrlPlotsFakeTaus");
    HistoWrapper::HistoLevel myEWKFakeTauCtrlPlotLevel = HistoWrapper::kInformative;
    if (!fPlotSeparatelyFakeTaus)
      myEWKFakeTauCtrlPlotLevel = HistoWrapper::kNumberOfLevels; // Prohibit creating histograms for EWK fakes to save disc space

    // Create histograms

    // vertex

    // tau selection

    // tau trigger SF
    TFileDirectory myTauDir = fCommonBaseDirectory.mkdir("TausWithSF");
    hTauPhiOscillationX = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myTauDir, "TauPhiOscillationX", "TauPhiOscillationX;N_{vertices};#tau p_{x}, GeV/c", 60, 0., 60., 500, 0, 500);
    hTauPhiOscillationY = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myTauDir, "TauPhiOscillationY", "TauPhiOscillationY;N_{vertices};#tau p_{y}, GeV/c", 60, 0., 60., 500, 0, 500);

    // veto tau selection

    // electron veto
    hCtrlIdentifiedElectronPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlDir, "IdentifiedElectronPt", "IdentifiedElectronPt;Identified electron p_{T}, GeV/c;N_{events} / 5 GeV", 100, 0., 500.);
    hCtrlEWKFakeTausIdentifiedElectronPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, "IdentifiedElectronPt", "IdentifiedElectronPt;Identified electron p_{T}, GeV/c;N_{events} / 5 GeV", 100, 0., 500.);

    // muon veto
    hCtrlIdentifiedMuonPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlDir, "IdentifiedMuonPt", "IdentifiedMuonPt;Identified muon p_{T}, GeV/c;N_{events} / 5 GeV", 100, 0., 500.);
    hCtrlEWKFakeTausIdentifiedMuonPt = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, "IdentifiedMuonPt", "IdentifiedMuonPt;Identified muon p_{T}, GeV/c;N_{events} / 5 GeV", 100, 0., 500.);

    // jet selection
    hCtrlNjets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "Njets", "Njets;Number of selected jets;N_{events}", 20, 0., 20.);
    hCtrlEWKFakeTausNjets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "Njets", "Njets;Number of selected jets;N_{events}", 20, 0., 20.);

    // MET trigger SF
    hCtrlNjetsAfterJetSelectionAndMETSF = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "NjetsAfterJetSelectionAndMETSF", "NjetsAfterJetSelectionAndMETSF;Number of selected jets;N_{events}", 20, 0., 20.);
    hCtrlEWKFakeTausNjetsAfterJetSelectionAndMETSF = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "NjetsAfterJetSelectionAndMETSF", "NjetsAfterJetSelectionAndMETSF;Number of selected jets;N_{events}", 20, 0., 20.);

    // improved delta phi collinear cuts (currently the point of the std. selections)
    for (int i = 0; i < 4; ++i) {
      std::stringstream sName;
      std::stringstream sTitle;
      sName << "ImprovedDeltaPhiCutsJet" << i << "Collinear";
      sTitle << "ImprovedDeltaPhiCutsJet" << i << "Collinear;#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{" << i << "},MET))^{2}}, ^{o};N_{events}";
      hCtrlQCDTailKillerCollinear.push_back(fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, sName.str().c_str(), sTitle.str().c_str(), 52, 0., 260.));
      sName.str("");
      sTitle.str("");
      sName << "ImprovedDeltaPhiCutsJet" << i << "CollinearFakeTaus";
      sTitle << "ImprovedDeltaPhiCutsJet" << i << "CollinearFakeTaus;#sqrt{#Delta#phi(#tau,MET)^{2}+(180^{o}-#Delta#phi(jet_{" << i << "},MET))^{2}}, ^{o};N_{events}";
      hCtrlEWKFakeTausQCDTailKillerCollinear.push_back(fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, sName.str().c_str(), sTitle.str().c_str(), 52, 0., 260.));
    }
    hCtrlSelectedTauPtAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlDir, "SelectedTau_pT_AfterStandardSelections", "SelectedTau_pT_AfterStandardSelections;#tau p_{T}, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlSelectedTauEtaAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlDir, "SelectedTau_eta_AfterStandardSelections", "SelectedTau_eta_AfterStandardSelections;#tau #eta;N_{events} / 0.1", 60, -3.0, 3.0);
    hCtrlSelectedTauPhiAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlDir, "SelectedTau_phi_AfterStandardSelections", "SelectedTau_eta_AfterStandardSelections;#tau #phi;N_{events} / 0.087", 72, -3.1415926, 3.1415926);
    hCtrlSelectedTauEtaVsPhiAfterStandardSelections = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myCtrlDir, "SelectedTau_etavsphi_AfterStandardSelections", "SelectedTau_etavsphi_AfterStandardSelections;#tau #eta;#tau #phi", 60, -3.0, 3.0, 36, -3.1415926, 3.1415926);
    hCtrlSelectedTauLeadingTrkPtAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlDir, "SelectedTau_LeadingTrackPt_AfterStandardSelections", "SelectedTau_LeadingTrackPt_AfterStandardSelections;#tau ldg.ch.particle p_{T}, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlSelectedTauRtauAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlDir, "SelectedTau_Rtau_AfterStandardSelections", "SelectedTau_Rtau_AfterStandardSelections;R_{#tau};N_{events} / 0.1", 120, 0., 1.2);
    hCtrlSelectedTauPAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlDir, "SelectedTau_p_AfterStandardSelections", "SelectedTau_p_AfterStandardSelections;#tau p, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlSelectedTauLeadingTrkPAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlDir, "SelectedTau_LeadingTrackP_AfterStandardSelections", "SelectedTau_LeadingTrackP_AfterStandardSelections;#tau ldg.ch.particle p, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlNjetsAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlDir, "Njets_AfterStandardSelections", "Njets_AfterStandardSelections;Number of selected jets;N_{events}", 20, 0., 20.);
    hCtrlEWKFakeTausSelectedTauPtAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, "SelectedTau_pT_AfterStandardSelections", "SelectedTau_pT_AfterStandardSelections;#tau p_{T}, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlEWKFakeTausSelectedTauEtaAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, "SelectedTau_eta_AfterStandardSelections", "SelectedTau_eta_AfterStandardSelections;#tau #eta;N_{events} / 0.1", 60, -3.0, 3.0);
    hCtrlEWKFakeTausSelectedTauPhiAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, "SelectedTau_phi_AfterStandardSelections", "SelectedTau_eta_AfterStandardSelections;#tau #phi;N_{events} / 0.087", 72, -3.1415926, 3.1415926);
    hCtrlEWKFakeTausSelectedTauEtaVsPhiAfterStandardSelections = fHistoWrapper.makeTH<TH2F>(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, "SelectedTau_etavsphi_AfterStandardSelections", "SelectedTau_etavsphi_AfterStandardSelections;#tau #eta;#tau #phi", 60, -3.0, 3.0, 36, -3.1415926, 3.1415926);
    hCtrlEWKFakeTausSelectedTauLeadingTrkPtAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, "SelectedTau_LeadingTrackPt_AfterStandardSelections", "SelectedTau_LeadingTrackPt_AfterStandardSelections;#tau ldg.ch.particle p_{T}, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlEWKFakeTausSelectedTauRtauAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, "SelectedTau_Rtau_AfterStandardSelections", "SelectedTau_Rtau_AfterStandardSelections;R_{#tau};N_{events} / 0.1", 120, 0., 1.2);
    hCtrlEWKFakeTausSelectedTauPAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, "SelectedTau_p_AfterStandardSelections", "SelectedTau_p_AfterStandardSelections;#tau p, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlEWKFakeTausSelectedTauLeadingTrkPAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, "SelectedTau_LeadingTrackP_AfterStandardSelections", "SelectedTau_LeadingTrackP_AfterStandardSelections;#tau ldg.ch.particle p, GeV/c;N_{events} / 5 GeV/c", 80, 0.0, 400.0);
    hCtrlEWKFakeTausNjetsAfterStandardSelections = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myCtrlEWKFakeTausDir, "Njets_AfterStandardSelections", "Njets_AfterStandardSelections;Number of selected jets;N_{events}", 20, 0., 20.);

    // MET selection
    hCtrlMET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "MET", "MET;MET, GeV;N_{events}", 100, 0., 500.);
    hCtrlEWKFakeTausMET = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "MET", "MET;MET, GeV;N_{events}", 100, 0., 500.);

    // b tagging
    hCtrlNbjets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, "NBjets", "NBjets;Number of identified b jets;N_{events}", 20, 0., 20.);
    hCtrlEWKFakeTausNbjets = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, "NBjets", "NBjets;Number of identified b jets;N_{events}", 20, 0., 20.);

    // improved delta phi back to back cuts
    for (int i = 0; i < 4; ++i) {
      std::stringstream sName;
      std::stringstream sTitle;
      sName << "ImprovedDeltaPhiCutsJet" << i << "BackToBack";
      sTitle << "ImprovedDeltaPhiCutsJet" << i << "BackToBack;#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{" << i << "},MET)^{2}}, ^{o};N_{events}";
      hCtrlQCDTailKillerBackToBack.push_back(fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlDir, sName.str().c_str(), sTitle.str().c_str(), 52, 0., 260.));
      sName.str("");
      sTitle.str("");
      sName << "ImprovedDeltaPhiCutsJet" << i << "BackToBackFakeTaus";
      sTitle << "ImprovedDeltaPhiCutsJet" << i << "BackToBackFakeTaus;#sqrt{(180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{" << i << "},MET)^{2}}, ^{o};N_{events}";
      hCtrlEWKFakeTausQCDTailKillerBackToBack.push_back(fHistoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myCtrlEWKFakeTausDir, sName.str().c_str(), sTitle.str().c_str(), 52, 0., 260.));
    }

    // top selection

    // evt topology

    // all selections
    hShapeTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kSystematics, *fs, "shapeTransverseMass", "shapeTransverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 5 GeV/c^{2}", 80, 0., 400.);
    hShapeEWKFakeTausTransverseMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kSystematics, *fs, "shapeEWKFakeTausTransverseMass", "shapeEWKFakeTausTransverseMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 5 GeV/c^{2}", 80, 0., 400.);

    // all selections with full mass
    hShapeFullMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kSystematics, *fs, "shapeInvariantMass", "shapeInvariantMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 5 GeV/c^{2}", 100, 0., 500.);
    hShapeEWKFakeTausFullMass = fHistoWrapper.makeTH<TH1F>(HistoWrapper::kSystematics, *fs, "shapeEWKFakeTausInvariantMass", "shapeEWKFakeTausInvariantMass;m_{T}(tau,MET), GeV/c^{2};N_{events} / 5 GeV/c^{2}", 100, 0., 500.);

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
                               edm::Ptr<pat::Tau>& selectedTau,
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
    edm::Ptr<pat::Tau> mySelectedTau;
    if (selectedTau.isNull()) {
      if (fTauData.passedEvent())
        mySelectedTau = fTauData.getSelectedTau();
    } else {
      mySelectedTau = selectedTau;
    }
    fSelectedTau = mySelectedTau;
    initialize(iEvent,iSetup,
               vertexData,
               fTauData,
               fSelectedTau,
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
                               edm::Ptr<pat::Tau>& selectedTau,
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
    //fTauSelection = &tauSelection;
    fFakeTauIdentifier = &fakeTauIdentifier;
    // Obtain data objects
    fVertexData = vertexData;
    if (!vertexData.passedEvent()) return; // Require valid vertex
    fTauData = tauData;
    edm::Ptr<pat::Tau> mySelectedTau;
    if (selectedTau.isNull()) {
      if (fTauData.passedEvent())
        mySelectedTau = fTauData.getSelectedTau();
    } else {
      mySelectedTau = selectedTau;
    }
    fSelectedTau = mySelectedTau;
    if (fTauData.passedEvent())
      fFakeTauData = fakeTauIdentifier.silentMatchTauToMC(iEvent, *(fSelectedTau));
    fElectronData = eVeto.silentAnalyze(iEvent, iSetup);
    fMuonData = muonVeto.silentAnalyze(iEvent, iSetup, fVertexData.getSelectedVertex());
    if (fTauData.passedEvent())
      fJetData = jetSelection.silentAnalyze(iEvent, iSetup, fSelectedTau, fVertexData.getNumberOfAllVertices());
    else
      fJetData = jetSelection.silentAnalyze(iEvent, iSetup, fVertexData.getNumberOfAllVertices());
    fBJetData = bJetSelection.silentAnalyze(iEvent, iSetup, fJetData.getSelectedJets());
    fTopData = topChiSelection.silentAnalyze(iEvent, iSetup, fJetData.getSelectedJets(), fBJetData.getSelectedJets());
    // Need to require one tau in the event
    if (fSelectedTau.isNull()) {
      fMETData = metSelection.silentAnalyzeNoIsolatedTaus(iEvent, iSetup);
      // Plots do not make sense if no tau has been found
      edm::Ptr<pat::Tau> myZeroTauPointer;
      for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it != hEveryStepHistograms.end(); ++it) {
        (*it)->cacheDataObjects(&fVertexData, 0, fSelectedTau, 0, &fElectronData, &fMuonData, &fJetData, &fMETData, &fBJetData, 0, &fTopData, 0);
      }
      return;
    }
    // A tau exists beyond this point, now obtain MET with residual type I MET
    fMETData = metSelection.silentAnalyze(iEvent, iSetup, vertexData.getNumberOfAllVertices(), fSelectedTau, fJetData.getAllJets());
    // Obtain improved delta phi cut data object
    fQCDTailKillerData = qcdTailKiller.silentAnalyze(iEvent, iSetup, fSelectedTau, fJetData.getSelectedJetsIncludingTau(), fMETData.getSelectedMET());
    // Do full higgs mass only if tau and b jet was found
    if (fBJetData.passedEvent()) {
      fFullHiggsMassData = fullHiggsMassCalculator.silentAnalyze(iEvent, iSetup, fSelectedTau, fBJetData, fMETData);
    }

    // Pass pointer to cached data objects to CommonPlotsFilledAtEveryStep
    if (!hEveryStepHistograms.size())
      throw cms::Exception("Assert") << "CommonPlots::initialize() was called before creating CommonPlots::createCommonPlotsFilledAtEveryStep()!" << endl<<  "  make first all CommonPlots::createCommonPlotsFilledAtEveryStep() and then call CommonPlots::initialize()";
    for (std::vector<CommonPlotsFilledAtEveryStep*>::iterator it = hEveryStepHistograms.begin(); it != hEveryStepHistograms.end(); ++it) {
      (*it)->cacheDataObjects(&fVertexData, &fTauData, fSelectedTau, &fFakeTauData, &fElectronData, &fMuonData, &fJetData, &fMETData, &fBJetData, &fQCDTailKillerData, &fTopData, &fFullHiggsMassData);
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
    if(fTauSelection && fFakeTauIdentifier) {
      fNormalisationAnalysis.analyseTauFakeRate(iEvent, fVertexData, *fTauSelection, fTauData, *fFakeTauIdentifier, fJetData);
    }
  }

  void CommonPlots::fillControlPlotsAfterTauSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const TauSelection::Data& tauData, const FakeTauIdentifier::Data& fakeTauData, const edm::Ptr<pat::Tau>& selectedTau, METSelection& metSelection) {
    fTauData = tauData;
    fFakeTauData = fakeTauData;
    fSelectedTau = selectedTau;
    fMETData = metSelection.silentAnalyze(iEvent, iSetup, fVertexData.getNumberOfAllVertices(), fSelectedTau, fJetData.getAllJets());
    // e->tau normalisation // FIXME tau trg scale factor needs to be applied!
    fNormalisationAnalysis.analyseEToTauFakes(fVertexData, tauData, fakeTauData, fElectronData, fMuonData, fJetData, fMETData);
  }

  void CommonPlots::fillControlPlotsAfterTauTriggerScaleFactor(const edm::Event& iEvent) {
    fMETPhiOscillationCorrectionAfterTaus.analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
    hTauPhiOscillationX->Fill(fVertexData.getNumberOfAllVertices(), fSelectedTau->px());
    hTauPhiOscillationY->Fill(fVertexData.getNumberOfAllVertices(), fSelectedTau->py());
  }

  void CommonPlots::fillControlPlotsAtTauVetoSelection(const edm::Event& iEvent, const edm::EventSetup& iSetup, const VetoTauSelection::Data& tauVetoData) {
    
  }

  void CommonPlots::fillControlPlotsAtElectronSelection(const edm::Event& iEvent, const ElectronSelection::Data& data) {
    fElectronData = data;
    hCtrlIdentifiedElectronPt->Fill(data.getSelectedElectronPtBeforePtCut());
    if (fFakeTauData.isFakeTau()) hCtrlEWKFakeTausIdentifiedElectronPt->Fill(data.getSelectedElectronPtBeforePtCut());
  }

  void CommonPlots::fillControlPlotsAtMuonSelection(const edm::Event& iEvent, const MuonSelection::Data& data) {
    fMuonData = data;
    hCtrlIdentifiedMuonPt->Fill(data.getSelectedMuonPtBeforePtCut());
    if (fFakeTauData.isFakeTau()) hCtrlEWKFakeTausIdentifiedMuonPt->Fill(data.getSelectedMuonPtBeforePtCut());
    fMETPhiOscillationCorrectionAfterLeptonVeto.analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
  }

  void CommonPlots::fillControlPlotsAtJetSelection(const edm::Event& iEvent, const JetSelection::Data& data) {
    fJetData = data;
    hCtrlNjets->Fill(data.getHadronicJetCount());
    if (fFakeTauData.isFakeTau()) hCtrlEWKFakeTausNjets->Fill(data.getHadronicJetCount());
    fMETPhiOscillationCorrectionAfterNjets.analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
  }

  void CommonPlots::fillControlPlotsAfterMETTriggerScaleFactor(const edm::Event& iEvent) {
    hCtrlNjetsAfterJetSelectionAndMETSF->Fill(fJetData.getHadronicJetCount());
    if (fFakeTauData.isFakeTau()) hCtrlEWKFakeTausNjetsAfterJetSelectionAndMETSF->Fill(fJetData.getHadronicJetCount());
  }

  void CommonPlots::fillControlPlotsAtCollinearDeltaPhiCuts(const edm::Event& iEvent, const QCDTailKiller::Data& data) {
    fQCDTailKillerData = data;
    bool myPassStatus = true;
    for (int i = 0; i < data.getNConsideredJets(); ++i) {
      if (i < 4 && myPassStatus) { // protection
        hCtrlQCDTailKillerCollinear[i]->Fill(data.getRadiusFromCollinearCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau())
          hCtrlEWKFakeTausQCDTailKillerCollinear[i]->Fill(data.getRadiusFromCollinearCorner(i)); // Make control plot before cut
        if (!data.passCollinearCutForJet(i))
          myPassStatus = false;
      }
    }
    // Fill control plots for selected taus after standard selections
    hCtrlSelectedTauRtauAfterStandardSelections->Fill(fTauData.getSelectedTauRtauValue());
    hCtrlSelectedTauLeadingTrkPtAfterStandardSelections->Fill(fSelectedTau->leadPFChargedHadrCand()->pt());
    hCtrlSelectedTauPtAfterStandardSelections->Fill(fSelectedTau->pt());
    hCtrlSelectedTauEtaAfterStandardSelections->Fill(fSelectedTau->eta());
    hCtrlSelectedTauPhiAfterStandardSelections->Fill(fSelectedTau->phi());
    hCtrlSelectedTauEtaVsPhiAfterStandardSelections->Fill(fSelectedTau->eta(), fSelectedTau->phi());
    hCtrlSelectedTauPAfterStandardSelections->Fill(fSelectedTau->p());
    hCtrlSelectedTauLeadingTrkPAfterStandardSelections->Fill(fSelectedTau->leadPFChargedHadrCand()->p());
    if (fFakeTauData.isFakeTau()) {
      hCtrlEWKFakeTausSelectedTauRtauAfterStandardSelections->Fill(fTauData.getSelectedTauRtauValue());
      hCtrlEWKFakeTausSelectedTauLeadingTrkPtAfterStandardSelections->Fill(fSelectedTau->leadPFChargedHadrCand()->pt());
      hCtrlEWKFakeTausSelectedTauPtAfterStandardSelections->Fill(fSelectedTau->pt());
      hCtrlEWKFakeTausSelectedTauEtaAfterStandardSelections->Fill(fSelectedTau->eta());
      hCtrlEWKFakeTausSelectedTauPhiAfterStandardSelections->Fill(fSelectedTau->phi());
      hCtrlEWKFakeTausSelectedTauEtaVsPhiAfterStandardSelections->Fill(fSelectedTau->eta(), fSelectedTau->phi());
      hCtrlEWKFakeTausSelectedTauPAfterStandardSelections->Fill(fSelectedTau->p());
      hCtrlEWKFakeTausSelectedTauLeadingTrkPAfterStandardSelections->Fill(fSelectedTau->leadPFChargedHadrCand()->p());
    }
    // Fill other control plots
    hCtrlNjetsAfterStandardSelections->Fill(fJetData.getHadronicJetCount());
    if (fFakeTauData.isFakeTau()) hCtrlEWKFakeTausNjetsAfterStandardSelections->Fill(fJetData.getHadronicJetCount());
  }

  void CommonPlots::fillControlPlotsAtMETSelection(const edm::Event& iEvent, const METSelection::Data& data) {
    fMETData = data;
    hCtrlMET->Fill(data.getSelectedMET()->et());
    if (fFakeTauData.isFakeTau()) hCtrlEWKFakeTausMET->Fill(data.getSelectedMET()->et());
  }

  void CommonPlots::fillControlPlotsAtBtagging(const edm::Event& iEvent, const BTagging::Data& data) {
    fBJetData = data;
    hCtrlNbjets->Fill(data.getBJetCount());
    if (fFakeTauData.isFakeTau()) hCtrlEWKFakeTausNbjets->Fill(data.getBJetCount());
    fMETPhiOscillationCorrectionAfterBjets.analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
  }

  void CommonPlots::fillControlPlotsAtBackToBackDeltaPhiCuts(const edm::Event& iEvent, const QCDTailKiller::Data& data) {
    fQCDTailKillerData = data;
    bool myPassStatus = true;
    for (int i = 0; i < data.getNConsideredJets(); ++i) {
      if (i < 4 && myPassStatus) { // protection
        hCtrlQCDTailKillerBackToBack[i]->Fill(data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
        if (fFakeTauData.isFakeTau())
          hCtrlEWKFakeTausQCDTailKillerBackToBack[i]->Fill(data.getRadiusFromBackToBackCorner(i)); // Make control plot before cut
        if (!data.passBackToBackCutForJet(i))
          myPassStatus = false;
      }
    }
  }

  void CommonPlots::fillControlPlotsAtTopSelection(const edm::Event& iEvent, const TopChiSelection::Data& data) {
    
  }

  void CommonPlots::fillControlPlotsAtEvtTopology(const edm::Event& iEvent, const EvtTopology::Data& data) {
    
  }

  void CommonPlots::fillControlPlotsAfterAllSelections(const edm::Event& iEvent, double transverseMass) {
    fMETPhiOscillationCorrectionAfterAllSelections.analyze(iEvent, fVertexData.getNumberOfAllVertices(), fMETData);
    //double myDeltaPhiTauMET = DeltaPhi::reconstruct(*(fSelectedTau), *(fMETData.getSelectedMET())) * 57.3; // converted to degrees
    hShapeTransverseMass->Fill(transverseMass);
    if (fFakeTauData.isFakeTau()) hShapeEWKFakeTausTransverseMass->Fill(transverseMass);
  }

  void CommonPlots::fillControlPlotsAfterAllSelectionsWithFullMass(const edm::Event& iEvent, FullHiggsMassCalculator::Data& data) {
    fFullHiggsMassData = data;
    hShapeFullMass->Fill(data.getHiggsMass());
    if (fFakeTauData.isFakeTau()) hShapeEWKFakeTausFullMass->Fill(data.getHiggsMass());
  }
}
