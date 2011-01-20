#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurementFromAntiTauControlRegion.h"

class HPlusQCDMeasurementFromAntiTauControlRegionProducer: public edm::EDProducer {
 public:

  explicit HPlusQCDMeasurementFromAntiTauControlRegionProducer(const edm::ParameterSet&);
  ~HPlusQCDMeasurementFromAntiTauControlRegionProducer();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual void beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual void endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::QCDMeasurementFromAntiTauControlRegion analysis;
};

HPlusQCDMeasurementFromAntiTauControlRegionProducer::HPlusQCDMeasurementFromAntiTauControlRegionProducer(const edm::ParameterSet& pset):
  eventCounter(), eventWeight(pset), analysis(pset, eventCounter, eventWeight)
{
  eventCounter.produces(this);
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusQCDMeasurementFromAntiTauControlRegionProducer::~HPlusQCDMeasurementFromAntiTauControlRegionProducer() {}
void HPlusQCDMeasurementFromAntiTauControlRegionProducer::beginJob() {}

void HPlusQCDMeasurementFromAntiTauControlRegionProducer::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
}

void HPlusQCDMeasurementFromAntiTauControlRegionProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  analysis.produce(iEvent, iSetup);
}

void HPlusQCDMeasurementFromAntiTauControlRegionProducer::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
}

void HPlusQCDMeasurementFromAntiTauControlRegionProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusQCDMeasurementFromAntiTauControlRegionProducer);
