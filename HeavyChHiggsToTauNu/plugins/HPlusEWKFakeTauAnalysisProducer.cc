#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EWKFakeTauAnalysis.h"

class HPlusEWKFakeTauAnalysisProducer: public edm::EDProducer {
 public:

  explicit HPlusEWKFakeTauAnalysisProducer(const edm::ParameterSet&);
  ~HPlusEWKFakeTauAnalysisProducer();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual void beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual void endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::EWKFakeTauAnalysis analysis;
};

HPlusEWKFakeTauAnalysisProducer::HPlusEWKFakeTauAnalysisProducer(const edm::ParameterSet& pset):
  eventCounter(), eventWeight(pset), analysis(pset, eventCounter, eventWeight)
{
  eventCounter.produces(this);
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusEWKFakeTauAnalysisProducer::~HPlusEWKFakeTauAnalysisProducer() {}
void HPlusEWKFakeTauAnalysisProducer::beginJob() {}

void HPlusEWKFakeTauAnalysisProducer::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
}

void HPlusEWKFakeTauAnalysisProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  analysis.produce(iEvent, iSetup);
}

void HPlusEWKFakeTauAnalysisProducer::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
}

void HPlusEWKFakeTauAnalysisProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusEWKFakeTauAnalysisProducer);
