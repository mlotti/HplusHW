#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalOptimisation.h"

class HPlusSignalOptimisationProducer: public edm::EDFilter {
 public:

  explicit HPlusSignalOptimisationProducer(const edm::ParameterSet&);
  ~HPlusSignalOptimisationProducer();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::SignalOptimisation analysis;
};

HPlusSignalOptimisationProducer::HPlusSignalOptimisationProducer(const edm::ParameterSet& pset):
  eventCounter(), eventWeight(pset), analysis(pset, eventCounter, eventWeight)
{
  eventCounter.produces(this);
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusSignalOptimisationProducer::~HPlusSignalOptimisationProducer() {}
void HPlusSignalOptimisationProducer::beginJob() {}

bool HPlusSignalOptimisationProducer::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusSignalOptimisationProducer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  return analysis.filter(iEvent, iSetup);
}

bool HPlusSignalOptimisationProducer::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return true;
}

void HPlusSignalOptimisationProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusSignalOptimisationProducer);
