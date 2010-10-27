// -*- C++ -*-
//
// Package:    GoodVertexCounter
// Class:      GoodVertexCounter
// 
/**\class GoodVertexCounter GoodVertexCounter.cc TauAnalysis/TauIdEfficiency/plugins/GoodVertexCounter.cc

 Description: Writes the number of good vertices in the event into the edmntuple

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  Copied and edited from Andrea RIZZI's DPGAnalysis/Skims/src/GoodVertexFilter.cc
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
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
//
// class declaration
//

class GoodVertexCounter : public edm::EDProducer {
 public:
  explicit GoodVertexCounter(const edm::ParameterSet&);
  ~GoodVertexCounter();

 private:
  virtual void produce(edm::Event&, const edm::EventSetup&);
  edm::InputTag vertexSrc;        
  unsigned int minNDOF;
  double maxAbsZ;
  double maxd0;
};

GoodVertexCounter::GoodVertexCounter(const edm::ParameterSet& iConfig) {
  vertexSrc = iConfig.getParameter<edm::InputTag>("vertexCollection");
  minNDOF = iConfig.getParameter<unsigned int>("minimumNDOF");
  maxAbsZ = iConfig.getParameter<double>("maxAbsZ");
  maxd0 = iConfig.getParameter<double>("maxd0");

  produces<reco::VertexCollection>("GoodVertexCollection");
  produces<int>("GoodVertexCount");
}

GoodVertexCounter::~GoodVertexCounter() {
}

void GoodVertexCounter::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  std::auto_ptr<reco::VertexCollection> myGoodVertexCollection(new reco::VertexCollection);
  std::auto_ptr<int> myResult(new int);
  *myResult = 0;
  edm::Handle<reco::VertexCollection> pvHandle; 
  iEvent.getByLabel(vertexSrc,pvHandle);
  const reco::VertexCollection & vertices = *pvHandle.product();
  for (reco::VertexCollection::const_iterator it = vertices.begin(); it != vertices.end(); ++it) {
    if (it->ndof() > minNDOF && 
	((maxAbsZ <=0) || fabs(it->z()) <= maxAbsZ) &&
	((maxd0 <=0) || fabs(it->position().rho()) <= maxd0)) {
      ++(*myResult);
      myGoodVertexCollection->push_back(*it);
    }
  }
  iEvent.put(myGoodVertexCollection, "GoodVertexCollection");
  iEvent.put(myResult, "GoodVertexCount");
}

//define this as a plug-in
DEFINE_FWK_MODULE(GoodVertexCounter);
