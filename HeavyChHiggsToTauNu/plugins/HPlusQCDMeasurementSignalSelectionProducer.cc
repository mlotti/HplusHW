#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurementSignalSelection.h"

class HPlusQCDMeasurementSignalSelectionProducer: public edm::EDProducer {
 public:

  explicit HPlusQCDMeasurementSignalSelectionProducer(const edm::ParameterSet&);
  ~HPlusQCDMeasurementSignalSelectionProducer();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual void beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual void endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::QCDMeasurementSignalSelection analysis;
};

HPlusQCDMeasurementSignalSelectionProducer::HPlusQCDMeasurementSignalSelectionProducer(const edm::ParameterSet& pset):
  eventCounter(), eventWeight(pset), analysis(pset, eventCounter, eventWeight)
{
  eventCounter.produces(this);
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusQCDMeasurementSignalSelectionProducer::~HPlusQCDMeasurementSignalSelectionProducer() {}
void HPlusQCDMeasurementSignalSelectionProducer::beginJob() {}

void HPlusQCDMeasurementSignalSelectionProducer::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
}

void HPlusQCDMeasurementSignalSelectionProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  analysis.produce(iEvent, iSetup);
}

void HPlusQCDMeasurementSignalSelectionProducer::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
}

void HPlusQCDMeasurementSignalSelectionProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusQCDMeasurementSignalSelectionProducer);
