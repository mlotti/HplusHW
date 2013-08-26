#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/MergeableCounter.h"
#include "DataFormats/Common/interface/Handle.h"


class HPlusEventCountProducer : public edm::EDProducer {
public:
  explicit HPlusEventCountProducer(const edm::ParameterSet&);
  ~HPlusEventCountProducer();

private:
  virtual void beginLuminosityBlock(edm::LuminosityBlock &, const edm::EventSetup &);
  virtual void produce(edm::Event &, const edm::EventSetup &);
  virtual void endLuminosityBlock(edm::LuminosityBlock &, const edm::EventSetup &);
      
  // ----------member data ---------------------------

  edm::InputTag weightSrc_;
  double eventsProcessedInLumiWeight_;
  double eventsProcessedInLumiWeightSquared_;
  unsigned int eventsProcessedInLumi_;
  bool hasWeight_;
};


HPlusEventCountProducer::HPlusEventCountProducer(const edm::ParameterSet& iConfig):
  weightSrc_(""),
  eventsProcessedInLumiWeight_(0),
  eventsProcessedInLumiWeightSquared_(0),
  eventsProcessedInLumi_(0),
  hasWeight_(false) {

  if(iConfig.exists("weightSrc")) {
    hasWeight_ = true;
    weightSrc_ = iConfig.getParameter<edm::InputTag>("weightSrc");
  }

  produces<edm::MergeableCounter, edm::InLumi>();
  produces<double, edm::InLumi>("Weights");
  produces<double, edm::InLumi>("WeightsSquared");
}
HPlusEventCountProducer::~HPlusEventCountProducer(){}

void HPlusEventCountProducer::beginLuminosityBlock(edm::LuminosityBlock& iLuminosityBlock, const edm::EventSetup& iSetup) {
  eventsProcessedInLumi_ = 0;
  eventsProcessedInLumiWeight_ = 0;
  eventsProcessedInLumiWeightSquared_ = 0;
}

void HPlusEventCountProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  double weight = 1.0;

  if(hasWeight_) {
    edm::Handle<double> hweight;
    iEvent.getByLabel(weightSrc_, hweight);
    weight = *hweight;
  }

  eventsProcessedInLumi_++;
  eventsProcessedInLumiWeight_ += weight;
  eventsProcessedInLumiWeightSquared_ += weight*weight;
}

void HPlusEventCountProducer::endLuminosityBlock(edm::LuminosityBlock &iLuminosityBlock, const edm::EventSetup& iSetup) {
  LogTrace("EventCounting") << "endLumi: adding " << eventsProcessedInLumi_ << " events" << std::endl;

  std::auto_ptr<edm::MergeableCounter> numEventsPtr(new edm::MergeableCounter);
  numEventsPtr->value = eventsProcessedInLumi_;
  iLuminosityBlock.put(numEventsPtr);

  if(hasWeight_) {
    std::auto_ptr<double> numEventsWeight(new double(eventsProcessedInLumiWeight_));
    iLuminosityBlock.put(numEventsWeight, "Weights");

    std::auto_ptr<double> numEventsWeightSquared(new double(eventsProcessedInLumiWeightSquared_));
    iLuminosityBlock.put(numEventsWeightSquared, "WeightsSquared");
  }
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusEventCountProducer);
