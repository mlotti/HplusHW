// -*- c++ -*-
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/CommonPlotsFilledAtEveryStep.h"

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
    hFakeTauStatus = histoWrapper.makeTH<TH1F>(HistoWrapper::kVital, myDir, "tau_fakeStatus", "tau_fakeStatus;N_{events}", 26, 0, 26);
    if (hFakeTauStatus->isActive()) {
      // items labeled 'main count' sum up to Nevents (useful if you want to know the fractions)
      hFakeTauStatus->GetXaxis()->SetBinLabel(1, "All events"); // control to give Nevents
      hFakeTauStatus->GetXaxis()->SetBinLabel(2, "1-pr. #tau"); // main count
      hFakeTauStatus->GetXaxis()->SetBinLabel(3, "3-pr. #tau"); // main count
      hFakeTauStatus->GetXaxis()->SetBinLabel(4, "e#rightarrow#tau"); // main count
      hFakeTauStatus->GetXaxis()->SetBinLabel(5, "#mu#rightarrow#tau"); // main count
      hFakeTauStatus->GetXaxis()->SetBinLabel(6, "jet#rightarrow#tau"); // main count
      hFakeTauStatus->GetXaxis()->SetBinLabel(7, "uds#rightarrow#tau"); // subcount of jet->tau
      hFakeTauStatus->GetXaxis()->SetBinLabel(8, "cb#rightarrow#tau"); // subcount of jet->tau
      hFakeTauStatus->GetXaxis()->SetBinLabel(9, "g#rightarrow#tau"); // subcount of jet->tau
      hFakeTauStatus->GetXaxis()->SetBinLabel(10, "#tau#rightarrowe#rightarrow#tau"); // subcount of jet->tau
      hFakeTauStatus->GetXaxis()->SetBinLabel(11, "#tau#rightarrow#mu#rightarrow#tau"); // subcount of jet->tau
      // Additional non-matched hadronic tau lepton in acceptance
      hFakeTauStatus->GetXaxis()->SetBinLabel(12, "#tau+#tau_{h}"); // subcount of tau->tau
      hFakeTauStatus->GetXaxis()->SetBinLabel(13, "e#rightarrow#tau+#tau_{h}"); // subcount of e->tau
      hFakeTauStatus->GetXaxis()->SetBinLabel(14, "#mu#rightarrow#tau+#tau_{h}"); // subcount of mu->tau
      hFakeTauStatus->GetXaxis()->SetBinLabel(15, "jet#rightarrow#tau+#tau_{h}"); // subcount of jet->tau
      // Background type
      hFakeTauStatus->GetXaxis()->SetBinLabel(16, "bkg:QCD"); // main count 2
      hFakeTauStatus->GetXaxis()->SetBinLabel(17, "bkg:emb."); // main count 2
      hFakeTauStatus->GetXaxis()->SetBinLabel(18, "bkg:fake"); // main count 2
      hFakeTauStatus->GetXaxis()->SetBinLabel(19, "bkg:unkn."); // main count 2
      // Tau origin
      hFakeTauStatus->GetXaxis()->SetBinLabel(20, "orig.W->fake#tau"); // subcount of e/mu->tau
      hFakeTauStatus->GetXaxis()->SetBinLabel(21, "orig.Z->fake#tau"); // subcount of e/mu->tau
      hFakeTauStatus->GetXaxis()->SetBinLabel(22, "orig.H+->fake#tau"); // subcount of e/mu->tau
      hFakeTauStatus->GetXaxis()->SetBinLabel(23, "orig.W#rightarrow#tau"); // subcount of tau->tau
      hFakeTauStatus->GetXaxis()->SetBinLabel(24, "orig.Z#rightarrow#tau#tau"); // subcount of tau->tau
      hFakeTauStatus->GetXaxis()->SetBinLabel(25, "orig.H+#rightarrow#tau#nu"); // subcount of tau->tau
      hFakeTauStatus->GetXaxis()->SetBinLabel(26, "orig.unkn."); // jet->tau
    }
    hTauPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "tau_pT", "tau_pT;#tau p_{T}, GeV/c;N_{events}", 100, 0.0, 500.0);
    hTauEta = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "tau_eta", "tau_eta;#tau #eta;N_{events}", 50, -2.5, 2.5);
    hTauPhi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "tau_phi", "tau_phi;#tau #phi;N_{events}", 72, -3.1415926, 3.1415926);
    hRtau = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "tau_Rtau", "tau_Rtau;R_{#tau};N_{events}", 60, 0.0, 1.2);
    hSelectedElectrons = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "electrons_N", "electrons_N;N_{electrons};N_{events}", 40, 0.0, 40.);
    hSelectedMuons = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "muons_N", "muons_N;N_{muons};N_{events}", 40, 0.0, 40.);
    hNjets = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jets_N", "jets_N;N_{jets};N_{events}", 20, 0.0, 20.);
    hNjetsAllIdentified = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "jets_N_allIdentified", "jets_N_allIdentified;N_{jets};N_{events}", 20, 0.0, 20.);
    hMETCalo = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MET_Calo", "MET_Calo;Calo MET, GeV;N_{events}", 100, 0.0, 500.);
    hMETRaw = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MET_Raw", "MET_Raw;Raw MET, GeV;N_{events}", 100, 0.0, 500.);
    hMET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MET_MET", "MET;MET, GeV;N_{events}", 100, 0.0, 500.);
    hMETphi = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MET_phi", "MET_phi;MET #phi;N_{events}", 72, -3.1415926, 3.1415926);
    hMETSignificance = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MET_significance", "MET_significance;MET significance;N_{events}", 100, 0.0, 100.);
    hMETOverTrackPtSum = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MET_over_TrackPtSum", "MET_over_TrackPtSum;MET/0.5/#sqrt{#sum p_{T}^{track}} / #sqrt{GeV};N_{events}", 100, 0.0, 100.);
    hMETOverMHT = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MET_over_MHT", "MET_over_MHT;MET/MHT;N_{events}", 100, 0.0, 50.);
    hMETOverTauPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "MET_over_TauPt", "MET_over_TauPt;MET/#tau pT;N_{events}", 100, 0.0, 50.);
    hNbjets = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "bjets_N", "bjets_N;N_{b jets};N_{events}", 20, 0.0, 20.);
    hDeltaPhiTauMET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "DeltaPhi_TauMET", "DeltaPhi_TauMET;#Delta#phi(#tau,MET);N_{events}", 36, 0.0, 180.);
    hDeltaR_TauMETJet1MET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "hDeltaR_TauMETJet1MET", "hDeltaR_TauMETJet1MET;#sqrt((180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{1},MET)^{2}), ^{o};N_{events}", 52, 0.0, 260.);
    hDeltaR_TauMETJet2MET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "hDeltaR_TauMETJet2MET", "hDeltaR_TauMETJet1MET;#sqrt((180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{2},MET)^{2}), ^{o};N_{events}", 52, 0.0, 260.);
    hDeltaR_TauMETJet3MET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "hDeltaR_TauMETJet3MET", "hDeltaR_TauMETJet1MET;#sqrt((180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{3},MET)^{2}), ^{o};N_{events}", 52, 0.0, 260.);
    hDeltaR_TauMETJet4MET = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "hDeltaR_TauMETJet4MET", "hDeltaR_TauMETJet1MET;#sqrt((180^{o}-#Delta#phi(#tau,MET))^{2}+#Delta#phi(jet_{4},MET)^{2}), ^{o};N_{events}", 52, 0.0, 260.);
    hTopMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "topMass", "topMass;m_{bqq'}, GeV/c^{2};N_{events}", 100, 0., 500.);
    hTopPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "topPt", "topPt;p_{T}(bqq'), GeV/c;N_{events}", 100, 0., 500.);
    hWMass = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WMass", "WMass;m_{qq'}, GeV/c^{2};N_{events}", 60, 0., 300.);
    hWPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "WPt", "WPt;p_{T}(bqq'), GeV/c;N_{events}", 100, 0., 500.);
    hChargedHiggsPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myDir, "HiggsPt", "HiggsPt;p_{T}(#tau,MET), GeV/c;N_{events}", 100, 0., 500.);
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
          if (fFakeTauData->isEmbeddingGenuineTauLike())
            hFakeTauStatus->Fill(9);
        } else if (fFakeTauData->isMuonToTau()) {
          hFakeTauStatus->Fill(4);
          if (fFakeTauData->isEmbeddingGenuineTauLike())
            hFakeTauStatus->Fill(10);
        } else if (fFakeTauData->isJetToTau()) {
          hFakeTauStatus->Fill(5);
          // jet->tau parton details
          if (fJetData->getReferenceJetToTau().isNonnull()) {
            if (fJetData->getReferenceJetToTauPartonFlavour() >= 1 && fJetData->getReferenceJetToTauPartonFlavour() <= 3)
              hFakeTauStatus->Fill(6);
            else if (fJetData->getReferenceJetToTauPartonFlavour() >= 4 && fJetData->getReferenceJetToTauPartonFlavour() <= 5)
              hFakeTauStatus->Fill(7);
            if (fJetData->getReferenceJetToTauPartonFlavour() == 21)
              hFakeTauStatus->Fill(8);
          }
        }
        // Hadronic tau lepton in acceptance
        if (fFakeTauData->getTauMatchType() == FakeTauIdentifier::kkTauToTauAndTauJetInsideAcceptance ||
            fFakeTauData->getTauMatchType() == FakeTauIdentifier::kkOneProngTauToTauAndTauJetInsideAcceptance)
          hFakeTauStatus->Fill(11);
        else if (fFakeTauData->getTauMatchType() == FakeTauIdentifier::kkElectronToTauAndTauJetInsideAcceptance ||
                 fFakeTauData->getTauMatchType() == FakeTauIdentifier::kkElectronFromTauDecayToTauAndTauJetInsideAcceptance)
          hFakeTauStatus->Fill(12);
        else if (fFakeTauData->getTauMatchType() == FakeTauIdentifier::kkMuonToTauAndTauJetInsideAcceptance ||
                 fFakeTauData->getTauMatchType() == FakeTauIdentifier::kkMuonFromTauDecayToTauAndTauJetInsideAcceptance)
          hFakeTauStatus->Fill(13);
        else if (fFakeTauData->getTauMatchType() == FakeTauIdentifier::kkJetToTauAndTauJetInsideAcceptance)
          hFakeTauStatus->Fill(14);
        // Background type
        if (fFakeTauData->isEWKFakeTauLike())
          hFakeTauStatus->Fill(15);
        else if (fFakeTauData->isEmbeddingGenuineTauLikeWithSingleTauInAcceptance())
          hFakeTauStatus->Fill(16);
        else if (fFakeTauData->isEmbeddingGenuineTauLikeWithMultipleTausInAcceptance())
          hFakeTauStatus->Fill(17);
        else
          hFakeTauStatus->Fill(18);
        // Tau origin
        if (fFakeTauData->getTauOriginType() == FakeTauIdentifier::kkFromW)
          hFakeTauStatus->Fill(19);
        else if (fFakeTauData->getTauOriginType() == FakeTauIdentifier::kkFromZ)
          hFakeTauStatus->Fill(20);
        else if (fFakeTauData->getTauOriginType() == FakeTauIdentifier::kkFromHplus)
          hFakeTauStatus->Fill(21);
        else if (fFakeTauData->getTauOriginType() == FakeTauIdentifier::kkFromWTau)
          hFakeTauStatus->Fill(22);
        else if (fFakeTauData->getTauOriginType() == FakeTauIdentifier::kkFromZTauTau)
          hFakeTauStatus->Fill(23);
        else if (fFakeTauData->getTauOriginType() == FakeTauIdentifier::kkFromHplusTau)
          hFakeTauStatus->Fill(24);
        else
          hFakeTauStatus->Fill(25);
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
    if (fMETData->getSelectedMET().isNull()) return;
    hMETCalo->Fill(fMETData->getCaloMET()->et());
    hMETRaw->Fill(fMETData->getRawMET()->et());
    hMET->Fill(fMETData->getSelectedMET()->et());
    hMETphi->Fill(fMETData->getSelectedMET()->phi());
    hMETSignificance->Fill(fMETData->getSelectedMET()->significance());
    hMETOverTrackPtSum->Fill(fMETData->getSelectedMET()->et() / 0.5 / std::sqrt(fVertexData->getTrackSumPt()));
    if (fTauData) {
      hMETOverMHT->Fill(fMETData->getSelectedMET()->et() / fJetData->getMHT());
      hMETOverTauPt->Fill(fMETData->getSelectedMET()->et() / fTauData->getSelectedTau()->pt());
    }
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

    // top reco
    if (fTopData) {
      hTopMass->Fill(fTopData->getTopMass());
      hTopPt->Fill(fTopData->getTopP4().pt());
      hWMass->Fill(fTopData->getWMass());
      hWPt->Fill(fTopData->getWP4().pt());
    }

    // Boost of the Higgs
    hChargedHiggsPt->Fill((fMETData->getSelectedMET()->p4()+fTauData->getSelectedTau()->p4()).pt());

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
                                                      const TopSelectionManager::Data* topData,
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

}
