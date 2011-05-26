#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/AlphatAnalysis.h"

class HPlusAlphatAnalysisProducer: public edm::EDFilter {
 public:

  explicit HPlusAlphatAnalysisProducer(const edm::ParameterSet&);
  ~HPlusAlphatAnalysisProducer();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::AlphatAnalysis analysis;
};

HPlusAlphatAnalysisProducer::HPlusAlphatAnalysisProducer(const edm::ParameterSet& pset):
  eventCounter(), eventWeight(pset), analysis(pset, eventCounter, eventWeight)
{
  eventCounter.produces(this);
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusAlphatAnalysisProducer::~HPlusAlphatAnalysisProducer() {}
void HPlusAlphatAnalysisProducer::beginJob() {}

bool HPlusAlphatAnalysisProducer::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusAlphatAnalysisProducer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  return analysis.filter(iEvent, iSetup);
}

bool HPlusAlphatAnalysisProducer::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return true;
}

void HPlusAlphatAnalysisProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusAlphatAnalysisProducer);
