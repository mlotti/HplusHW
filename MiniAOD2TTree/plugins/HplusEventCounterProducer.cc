// -*- C++ -*-
// Description: An event counter that stores the sum of positive and negative events counts into the lumi block
// Modified from CommonTools/​UtilAlgos/​plugins/​EventCountProducer.cc

#include <memory>
#include <vector>
#include <algorithm>
#include <iostream>

// user include files
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

class HplusEventCountProducer : public edm::one::EDProducer<edm::one::WatchLuminosityBlocks,
                                                       edm::EndLuminosityBlockProducer> {
public:
  explicit HplusEventCountProducer(const edm::ParameterSet&);
  ~HplusEventCountProducer();

private:
  virtual void produce(edm::Event &, const edm::EventSetup&) override;
  virtual void beginLuminosityBlock(const edm::LuminosityBlock &, const edm::EventSetup&) override;
  virtual void endLuminosityBlock(edm::LuminosityBlock const&, const edm::EventSetup&) override;
  virtual void endLuminosityBlockProduce(edm::LuminosityBlock &, const edm::EventSetup&) override;
      
  // ----------member data ---------------------------
  edm::EDGetTokenT<GenEventInfoProduct> eventInfoToken;
  
  int positiveEventsProcessedInLumi_;
  int negativeEventsProcessedInLumi_;
};

using namespace edm;
using namespace std;

HplusEventCountProducer::HplusEventCountProducer(const edm::ParameterSet& iConfig):
  eventInfoToken(consumes<GenEventInfoProduct>(edm::InputTag("generator"))) {
  produces<edm::MergeableCounter, edm::InLumi>();
}

HplusEventCountProducer::~HplusEventCountProducer(){}

void HplusEventCountProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup){
  if (iEvent.isRealData()) {
    ++positiveEventsProcessedInLumi_;
    return;
  }
  // For MC, read gen weight
  edm::Handle<GenEventInfoProduct> handle;
  iEvent.getByToken(eventInfoToken, handle);
  if (handle.isValid()) {
    if (handle->weight() < 0.0) {
      ++negativeEventsProcessedInLumi_;
    } else {
      ++positiveEventsProcessedInLumi_;
    }
  } else {
    ++positiveEventsProcessedInLumi_;
  }
}

void HplusEventCountProducer::beginLuminosityBlock(const LuminosityBlock & theLuminosityBlock, const EventSetup & theSetup) {
  positiveEventsProcessedInLumi_ = 0;
  negativeEventsProcessedInLumi_ = 0;
}

void HplusEventCountProducer::endLuminosityBlock(LuminosityBlock const& theLuminosityBlock, const EventSetup & theSetup) {
}

void HplusEventCountProducer::endLuminosityBlockProduce(LuminosityBlock & theLuminosityBlock, const EventSetup & theSetup) {
  LogTrace("EventCounting") << "endLumi: adding +" << positiveEventsProcessedInLumi_
                            << " -" << negativeEventsProcessedInLumi_ << " events" << endl;

  auto_ptr<edm::MergeableCounter> numEventsPtr(new edm::MergeableCounter);
  numEventsPtr->value = positiveEventsProcessedInLumi_ - negativeEventsProcessedInLumi_;
  theLuminosityBlock.put(numEventsPtr);
}

//define this as a plug-in
DEFINE_FWK_MODULE(HplusHplusEventCountProducer);