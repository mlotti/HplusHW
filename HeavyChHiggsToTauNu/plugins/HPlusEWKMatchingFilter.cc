#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EWKMatching.h"

class HPlusEWKMatchingFilter: public edm::EDFilter {
 public:

  explicit HPlusEWKMatchingFilter(const edm::ParameterSet&);
  ~HPlusEWKMatchingFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::EWKMatching analysis;
};

HPlusEWKMatchingFilter::HPlusEWKMatchingFilter(const edm::ParameterSet& pset):
  eventCounter(pset), eventWeight(pset), analysis(pset, eventCounter, eventWeight)
{
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
  analysis.produces(this);
}
HPlusEWKMatchingFilter::~HPlusEWKMatchingFilter() {}
void HPlusEWKMatchingFilter::beginJob() {}

bool HPlusEWKMatchingFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusEWKMatchingFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  return analysis.filter(iEvent, iSetup);
}

void HPlusEWKMatchingFilter::endJob() {
  eventCounter.endJob();
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusEWKMatchingFilter);