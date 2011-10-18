#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MakeTH.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/DeltaPhi.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TLorentzVector.h"

#include "TH1F.h"

namespace HPlus {
  FakeMETVeto::Data::Data(const FakeMETVeto *fakeMETVeto, bool passedEvent):
    fFakeMETVeto(fakeMETVeto), fPassedEvent(passedEvent) {}
  FakeMETVeto::Data::~Data() {}
  
  FakeMETVeto::FakeMETVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fMinDeltaPhi(iConfig.getUntrackedParameter<double>("minDeltaPhi")),
    //fCount(eventCounter.addCounter(" ")),
    fEventWeight(eventWeight) {
    edm::Service<TFileService> fs;
    TFileDirectory myDir = fs->mkdir("FakeMETVeto");
    
    hClosestDeltaPhi = makeTH<TH1F>(myDir, "Closest_DeltaPhi_of_MET_and_selected_jets_or_taus", "min DeltaPhi(MET,selected jets or taus);min(#Delta#phi(MET,jets)), degrees;N / 5", 36, 0., 180.);
    hClosestDeltaPhiToJets = makeTH<TH1F>(myDir, "Closest_DeltaPhi_of_MET_and_selected_jets", "min DeltaPhi(MET,selected jets);min(#Delta#phi(MET,jets)), degrees;N / 5", 36, 0., 180.);
    hClosestDeltaPhiToTaus = makeTH<TH1F>(myDir, "Closest_DeltaPhi_of_MET_and_taus", "min DeltaPhi(MET,selected taus);min(#Delta#phi(MET,jets)), degrees;N / 5", 36, 0., 180.);
    
    hClosestDeltaPhiZoom = makeTH<TH1F>(myDir, "Closest_DeltaPhi_of_MET_and_selected_jets_or_taus_Zoom", "min DeltaPhi(MET,selected jets or taus);min(#Delta#phi(MET,jets)), degrees;N / 2", 25, 0., 50.0);
    hClosestDeltaPhiToJetsZoom = makeTH<TH1F>(myDir, "Closest_DeltaPhi_of_MET_and_selected_jets_Zoom", "min DeltaPhi(MET,selected jets);min(#Delta#phi(MET,jets)), degrees;N / 2", 25, 0., 50.0);
    hClosestDeltaPhiToTausZoom = makeTH<TH1F>(myDir, "Closest_DeltaPhi_of_MET_and_taus_Zoom", "min DeltaPhi(MET,selected taus);min(#Delta#phi(MET,jets)), degrees;N / 2", 25, 0., 50.0);
  }

  FakeMETVeto::~FakeMETVeto() {}

  //  FakeMETVeto::Data FakeMETVeto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met) {
  FakeMETVeto::Data FakeMETVeto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const reco::Candidate& tau, const edm::PtrVector<pat::Jet>& jets, const edm::Ptr<reco::MET>& met) {
    bool passEvent = false;
 

    // Loop over selected taus
    fClosestDeltaPhiToTaus = 999.;
    double fClosestDeltaPhiToTaus = reco::deltaPhi(*met, tau) * 180./3.14159;

    //    for(edm::PtrVector<reco::Candidate>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
    //      double myDeltaPhi = reco::deltaPhi(*met, **iter) * 180./3.14159;
    //      if ( fabs(myDeltaPhi) < fClosestDeltaPhiToTaus)
    //        fClosestDeltaPhiToTaus = fabs(myDeltaPhi);
    //    }
    hClosestDeltaPhiToTaus->Fill(fClosestDeltaPhiToTaus, fEventWeight.getWeight());
    hClosestDeltaPhiToTausZoom->Fill(fClosestDeltaPhiToTaus, fEventWeight.getWeight());
    
    // Loop over selected jets
    fClosestDeltaPhiToJets = 999.;
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      double myDeltaPhi = reco::deltaPhi(*met, **iter) * 180./3.14159;
      if ( fabs(myDeltaPhi) < fClosestDeltaPhiToJets)
        fClosestDeltaPhiToJets = fabs(myDeltaPhi);
    }    hClosestDeltaPhiToJets->Fill(fClosestDeltaPhiToJets, fEventWeight.getWeight());
    hClosestDeltaPhiToJetsZoom->Fill(fClosestDeltaPhiToJets, fEventWeight.getWeight());

    // Combine results - for now take just DeltaPhi(MET,jet) into account 
    //if (fClosestDeltaPhiToJets < fClosestDeltaPhiToTaus) {
    fClosestDeltaPhi = fClosestDeltaPhiToJets; 
    //} else {
    //  fClosestDeltaPhi = fClosestDeltaPhiToTaus;
    //}

    // New: Don't combine results. Take deltaPhi(MET, jets)
    fClosestDeltaPhi = fClosestDeltaPhiToJets;
    hClosestDeltaPhi->Fill(fClosestDeltaPhi, fEventWeight.getWeight());
    hClosestDeltaPhiZoom->Fill(fClosestDeltaPhi, fEventWeight.getWeight());

    // Make cut
    passEvent = true; 
    if (fClosestDeltaPhi < fMinDeltaPhi)
      passEvent = false;

    return Data(this, passEvent);
  }
}
