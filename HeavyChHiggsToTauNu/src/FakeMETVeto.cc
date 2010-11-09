#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/FakeMETVeto.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1F.h"

namespace HPlus {
  FakeMETVeto::Data::Data(const FakeMETVeto *fakeMETVeto, bool passedEvent):
    fFakeMETVeto(fakeMETVeto), fPassedEvent(passedEvent) {}
  FakeMETVeto::Data::~Data() {}
  
  FakeMETVeto::FakeMETVeto(const edm::ParameterSet& iConfig, EventCounter& eventCounter, EventWeight& eventWeight):
    fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
    fMaxDeltaR(iConfig.getUntrackedParameter<double>("maxDeltaR")),
    //fCount(eventCounter.addCounter(" ")),
    fEventWeight(eventWeight) {
    edm::Service<TFileService> fs;
    hClosestDeltaR = fs->make<TH1F>("Closest_DeltaR_of_MET_and_selected_jets_or_taus", "min DeltaR(MET,selected jets or taus;#DeltaR;N / 0.01", 50, 0., 0.5);
    hClosestDeltaRToJets = fs->make<TH1F>("Closest_DeltaR_of_MET_and_selected_jets", "min DeltaR(MET,selected jets;#DeltaR;N / 0.01", 50, 0., 0.5);
    hClosestDeltaRToTaus = fs->make<TH1F>("Closest_DeltaR_of_MET_and_selected_jets", "min DeltaR(MET,selected taus;#DeltaR;N / 0.01", 50, 0., 0.5);
  }

  FakeMETVeto::~FakeMETVeto() {}

  FakeMETVeto::Data FakeMETVeto::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup, const edm::PtrVector<reco::Candidate>& taus, const edm::PtrVector<pat::Jet>& jets) {
    bool passEvent = false;
    edm::Handle<edm::View<reco::MET> > metHandle;
    iEvent.getByLabel(fSrc, metHandle);
    edm::Ptr<reco::MET> met = metHandle->ptrAt(0);

    // Loop over selected taus
    fClosestDeltaRToTaus = 999.;
    for(edm::PtrVector<reco::Candidate>::const_iterator iter = taus.begin(); iter != taus.end(); ++iter) {
      double myDeltaR = reco::deltaR(*met, **iter);
      if (myDeltaR < fClosestDeltaRToTaus)
        fClosestDeltaRToTaus = myDeltaR;
    }
    hClosestDeltaRToTaus->Fill(fClosestDeltaRToTaus, fEventWeight.getWeight());
    
    // Loop over selected jets
    fClosestDeltaRToJets = 999.;
    for(edm::PtrVector<pat::Jet>::const_iterator iter = jets.begin(); iter != jets.end(); ++iter) {
      double myDeltaR = reco::deltaR(*met, **iter);
      if (myDeltaR < fClosestDeltaRToJets)
        fClosestDeltaRToJets = myDeltaR;
    }
    hClosestDeltaRToJets->Fill(fClosestDeltaRToJets, fEventWeight.getWeight());

    // Combine results
    if (fClosestDeltaRToJets < fClosestDeltaRToTaus) {
      fClosestDeltaR = fClosestDeltaRToJets;
    } else {
      fClosestDeltaR = fClosestDeltaRToTaus;
    }
    hClosestDeltaR->Fill(fClosestDeltaR, fEventWeight.getWeight());

    // Make cut
    passEvent = true; 
    if (fClosestDeltaR > fMaxDeltaR)
      passEvent = false;

    return Data(this, passEvent);
  }
}
