#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalElectronVeto.h"

class HPlusGlobalElectronVetoFilter: public edm::EDFilter {
 public:

  explicit HPlusGlobalElectronVetoFilter(const edm::ParameterSet&);
  ~HPlusGlobalElectronVetoFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::GlobalElectronVeto fGlobalElectronVeto;
  edm::InputTag fVertexSrc;
};

HPlusGlobalElectronVetoFilter::HPlusGlobalElectronVetoFilter(const edm::ParameterSet& iConfig):
  eventCounter(),
  eventWeight(iConfig),
  fGlobalElectronVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalElectronVeto"), eventCounter, eventWeight)
{
  eventCounter.produces(this);
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusGlobalElectronVetoFilter::~HPlusGlobalElectronVetoFilter() {}
void HPlusGlobalElectronVetoFilter::beginJob() {}

bool HPlusGlobalElectronVetoFilter::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusGlobalElectronVetoFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  HPlus::GlobalElectronVeto::Data muonVetoData = fGlobalElectronVeto.analyze(iEvent, iSetup);
  if (!muonVetoData.passedEvent()) return false;

  return true;
}

bool HPlusGlobalElectronVetoFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return false;
}

void HPlusGlobalElectronVetoFilter::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusGlobalElectronVetoFilter);
