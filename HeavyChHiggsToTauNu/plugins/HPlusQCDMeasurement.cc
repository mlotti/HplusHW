#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurement.h"

class HPlusQCDMeasurementProducer: public edm::EDProducer {
 public:

  explicit HPlusQCDMeasurementProducer(const edm::ParameterSet&);
  ~HPlusQCDMeasurementProducer();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual void beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual void endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::QCDMeasurement analysis;
};

HPlusQCDMeasurementProducer::HPlusQCDMeasurementProducer(const edm::ParameterSet& pset):
  eventCounter(), eventWeight(pset), analysis(pset, eventCounter, eventWeight)
{
  eventCounter.produces(this);
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusQCDMeasurementProducer::~HPlusQCDMeasurementProducer() {}
void HPlusQCDMeasurementProducer::beginJob() {}

void HPlusQCDMeasurementProducer::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
}

void HPlusQCDMeasurementProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  analysis.produce(iEvent, iSetup);
}

void HPlusQCDMeasurementProducer::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
}

void HPlusQCDMeasurementProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusQCDMeasurementProducer);
