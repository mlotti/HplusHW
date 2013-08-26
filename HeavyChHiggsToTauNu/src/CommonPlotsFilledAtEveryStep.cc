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
