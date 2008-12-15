#ifndef IterativeTrackCollectionProducer_h
#define IterativeTrackCollectionProducer_h

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"

using namespace edm;
using namespace std;

class IterativeTrackCollectionProducer : public edm::EDProducer {
   public:
      explicit IterativeTrackCollectionProducer(const edm::ParameterSet&);
      virtual ~IterativeTrackCollectionProducer();

      virtual void produce(edm::Event&, const edm::EventSetup&);
 private:
};
#endif
