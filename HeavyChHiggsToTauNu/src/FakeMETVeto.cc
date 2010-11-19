#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

namespace HPlus {
  FakeMETVeto::Data::Data(const FakeMETVeto *fakeMETVeto, bool passedEvent):
    fFakeMETVeto(fakeMETVeto), fPassedEvent(passedEvent) {}
  FakeMETVeto::Data::~Data() {}
  
  FakeMETVeto::FakeMETVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fMaxDeltaPhi(iConfig.getUntrackedParameter<double>("maxDeltaPhi")),
    //fCount(eventCounter.addCounter(" ")),
    fEventWeight(eventWeight) {
    edm::Service<TFileService> fs;
    hClosestDeltaPhi = fs->make<TH1F>("Closest_DeltaPhi_of_MET_and_selected_jets_or_taus", "min DeltaPhi(MET,selected jets or taus;#Delta#phi;N / 0.01", 50, 0., 0.5);
    hClosestDeltaPhiToJets = fs->make<TH1F>("Closest_DeltaPhi_of_MET_and_selected_jets", "min DeltaPhi(MET,selected jets;#Delta#phi;N / 0.01", 50, 0., 0.5);
    hClosestDeltaPhiToTaus = fs->make<TH1F>("Closest_DeltaPhi_of_MET_and_selected_jets", "min DeltaPhi(MET,selected taus;#Delta#phi;N / 0.01", 50, 0., 0.5);
  }

  FakeMETVeto::~FakeMETVeto() {}

  FakeMETVeto::Data FakeMETVeto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus, const edm::PtrVector<pat::Jet>& jets) {
    bool passEvent = false;
    edm::Handle<edm::View<reco::MET> > metHandle;
    iEvent.getByLabel(fSrc, metHandle);
    edm::Ptr<reco::MET> met = metHandle->ptrAt(0);

    // Loop over selected taus
    fClosestDeltaPhiToTaus = 999.;
    for(edm::PtrVector<reco::Candidate>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
      double myDeltaPhi = reco::deltaPhi(*met, **iter);
      if (myDeltaPhi < fClosestDeltaPhiToTaus)
        fClosestDeltaPhiToTaus = myDeltaPhi;
    }
    hClosestDeltaPhiToTaus->Fill(fClosestDeltaPhiToTaus, fEventWeight.getWeight());
    
    // Loop over selected jets
    fClosestDeltaPhiToJets = 999.;
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      double myDeltaPhi = reco::deltaPhi(*met, **iter);
      if (myDeltaPhi < fClosestDeltaPhiToJets)
        fClosestDeltaPhiToJets = myDeltaPhi;
    }
    hClosestDeltaPhiToJets->Fill(fClosestDeltaPhiToJets, fEventWeight.getWeight());

    // Combine results
    if (fClosestDeltaPhiToJets < fClosestDeltaPhiToTaus) {
      fClosestDeltaPhi = fClosestDeltaPhiToJets;
    } else {
      fClosestDeltaPhi = fClosestDeltaPhiToTaus;
    }
    hClosestDeltaPhi->Fill(fClosestDeltaPhi, fEventWeight.getWeight());

    // Make cut
    passEvent = true; 
    if (fClosestDeltaPhi > fMaxDeltaPhi)
      passEvent = false;

    return Data(this, passEvent);
  }
}
