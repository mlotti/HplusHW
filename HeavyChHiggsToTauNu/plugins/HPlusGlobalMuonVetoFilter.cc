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
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/MuonSelection.h"

class HPlusGlobalMuonVetoFilter: public edm::EDFilter {
 public:

  explicit HPlusGlobalMuonVetoFilter(const edm::ParameterSet&);
  ~HPlusGlobalMuonVetoFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventWeight eventWeight;
  HPlus::HistoWrapper histoWrapper;
  HPlus::EventCounter eventCounter;
  HPlus::MuonSelection fMuonSelection;
  edm::InputTag fVertexSrc;
  bool fFilter;
};

HPlusGlobalMuonVetoFilter::HPlusGlobalMuonVetoFilter(const edm::ParameterSet& iConfig):
  eventWeight(iConfig),
  histoWrapper(eventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  eventCounter(iConfig, eventWeight, histoWrapper),
  fMuonSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MuonSelection"), eventCounter, histoWrapper),
  fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
  fFilter(iConfig.getParameter<bool>("filter"))
{
  produces<bool>();
}
HPlusGlobalMuonVetoFilter::~HPlusGlobalMuonVetoFilter() {}
void HPlusGlobalMuonVetoFilter::beginJob() {}

bool HPlusGlobalMuonVetoFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusGlobalMuonVetoFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Vertex> > hvert;
  iEvent.getByLabel(fVertexSrc, hvert);

  if(hvert->empty())
    throw cms::Exception("LogicError") << "Vertex collection " << fVertexSrc.encode() << " is empty!" << std::endl;

  // Global muon veto
  HPlus::MuonSelection::Data muonVetoData = fMuonSelection.analyze(iEvent, iSetup, hvert->ptrAt(0));
  bool passed = muonVetoData.passedEvent();
  std::auto_ptr<bool> p(new bool(passed));
  iEvent.put(p);

  return !fFilter || (fFilter && passed);
}

void HPlusGlobalMuonVetoFilter::endJob() {
  eventCounter.endJob();
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusGlobalMuonVetoFilter);
