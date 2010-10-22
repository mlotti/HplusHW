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
      
  edm::InputTag fPatTriggerSource;
  edm::InputTag fTauSource;
  /*  edm::InputTag fTriggerSource;
  edm::InputTag fTriggerEventSource;

  std::string fHLTTriggerName;
  */
};


TauHLTMatchProducer::TauHLTMatchProducer( const edm::ParameterSet & iConfig ) :
  fPatTriggerSource(iConfig.getParameter<edm::InputTag>("patTrigger")),
  fTauSource(iConfig.getParameter<edm::InputTag>("src"))
  /*
  fTriggerSource(iConfig.getParameter<edm::InputTag>("trigger")),
  fTriggerEventSource(iConfig.getParameter<edm::InputTag>("triggerEvent")),

  fHLTTriggerName(iConfig.getParameter<std::string>("hltTriggerForMatching")) */{
}

TauHLTMatchProducer::~TauHLTMatchProducer() {
}

void TauHLTMatchProducer::beginJob() {
}

void TauHLTMatchProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup ) {

  // PAT trigger object collection
  //edm::Handle<edm::Association< std::vector<pat::TriggerObject> > > myPatTriggerEvent;
  //iEvent.getByLabel(fPatTriggerEventSource, myPatTriggerEvent);

  edm::Handle< std::vector<pat::TriggerObject> > myPatTriggerObjects;
  iEvent.getByLabel(fPatTriggerSource, myPatTriggerObjects);

  edm::Handle< std::vector<pat::TriggerAlgorithm> > myPatTriggerAlgorithms;
  iEvent.getByLabel(fPatTriggerSource, myPatTriggerAlgorithms);

  edm::Handle< std::vector<pat::TriggerFilter> > myPatTriggerFilters;
  iEvent.getByLabel(fPatTriggerSource, myPatTriggerFilters);

  // PAT tau collection
  edm::Handle<pat::TauCollection> myTaus;
  iEvent.getByLabel(fTauSource, myTaus);

  std::cout << "trigger objects: " << myPatTriggerObjects->size() << std::endl;
  for (std::vector<pat::TriggerObject>::const_iterator it = myPatTriggerObjects->begin(); it != myPatTriggerObjects->end(); ++it) {
    std::cout << " collection=" << (*it).collection() << " ids:";
    for (std::vector<int>::const_iterator i = (*it).filterIds().begin(); i != (*it).filterIds().end(); ++i) {
      std::cout << " " << *i;
    }
    std::cout << std::endl;
  }


  std::cout << "trigger filters:" << std::endl;
  for (std::vector<pat::TriggerFilter>::const_iterator it = myPatTriggerFilters->begin(); it != myPatTriggerFilters->end(); ++it) {
    std::cout << "  " << (*it).label() << " type=" << (*it).type() << std::endl;
  }

  /*
  std::cout << "trigger algorithms:" << std::endl;
  for (std::vector<pat::TriggerAlgorithm>::const_iterator it = myPatTriggerAlgorithms->begin(); it != myPatTriggerAlgorithms->end(); ++it) {
    std::cout << "  " << (*it).name() << " bit=" << (*it).bit() << " prescale=" << (*it).prescale() << std::endl;
  }
  */


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
  /* 


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
  */
  // mean pt
  
}

void TauHLTMatchProducer::endJob() {
}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(TauHLTMatchProducer);
