#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurementMETfit.h"

class HPlusQCDMeasurementMETfitProducer: public edm::EDProducer {
 public:

  explicit HPlusQCDMeasurementMETfitProducer(const edm::ParameterSet&);
  ~HPlusQCDMeasurementMETfitProducer();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual void beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual void endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::QCDMeasurementMETfit analysis;
};

HPlusQCDMeasurementMETfitProducer::HPlusQCDMeasurementMETfitProducer(const edm::ParameterSet& pset):
  eventCounter(), eventWeight(pset), analysis(pset, eventCounter, eventWeight)
{
  eventCounter.produces(this);
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusQCDMeasurementMETfitProducer::~HPlusQCDMeasurementMETfitProducer() {}
void HPlusQCDMeasurementMETfitProducer::beginJob() {}

void HPlusQCDMeasurementMETfitProducer::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
}

void HPlusQCDMeasurementMETfitProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  analysis.produce(iEvent, iSetup);
}

void HPlusQCDMeasurementMETfitProducer::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
}

void HPlusQCDMeasurementMETfitProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusQCDMeasurementMETfitProducer);
