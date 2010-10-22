#include "PhysicsTools/PatUtils/interface/TriggerHelper.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "TMath.h"
//#include "FWCore/ServiceRegistry/interface/Service.h"
//#include "PhysicsTools/UtilAlgos/interface/TFileService.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include <string>
#include <vector>

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

class TauHLTMatchProducer : public edm::EDProducer {
 public:
  TauHLTMatchProducer(const edm::ParameterSet& iConfig);
  ~TauHLTMatchProducer();

 private:
  virtual void beginJob() ;
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();
      
  edm::InputTag fTriggerSource;
  edm::InputTag fTriggerEventSource;
  edm::InputTag fTauSource;
  std::string fHLTTriggerName;

};


TauHLTMatchProducer::TauHLTMatchProducer( const edm::ParameterSet & iConfig ) :
  fTriggerSource(iConfig.getParameter<edm::InputTag>("trigger")),
  fTriggerEventSource(iConfig.getParameter<edm::InputTag>("triggerEvent")),
  fTauSource(iConfig.getParameter<edm::InputTag>("tauCollections")),
  fHLTTriggerName(iConfig.getParameter<std::string>("hltTriggerForMatching")) {
}

TauHLTMatchProducer::~TauHLTMatchProducer() {
}

void TauHLTMatchProducer::beginJob() {
}

void TauHLTMatchProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup ) {
  // PAT trigger information
  /*  edm::Handle<pat::TriggerEvent> myTriggerEvent;
  iEvent.getByLabel(fTriggerEventSource, myTriggerEvent);
  edm::Handle<pat::TriggerPathCollection> myTriggerPaths;
  iEvent.getByLabel(fTriggerSource, myTriggerPaths);
  edm::Handle<pat::TriggerFilterCollection> myTriggerFilters;
  iEvent.getByLabel(fTriggerSource, myTriggerFilters);
  edm::Handle<pat::TriggerObjectCollection> myTriggerObjects;
  iEvent.getByLabel(fTriggerSource, myTriggerObjects);
  */

  // PAT trigger object collection
  edm::Handle<edm::Association< std::vector<pat::TriggerObject> > > myPatTriggerEvent;
  iEvent.getByLabel(fPatTriggerEventSource, myPatTriggerEvent);
  


  // PAT tau collection
  edm::Handle<pat::TauCollection> myTaus;
  iEvent.getByLabel(fTauSource, myTaus);

  // PAT trigger helper for trigger matching information
  const pat::helper::TriggerMatchHelper myMatchHelper;

  // Do matching
  double myBestDeltaR = 999;
  size_t myBestTauIndex = 0;
  int myGoodTaus = 0;
  for ( size_t iTau = 0; iTau < myTaus->size(); ++iTau ) {
    if (fabs(myTaus->at(iTau).eta() > 2.4) || myTaus->at(iTau).et() < 20) continue;
    ++myGoodTaus;
    const pat::TriggerObjectRef myTrigRef(myMatchHelper.triggerMatchObject(myTaus, iTau, fHLTTriggerName, iEvent, *myTriggerEvent));
    if (myTrigRef.isAvailable()) {  // check references (necessary!)
      std::cout << "*" << std::endl;
      // decide by deltaR
      double myDeltaR = deltaR(myTaus->at(iTau).eta(), myTaus->at(iTau).phi(), myTrigRef->eta(), myTrigRef->phi());
      if (myDeltaR < myBestDeltaR) {
	myBestDeltaR = myDeltaR;
	myBestTauIndex = iTau;
      }
    }
  }
 
  std::cout << "taus=" << myGoodTaus << "/" << myTaus->size() << " match: DR=" << myBestDeltaR << " index=" << myBestTauIndex << std::endl;

  // mean pt
  
}

void TauHLTMatchProducer::endJob() {
}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(TauHLTMatchProducer);
