#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/QCDMeasurementBasic.h"

class HPlusQCDMeasurementBasicFilter : public edm::EDFilter {
 public:

  explicit HPlusQCDMeasurementBasicFilter(const edm::ParameterSet&);
  ~HPlusQCDMeasurementBasicFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::QCDMeasurementBasic analysis;
};

HPlusQCDMeasurementBasicFilter::HPlusQCDMeasurementBasicFilter(const edm::ParameterSet& pset):
  eventCounter(), eventWeight(pset), analysis(pset, eventCounter, eventWeight)
{
  eventCounter.produces(this);
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusQCDMeasurementBasicFilter::~HPlusQCDMeasurementBasicFilter() {}
void HPlusQCDMeasurementBasicFilter::beginJob() {}

bool HPlusQCDMeasurementBasicFilter::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusQCDMeasurementBasicFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  return analysis.filter(iEvent, iSetup);
}

bool HPlusQCDMeasurementBasicFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return true;
}

void HPlusQCDMeasurementBasicFilter::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusQCDMeasurementBasicFilter);
