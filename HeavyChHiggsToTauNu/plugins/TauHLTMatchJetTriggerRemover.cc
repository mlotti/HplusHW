// -*- C++ -*-
//
// Package:    TauHLTMatchJetTriggerRemover
// Class:      TauHLTMatchJetTriggerRemover
// 
/**\class TauHLTMatchJetTriggerRemover TauHLTMatchJetTriggerRemover.cc HiggsAnalysis/HeavyChHiggsToTauNu/plugins/TauHLTMatchJetTriggerRemover.cc

 Description: Takes as input two patTauCollections (one matched to HLT tau trigger and one matched to HLT jet trigger);
              produces a patTauCollection with the highest patTau matching to the jet trigger removed

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  Lauri A. Wendland
//
// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
 
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
 
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/Math/interface/deltaR.h"

//
// class declaration
//

class TauHLTMatchJetTriggerRemover : public edm::EDProducer {
 public:
  explicit TauHLTMatchJetTriggerRemover(const edm::ParameterSet&);
  ~TauHLTMatchJetTriggerRemover();

 private:
  virtual void produce(edm::Event&, const edm::EventSetup&);
  edm::InputTag fTausMatchedToTauTriggerSource;
  edm::InputTag fTausMatchedToJetTriggerSource;
};

TauHLTMatchJetTriggerRemover::TauHLTMatchJetTriggerRemover(const edm::ParameterSet& iConfig) :
  fTausMatchedToTauTriggerSource(iConfig.getParameter<edm::InputTag>("tausMatchedToTauTriggerSrc")),
  fTausMatchedToJetTriggerSource(iConfig.getParameter<edm::InputTag>("tausMatchedToJetTriggerSrc")) {

  produces<pat::TauCollection>("");
}

TauHLTMatchJetTriggerRemover::~TauHLTMatchJetTriggerRemover() {
}

void TauHLTMatchJetTriggerRemover::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  std::auto_ptr<pat::TauCollection> myCleanedTauCollection(new pat::TauCollection);

  edm::Handle<pat::TauCollection> myTausMatchedToTauTrigger; 
  iEvent.getByLabel(fTausMatchedToTauTriggerSource, myTausMatchedToTauTrigger);
  edm::Handle<pat::TauCollection> myTausMatchedToJetTrigger; 
  iEvent.getByLabel(fTausMatchedToJetTriggerSource, myTausMatchedToJetTrigger);

  // Obtain highest tau matched to jet trigger (should be the first one, but let's make sure)
  pat::TauCollection::const_iterator itHighestJetMatchedTau;
  double myHighestJetMatchedTauPt = 0.;
  for (pat::TauCollection::const_iterator itJet = myTausMatchedToJetTrigger->begin();
       itJet != myTausMatchedToJetTrigger->end(); ++itJet) {
    if ((*itJet).pt() > myHighestJetMatchedTauPt) {
      myHighestJetMatchedTauPt = (*itJet).pt();
      itHighestJetMatchedTau = itJet;
    }
  }
  // Loop over taus matched to tau trigger and store all taus that do not match to the
  // highest tau matching to the jet trigger
  for (pat::TauCollection::const_iterator itTau = myTausMatchedToTauTrigger->begin();
       itTau != myTausMatchedToTauTrigger->end(); ++itTau) {
    if (myHighestJetMatchedTauPt > 0) {
      // make DeltaR matching
      double myDeltaR = reco::deltaR(*itTau, *itHighestJetMatchedTau);
      // store only if DeltaR does not match well
      if (myDeltaR > 0.05)
	myCleanedTauCollection->push_back(*itTau);
    } else { // nothing to clean, store all
      myCleanedTauCollection->push_back(*itTau);
    }
  }

  // Store cleaned tau collection
  iEvent.put(myCleanedTauCollection);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TauHLTMatchJetTriggerRemover);
