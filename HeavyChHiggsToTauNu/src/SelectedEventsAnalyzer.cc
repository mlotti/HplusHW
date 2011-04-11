// -*- c++ -*-
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SelectedEventsAnalyzer.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"

namespace HPlus {
  SelectedEventsAnalyzer::SelectedEventsAnalyzer(std::string prefix) {
    edm::Service<TFileService> fs;
    std::string myName;
    // Create histograms
    myName = prefix + "_TauPtAfterAllSelections";
    hTauPtAfterAllSelections = fs->make<TH1F>(myName.c_str(), "TauPtAfterAllSelections;tau p_{T}, GeV/c;N_{events}/5", 60, 0., 300.);
    hTauPtAfterAllSelections->Sumw2();
    myName = prefix + "_TauEtaAfterAllSelections";
    hTauEtaAfterAllSelections = fs->make<TH1F>(myName.c_str(), "TauEtaAfterAllSelections;tau #eta;N_{events}/0.1", 60, -3.0, 3.0);
    hTauEtaAfterAllSelections->Sumw2();
    myName = prefix + "_TauPhiAfterAllSelections";
    hTauPhiAfterAllSelections = fs->make<TH1F>(myName.c_str(), "TauPhiAfterAllSelections;tau #phi;N_{events}/5^{o}", 72, -180., 180.);
    hTauPhiAfterAllSelections->Sumw2();
    myName = prefix + "_RTauAfterAllSelections";
    hRTauAfterAllSelections = fs->make<TH1F>(myName.c_str(), "RTauAfterAllSelections;Rtau;N_{events}/0.02", 60, 0., 1.2);
    hRTauAfterAllSelections->Sumw2();
    myName = prefix + "_NJetsAfterAllSelections";
    hNJetsAfterAllSelections = fs->make<TH1F>(myName.c_str(), "NJetsAfterAllSelections;N_{hadronic jets};N_{events}", 10, 0., 10.);
    hNJetsAfterAllSelections->Sumw2();
    myName = prefix + "_BJetsAfterAllSelections";
    hBJetsAfterAllSelections = fs->make<TH1F>(myName.c_str(), "BJetsAfterAllSelections;N_{b-tagged jets};N_{events}", 10, 0., 10.);
    hBJetsAfterAllSelections->Sumw2();
    myName = prefix + "_METJetsAfterAllSelections";
    hMETAfterAllSelections = fs->make<TH1F>(myName.c_str(), "METAfterAllSelections;MET, GeV;N_{events} / 5 GeV", 60, 0., 300.);
    hMETAfterAllSelections->Sumw2();
    myName = prefix + "_METPhiAfterAllSelections";
    hMETPhiAfterAllSelections = fs->make<TH1F>(myName.c_str(), "METPhiAfterAllSelections;MET #phi;N_{events} / 5^{o}", 72, -180., 180.);
    hMETPhiAfterAllSelections->Sumw2();
    myName = prefix + "_FakeMETVetoAfterAllSelections";
    hFakeMETVetoAfterAllSelections = fs->make<TH1F>(myName.c_str(), "FakeMETVetoAfterAllSelections;min(#Delta#phi(MET, jets)), degrees;N_{events} / 5^{o}", 36, 0., 180.);
    hFakeMETVetoAfterAllSelections->Sumw2();
    myName = prefix + "_DeltaPhiTauMETAfterAllSelections";
    hDeltaPhiAfterAllSelections = fs->make<TH1F>(myName.c_str(), "DeltaPhiAfterAllSelections;#Delta#phi(MET, #tau), degrees;N_{events} / 5 degrees", 36, 0., 180.);
    hDeltaPhiAfterAllSelections->Sumw2();
    myName = prefix + "_TransverseMassAfterAllSelections";
    hTransverseMassAfterAllSelections = fs->make<TH1F>(myName.c_str(), "TransverseMassAfterAllSelections;m_{T}(MET, #tau), GeV/c^{2};N_{events} / 5 GeV/c^{2}", 60, 0., 300.);
    hTransverseMassAfterAllSelections->Sumw2();
  }

  SelectedEventsAnalyzer::~SelectedEventsAnalyzer() { }

  void SelectedEventsAnalyzer::fill(edm::PtrVector<pat::Tau>& selectedTau,
				    const TauSelection::Data& tauData,
				    const GlobalElectronVeto::Data& eVetoData,
				    const GlobalMuonVeto::Data& muVetoData,
				    const JetSelection::Data& jetData,
				    const BTagging::Data& btagData,
				    const METSelection::Data& METData,
				    const FakeMETVeto::Data& fakeMETVetoData,
				    const ForwardJetVeto::Data& forwardVetoData,
				    const double weight) {
    // Tau related
    hTauPtAfterAllSelections->Fill(selectedTau[0]->pt(), weight);
    hTauEtaAfterAllSelections->Fill(selectedTau[0]->eta(), weight);
    hTauPhiAfterAllSelections->Fill(selectedTau[0]->phi(), weight);
    if (tauData.getSelectedTaus().size()) {
      hRTauAfterAllSelections->Fill(tauData.getRtauOfSelectedTau(), weight);
    } else {
      // This should happen only when TauSelection is run with tau candidate selection only (or anti-isolation)
      hRTauAfterAllSelections->Fill(tauData.selectedTauCandidatePassedRtau(), weight);
    }
    // Global e/mu veto

    // Jets and b-jets
    hNJetsAfterAllSelections->Fill(jetData.getHadronicJetCount(), weight);
    hBJetsAfterAllSelections->Fill(btagData.getBJetCount(), weight);
    // MET
    hMETAfterAllSelections->Fill(METData.getSelectedMET()->et(), weight);
    hMETPhiAfterAllSelections->Fill(METData.getSelectedMET()->phi(), weight);
    // Fake MET veto
    hFakeMETVetoAfterAllSelections->Fill(fakeMETVetoData.closestDeltaPhi(), weight);
    // Forward jets veto

    // Transverse mass
    hDeltaPhiAfterAllSelections->Fill(fDeltaPhi.reconstruct(*(selectedTau[0]), *(METData.getSelectedMET()))*180.0/3.14159, weight);
    hTransverseMassAfterAllSelections->Fill(fTransverseMass.reconstruct(*(selectedTau[0]), *(METData.getSelectedMET())), weight);
  }

}
