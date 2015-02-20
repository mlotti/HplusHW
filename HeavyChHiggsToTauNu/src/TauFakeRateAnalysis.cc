// -*- c++ -*-
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauFakeRateAnalysis.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

namespace HPlus {
  TauFakeRateAnalysis::TauFakeRateAnalysis(HistoWrapper& histoWrapper) {
    edm::Service<TFileService> fs;
    TFileDirectory myBaseDir = histoWrapper.mkdir(HistoWrapper::kInformative, *fs, "TauFakeRate");

    // Create histograms

    // e -> tau fakes
    TFileDirectory myEtoTauDir = histoWrapper.mkdir(HistoWrapper::kInformative, myBaseDir, "eToTau");
    hEtoTauZmassAll = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_mZ_all", "etotau_mZ_all;m_{ee} / GeV/c^{2};N_{events}", 50, 0, 250);
    hEtoTauZmassDecayMode0 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_mZ_decayMode0", "etotau_mZ_decayMode0;m_{ee} / GeV/c^{2};N_{events}", 50, 0, 250);
    hEtoTauZmassDecayMode1 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_mZ_decayMode1", "etotau_mZ_decayMode1;m_{ee} / GeV/c^{2};N_{events}", 50, 0, 250);
    hEtoTauZmassDecayMode2 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_mZ_decayMode2", "etotau_mZ_decayMode2;m_{ee} / GeV/c^{2};N_{events}", 50, 0, 250);
    hEtoTauTauPtAll = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_taupT_all", "etotau_tauPt_all;#tau p_{T} / GeV/c;N_{events}", 50, 0, 250);
    hEtoTauTauPtDecayMode0 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_taupT_decayMode0", "etotau_tauPt_decayMode0;#tau p_{T} / GeV/c;N_{events}", 50, 0, 250);
    hEtoTauTauPtDecayMode1 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_taupT_decayMode1", "etotau_tauPt_decayMode1;#tau p_{T} / GeV/c;N_{events}", 50, 0, 250);
    hEtoTauTauPtDecayMode2 = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myEtoTauDir, "etotau_taupT_decayMode2", "etotau_tauPt_decayMode2;#tau p_{T} / GeV/c;N_{events}", 50, 0, 250);

    // tau fake rate
    TFileDirectory myTauDebugDir = histoWrapper.mkdir(HistoWrapper::kInformative, myBaseDir, "TauFakeRate");
    hTauVsJetDeltaPt = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauVsJetDeltaPt", "#Deltap_{T}(#tau,jet), GeV/c", 200, -500, 500);
    hTauVsJetDeltaR = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauVsJetDeltaR", "#DeltaR(#tau,jet), GeV/c", 100, 0, .5);
    hTauVsJetMCFlavor = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauVsJetMCFlavor", "MC flavor of jet matching to tau", 30, 0, 30);
    hTauVsJetDeltaPtGenuineTaus = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauVsJetDeltaPttaus", "genuine #tau's: #Deltap_{T}(#tau,jet), GeV/c", 200, -500, 500);
    hTauVsJetDeltaPtElectrons = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauVsJetDeltaPtelectrons", "electrons: #Deltap_{T}(#tau,jet), GeV/c", 200, -500, 500);
    hTauVsJetDeltaPtHeavyFlavor = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauVsJetDeltaPtcb", "cb: #Deltap_{T}(#tau,jet), GeV/c", 200, -500, 500);
    hTauVsJetDeltaRHeavyFlavor = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauVsJetDeltaRcb", "cb: #DeltaR(#tau,jet), GeV/c", 100, 0, .5);
    hTauVsJetDeltaPtLightFlavor = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauVsJetDeltaPtuds", "uds: #Deltap_{T}(#tau,jet), GeV/c", 200, -500, 500);
    hTauVsJetDeltaRLightFlavor = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauVsJetDeltaRuds", "uds: #DeltaR(#tau,jet), GeV/c", 100, 0, .5);

