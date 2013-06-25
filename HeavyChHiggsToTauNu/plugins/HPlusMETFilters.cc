#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METFilters.h"

class HPlusMETFilters: public edm::EDFilter {
 public:

  explicit HPlusMETFilters(const edm::ParameterSet&);
  ~HPlusMETFilters();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event&, const edm::EventSetup&);
  virtual void endJob();

  virtual bool endLuminosityBlock(edm::LuminosityBlock&, const edm::EventSetup&);

  HPlus::EventWeight eventWeight;
  HPlus::HistoWrapper histoWrapper;
  HPlus::EventCounter eventCounter;
  HPlus::METFilters fMETFilters;
  bool fFilter;
};

HPlusMETFilters::HPlusMETFilters(const edm::ParameterSet& iConfig):
  eventWeight(iConfig),
  histoWrapper(eventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  eventCounter(iConfig, eventWeight, histoWrapper),
  fMETFilters(iConfig.getUntrackedParameter<edm::ParameterSet>("metFilters"), eventCounter),
  fFilter(iConfig.getParameter<bool>("filter"))
{
  produces<bool>();
}
HPlusMETFilters::~HPlusMETFilters() {}
void HPlusMETFilters::beginJob() {}

bool HPlusMETFilters::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
    eventCounter.endLuminosityBlock(iBlock, iSetup);
    return true;
}

bool HPlusMETFilters::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {

//------ MET (noise) filters for data (reject events with instrumental fake MET)
  bool passed = true;
  if(iEvent.isRealData()) {
    passed = fMETFilters.passedEvent(iEvent, iSetup);
  }
  std::auto_ptr<bool> p(new bool(passed));
  iEvent.put(p);

  return !fFilter || (fFilter && passed);
}

void HPlusMETFilters::endJob() {
    eventCounter.endJob();
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusMETFilters);
