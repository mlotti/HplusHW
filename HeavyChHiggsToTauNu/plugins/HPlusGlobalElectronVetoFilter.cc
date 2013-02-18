#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/ElectronSelection.h"

class HPlusGlobalElectronVetoFilter: public edm::EDFilter {
 public:

  explicit HPlusGlobalElectronVetoFilter(const edm::ParameterSet&);
  ~HPlusGlobalElectronVetoFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  edm::InputTag fVertexSrc;
  HPlus::EventWeight eventWeight;
  HPlus::HistoWrapper histoWrapper;
  HPlus::EventCounter eventCounter;
  HPlus::ElectronSelection fElectronSelection;
  bool fFilter;
};

HPlusGlobalElectronVetoFilter::HPlusGlobalElectronVetoFilter(const edm::ParameterSet& iConfig):
  fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
  eventWeight(iConfig),
  histoWrapper(eventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  eventCounter(iConfig, eventWeight, histoWrapper),
  fElectronSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("ElectronSelection"), fVertexSrc, eventCounter, histoWrapper),
  fFilter(iConfig.getParameter<bool>("filter"))
{
  produces<bool>();
}
HPlusGlobalElectronVetoFilter::~HPlusGlobalElectronVetoFilter() {}
void HPlusGlobalElectronVetoFilter::beginJob() {}

bool HPlusGlobalElectronVetoFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusGlobalElectronVetoFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  HPlus::ElectronSelection::Data electronVetoData = fElectronSelection.analyze(iEvent, iSetup);
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
