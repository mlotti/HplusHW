#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurementByMetFactorisationPart2.h"

class HPlusQCDMeasurementByMetFactorisationPart2Producer: public edm::EDProducer {
 public:

  explicit HPlusQCDMeasurementByMetFactorisationPart2Producer(const edm::ParameterSet&);
  ~HPlusQCDMeasurementByMetFactorisationPart2Producer();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual void beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual void endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::QCDMeasurementByMetFactorisationPart2 analysis;
};

HPlusQCDMeasurementByMetFactorisationPart2Producer::HPlusQCDMeasurementByMetFactorisationPart2Producer(const edm::ParameterSet& pset):
  eventCounter(), eventWeight(pset), analysis(pset, eventCounter, eventWeight)
{
  eventCounter.produces(this);
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusQCDMeasurementByMetFactorisationPart2Producer::~HPlusQCDMeasurementByMetFactorisationPart2Producer() {}
void HPlusQCDMeasurementByMetFactorisationPart2Producer::beginJob() {}

void HPlusQCDMeasurementByMetFactorisationPart2Producer::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
}

void HPlusQCDMeasurementByMetFactorisationPart2Producer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  analysis.produce(iEvent, iSetup);
}

void HPlusQCDMeasurementByMetFactorisationPart2Producer::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
}

void HPlusQCDMeasurementByMetFactorisationPart2Producer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusQCDMeasurementByMetFactorisationPart2Producer);
