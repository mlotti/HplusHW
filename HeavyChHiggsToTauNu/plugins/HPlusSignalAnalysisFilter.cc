#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/SignalAnalysis.h"

class HPlusSignalAnalysisFilter: public edm::EDFilter {
 public:

  explicit HPlusSignalAnalysisFilter(const edm::ParameterSet&);
  ~HPlusSignalAnalysisFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::SignalAnalysis analysis;
};

HPlusSignalAnalysisFilter::HPlusSignalAnalysisFilter(const edm::ParameterSet& pset):
  eventCounter(), eventWeight(pset), analysis(pset, eventCounter, eventWeight)
{
  eventCounter.produces(this);
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
  analysis.produces(this);
}
HPlusSignalAnalysisFilter::~HPlusSignalAnalysisFilter() {}
void HPlusSignalAnalysisFilter::beginJob() {}

bool HPlusSignalAnalysisFilter::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusSignalAnalysisFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  return analysis.filter(iEvent, iSetup);
}

bool HPlusSignalAnalysisFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return true;
}

void HPlusSignalAnalysisFilter::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusSignalAnalysisFilter);