    hTauVsJetTauPtbBefore = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtbBefore", "TauFakeRatePtbBefore;b#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtbleptonicBefore = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtbleptonicBefore", "TauFakeRatePtbleptonicBefore;leptonic b#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtcBefore = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtcBefore", "TauFakeRatePtcBefore;c#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtudsBefore = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtudsBefore", "TauFakeRatePtudsBefore;uds#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtgBefore = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtgBefore", "TauFakeRatePtgBefore;g#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPteBefore = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePteBefore", "TauFakeRatePteBefore;e#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtmuBefore = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtmuBefore", "TauFakeRatePtmuBefore;#mu#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtbAfter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtbAfter", "TauFakeRatePtbAfter;b#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtbleptonicAfter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtbleptonicAfter", "TauFakeRatePtbleptonicAfter;leptonic b#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtcAfter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtcAfter", "TauFakeRatePtcAfter;c#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtudsAfter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtudsAfter", "TauFakeRatePtudsAfter;uds#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtgAfter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtgAfter", "TauFakeRatePtgAfter;g#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPteAfter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePteAfter", "TauFakeRatePteAfter;e#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtmuAfter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtmuAfter", "TauFakeRatePtmuAfter;#mu#rightarrow#tau, #tau p_{T}", 100, 0, 500);

    hTauVsJetTauPtbByJetPtBefore = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtbByJetPtBefore", "TauFakeRatePtbByJetPtBefore;b#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtbleptonicByJetPtBefore = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtbleptonicByJetPtBefore", "TauFakeRatePtbleptonicByJetPtBefore;leptonic b#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtcByJetPtBefore = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtcByJetPtBefore", "TauFakeRatePtcByJetPtBefore;c#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtudsByJetPtBefore = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtudsByJetPtBefore", "TauFakeRatePtudsByJetPtBefore;uds#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtgByJetPtBefore = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtgByJetPtBefore", "TauFakeRatePtgByJetPtBefore;g#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPteByJetPtBefore = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePteByJetPtBefore", "TauFakeRatePteByJetPtBefore;e#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtmuByJetPtBefore = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtmuByJetPtBefore", "TauFakeRatePtmuByJetPtBefore;#mu#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtbByJetPtAfter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtbByJetPtAfter", "TauFakeRatePtbByJetPtAfter;b#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtbleptonicByJetPtAfter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtbleptonicByJetPtAfter", "TauFakeRatePtbleptonicByJetPtAfter;leptonic b#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtcByJetPtAfter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtcByJetPtAfter", "TauFakeRatePtcByJetPtAfter;c#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtudsByJetPtAfter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtudsByJetPtAfter", "TauFakeRatePtudsByJetPtAfter;uds#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtgByJetPtAfter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtgByJetPtAfter", "TauFakeRatePtgByJetPtAfter;g#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPteByJetPtAfter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePteByJetPtAfter", "TauFakeRatePteByJetPtAfter;e#rightarrow#tau, #tau p_{T}", 100, 0, 500);
    hTauVsJetTauPtmuByJetPtAfter = histoWrapper.makeTH<TH1F>(HistoWrapper::kInformative, myTauDebugDir, "TauFakeRatePtmuByJetPtAfter", "TauFakeRatePtmuByJetPtAfter;#mu#rightarrow#tau, #tau p_{T}", 100, 0, 500);
  }
  TauFakeRateAnalysis::~TauFakeRateAnalysis() { }

  void TauFakeRateAnalysis::analyseEToTauFakes(const VertexSelection::Data& vertexData,
                                               const TauSelection::Data& tauData,
                                               const FakeTauIdentifier::Data& fakeTauData,
                                               const ElectronSelection::Data& electronData,
                                               const MuonSelection::Data& muondata,
                                               const JetSelection::Data& jetData,
                                               const METSelection::Data& metData) {
            // TODO: change selection as follows:
    // Strategy A: use Z->ee and tag and probe
    // 1) trg, PV
    // 2) 1 electron
    // 3) mu veto
    // 4) Njets <= 2 or 3
    // 5) if necessary MET < 40 or 50
    // 6) apply tau ID with no Rtau
    // 7) calculate m(ee) (Z->tau_h tau_e gives peak at 

    // Strategy B: take ttbar or Wjets events, look at electrons that overlap with taus and see how often they pass tau ID

    // Make sure vertex has been found
    if (!vertexData.passedEvent()) return;
    // Make sure tau has been found
    if (!tauData.passedEvent()) return;
    // Find one electron that is not compatible with tau
    edm::Ptr<pat::Electron> myElectron;
    int myElectronCount = 0;
    edm::PtrVector<pat::Electron> myElectrons = electronData.getSelectedElectronsTight();
    for (edm::PtrVector<pat::Electron>::iterator i = myElectrons.begin(); i != myElectrons.end(); ++i) {
      double myDeltaR = reco::deltaR(tauData.getSelectedTau()->p4(), (*i)->p4());
      if (myDeltaR > 0.4) {
        ++myElectronCount;
        myElectron = *i;
      }
    }
    if (myElectronCount != 1) return;
    // Require opposite sign of tau and electron
    if (myElectron->charge() == tauData.getSelectedTau()->charge()) return;
    // Calculate Z mass
//     LorentzVector myZCandidate;
//     myZCandidate += tauData.getSelectedTau()->p4();
//     myZCandidate += myElectron->p4();
    double myZCandidateMass = (tauData.getSelectedTau()->p4() + myElectron->p4()).mass();
//     myZCandidate.M();
    // Fill histograms
    hEtoTauZmassAll->Fill(myZCandidateMass);
    if (tauData.getSelectedTau()->decayMode() == 0) {
      hEtoTauZmassDecayMode0->Fill(myZCandidateMass);
    } else if (tauData.getSelectedTau()->decayMode() == 1) {
      hEtoTauZmassDecayMode1->Fill(myZCandidateMass);
    } else if (tauData.getSelectedTau()->decayMode() == 2) {
      hEtoTauZmassDecayMode2->Fill(myZCandidateMass);
    }
    // Select events with Z mass
    if (!(myZCandidateMass > 80 && myZCandidateMass < 100)) return;
    double myTauPt = tauData.getSelectedTau()->pt();
    hEtoTauTauPtAll->Fill(myTauPt);
    if (tauData.getSelectedTau()->decayMode() == 0) {
      hEtoTauTauPtDecayMode0->Fill(myTauPt);
    } else if (tauData.getSelectedTau()->decayMode() == 1) {
      hEtoTauTauPtDecayMode1->Fill(myTauPt);
    } else if (tauData.getSelectedTau()->decayMode() == 2) {
      hEtoTauTauPtDecayMode2->Fill(myTauPt);
    }

  }

  void TauFakeRateAnalysis::analyseTauFakeRate(const edm::Event& iEvent,
                                               const VertexSelection::Data& vertexData,
                                               TauSelection& tauSelection,
                                               const TauSelection::Data& tauData,
                                               FakeTauIdentifier& fakeTauIdentifier,
                                               const JetSelection::Data& jetData) {
        // Require that vertex selection has passed
    if (!vertexData.passedEvent()) return;
    // Obtain a list of taus that have passed all selections except for tau isolation and Rtau
    edm::PtrVector<pat::Tau> myTauList;
    for (edm::PtrVector<pat::Tau>::const_iterator it = tauData.getSelectedTausBeforeIsolation().begin();
         it != tauData.getSelectedTausBeforeIsolation().end(); ++it) {
      // These taus have passed the tau candidate selection, let's apply nprongs cut
      if (tauSelection.getPassesNProngsStatusOfTauObject(*it))
        myTauList.push_back(*it);
    }
    // Require that at least a tau candidate has been found
    if (!myTauList.size()) return;
    // Loop over taus
    for (edm::PtrVector<pat::Tau>::const_iterator iTau = myTauList.begin(); iTau != myTauList.end(); ++iTau) {
      // Match tau to jet
      double myMinDeltaR = 99.;
      size_t mySelectedIndex = 0;
      for (size_t j = 0; j < jetData.getAllJets().size(); ++j) {
        if (!(jetData.getAllJets()[j]->pt() > 20. && std::abs(jetData.getAllJets()[j]->eta()) < 2.5)) continue;
        double myDeltaR = reco::deltaR((*iTau)->p4(), jetData.getAllJets()[j]->p4());
        if (myDeltaR < myMinDeltaR) {
          myMinDeltaR = myDeltaR;
          mySelectedIndex = j;
        }
      }
      if (!(myMinDeltaR < 0.4)) continue;
      const edm::Ptr<pat::Jet> myRefJet = jetData.getAllJets()[mySelectedIndex];
      // Reference jet has been found
      int myFlavor = std::abs(myRefJet->partonFlavour());
      // Skip genuine taus
      FakeTauIdentifier::Data tauMatchData = fakeTauIdentifier.silentMatchTauToMC(iEvent, **iTau);
      if (!fakeTauIdentifier.isFakeTau(tauMatchData.getTauMatchType())) continue;
      // Fill values before isolation
      if (fakeTauIdentifier.isElectronToTau(tauMatchData.getTauMatchType())) {
        hTauVsJetTauPteBefore->Fill((*iTau)->pt());
        hTauVsJetTauPteByJetPtBefore->Fill(myRefJet->pt());
        if (myFlavor == 5) {
          hTauVsJetTauPtbleptonicBefore->Fill((*iTau)->pt());
          hTauVsJetTauPtbleptonicByJetPtBefore->Fill(myRefJet->pt());
        }
      } else if (fakeTauIdentifier.isMuonToTau(tauMatchData.getTauMatchType())) {
        hTauVsJetTauPtmuBefore->Fill((*iTau)->pt());
        hTauVsJetTauPtmuByJetPtBefore->Fill(myRefJet->pt());
        if (myFlavor == 5) {
          hTauVsJetTauPtbleptonicBefore->Fill((*iTau)->pt());
          hTauVsJetTauPtbleptonicByJetPtBefore->Fill(myRefJet->pt());
        }
      } else if (myFlavor >= 1 && myFlavor <= 3) {
        hTauVsJetTauPtudsBefore->Fill((*iTau)->pt());
        hTauVsJetTauPtudsByJetPtBefore->Fill(myRefJet->pt());
      } else if (myFlavor == 4) {
        hTauVsJetTauPtcBefore->Fill((*iTau)->pt());
        hTauVsJetTauPtcByJetPtBefore->Fill(myRefJet->pt());
      } else if (myFlavor == 5) {
        hTauVsJetTauPtbBefore->Fill((*iTau)->pt());
        hTauVsJetTauPtbByJetPtBefore->Fill(myRefJet->pt());
      } else if (myFlavor == 21) {
        hTauVsJetTauPtgBefore->Fill((*iTau)->pt());
        hTauVsJetTauPtgByJetPtBefore->Fill(myRefJet->pt());
      }
      // Require that tau passes isolation
      if (!tauSelection.getPassesIsolationStatusOfTauObject(*iTau)) continue;
      // Fill values after isolation
      if (fakeTauIdentifier.isElectronToTau(tauMatchData.getTauMatchType())) {
        hTauVsJetTauPteAfter->Fill((*iTau)->pt());
        hTauVsJetTauPteByJetPtAfter->Fill(myRefJet->pt());
        if (myFlavor == 5) {
          hTauVsJetTauPtbleptonicAfter->Fill((*iTau)->pt());
          hTauVsJetTauPtbleptonicByJetPtAfter->Fill(myRefJet->pt());
        }
      } else if (fakeTauIdentifier.isMuonToTau(tauMatchData.getTauMatchType())) {
        hTauVsJetTauPtmuAfter->Fill((*iTau)->pt());
        hTauVsJetTauPtmuByJetPtAfter->Fill(myRefJet->pt());
        if (myFlavor == 5) {
          hTauVsJetTauPtbleptonicAfter->Fill((*iTau)->pt());
          hTauVsJetTauPtbleptonicByJetPtAfter->Fill(myRefJet->pt());
        }
      } else if (myFlavor >= 1 && myFlavor <= 3) {
        hTauVsJetTauPtudsAfter->Fill((*iTau)->pt());
        hTauVsJetTauPtudsByJetPtAfter->Fill(myRefJet->pt());
      } else if (myFlavor == 4) {
        hTauVsJetTauPtcAfter->Fill((*iTau)->pt());
        hTauVsJetTauPtcByJetPtAfter->Fill(myRefJet->pt());
      } else if (myFlavor == 5) {
        hTauVsJetTauPtbAfter->Fill((*iTau)->pt());
        hTauVsJetTauPtbByJetPtAfter->Fill(myRefJet->pt());
      } else if (myFlavor == 21) {
        hTauVsJetTauPtgAfter->Fill((*iTau)->pt());
        hTauVsJetTauPtgByJetPtAfter->Fill(myRefJet->pt());
      }
    }

    // Calculate delta pT for selected tau after full tauID
    if (!tauData.passedEvent()) return;
    // Require reference jet for selected tau
    if (jetData.getReferenceJetToTau().isNull()) return;
    double myDeltaPt = jetData.getReferenceJetToTauDeltaPt();
    int myFlavor = std::abs(jetData.getReferenceJetToTauPartonFlavour());
    hTauVsJetDeltaPt->Fill(myDeltaPt);
    hTauVsJetDeltaR->Fill(jetData.getReferenceJetToTauMatchDeltaR());
    hTauVsJetMCFlavor->Fill(myFlavor);
    if (myFlavor >= 4 && myFlavor <= 5) {
      hTauVsJetDeltaPtHeavyFlavor->Fill(myDeltaPt);
      hTauVsJetDeltaRHeavyFlavor->Fill(jetData.getReferenceJetToTauMatchDeltaR());
    } else if (myFlavor >= 1 && myFlavor <= 3) {
      hTauVsJetDeltaPtLightFlavor->Fill(myDeltaPt);
      hTauVsJetDeltaRLightFlavor->Fill(jetData.getReferenceJetToTauMatchDeltaR());
    }
  }
}
