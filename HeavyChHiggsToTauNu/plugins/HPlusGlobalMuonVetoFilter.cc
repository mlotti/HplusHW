#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GlobalMuonVeto.h"

class HPlusGlobalMuonVetoFilter: public edm::EDFilter {
 public:

  explicit HPlusGlobalMuonVetoFilter(const edm::ParameterSet&);
  ~HPlusGlobalMuonVetoFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::GlobalMuonVeto fGlobalMuonVeto;
  edm::InputTag fVertexSrc;
  bool fFilter;
};

HPlusGlobalMuonVetoFilter::HPlusGlobalMuonVetoFilter(const edm::ParameterSet& iConfig):
  eventCounter(),
  eventWeight(iConfig),
  fGlobalMuonVeto(iConfig.getUntrackedParameter<edm::ParameterSet>("GlobalMuonVeto"), eventCounter, eventWeight),
  fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
  fFilter(iConfig.getParameter<bool>("filter"))
{
  eventCounter.produces(this);
  produces<bool>();
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusGlobalMuonVetoFilter::~HPlusGlobalMuonVetoFilter() {}
void HPlusGlobalMuonVetoFilter::beginJob() {}

bool HPlusGlobalMuonVetoFilter::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusGlobalMuonVetoFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Vertex> > hvert;
  iEvent.getByLabel(fVertexSrc, hvert);

  if(hvert->empty())
    throw cms::Exception("LogicError") << "Vertex collection " << fVertexSrc.encode() << " is empty!" << std::endl;

  // Global muon veto
  HPlus::GlobalMuonVeto::Data muonVetoData = fGlobalMuonVeto.analyze(iEvent, iSetup, hvert->ptrAt(0));
  bool passed = muonVetoData.passedEvent();
  std::auto_ptr<bool> p(new bool(passed));
  iEvent.put(p);

  return !fFilter || (fFilter && passed);
}

bool HPlusGlobalMuonVetoFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return false;
}

void HPlusGlobalMuonVetoFilter::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusGlobalMuonVetoFilter);
