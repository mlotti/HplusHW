#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"

class HPlusGlobalElectronVetoFilter: public edm::EDFilter {
 public:

  explicit HPlusGlobalElectronVetoFilter(const edm::ParameterSet&);
  ~HPlusGlobalElectronVetoFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::HistoWrapper histoWrapper;
  HPlus::GlobalElectronVeto fGlobalElectronVeto;
  bool fFilter;
};

HPlusGlobalElectronVetoFilter::HPlusGlobalElectronVetoFilter(const edm::ParameterSet& iConfig):
  eventCounter(iConfig),
  eventWeight(iConfig),
  histoWrapper(eventWeight, "Debug"),
  fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, histoWrapper),
  fFilter(iConfig.getParameter<bool>("filter"))
{
  produces<bool>();
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusGlobalElectronVetoFilter::~HPlusGlobalElectronVetoFilter() {}
void HPlusGlobalElectronVetoFilter::beginJob() {}

bool HPlusGlobalElectronVetoFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusGlobalElectronVetoFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  HPlus::GlobalElectronVeto::Data electronVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
  bool passed = electronVetoData.passedEvent();
  std::auto_ptr<bool> p(new bool(passed));
  iEvent.put(p);

  return !fFilter || (fFilter && passed);
}

void HPlusGlobalElectronVetoFilter::endJob() {
  eventCounter.endJob();
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusGlobalElectronVetoFilter);
