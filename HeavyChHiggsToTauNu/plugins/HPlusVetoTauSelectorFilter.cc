#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VetoTauSelection.h"

class HPlusVetoTauPtrSelectorFilter: public edm::EDFilter {
 public:

  explicit HPlusVetoTauPtrSelectorFilter(const edm::ParameterSet&);
  ~HPlusVetoTauPtrSelectorFilter();
    void vetoTauData();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventWeight eventWeight;
  HPlus::HistoWrapper histoWrapper;
  HPlus::EventCounter eventCounter;
  HPlus::VetoTauSelection fVetoTauSelection;
  edm::InputTag fTauSrc;
  bool fFilter;
  edm::InputTag fVertexSrc;
  bool fThrow;

  // Let's use reco::Candidate as the output type, as the required
  // dictionaries for edm::PtrVector<pat:Tau> do not exist, and I
  // don't want to use edm::Ref (as edm::Ptr is supposed to be better
  // in all ways) and I don't want to create the dictionaries myself. 
  typedef edm::PtrVector<reco::Candidate> Product;
};

HPlusVetoTauPtrSelectorFilter::HPlusVetoTauPtrSelectorFilter(const edm::ParameterSet& iConfig):
  eventWeight(iConfig),
  histoWrapper(eventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  eventCounter(iConfig, eventWeight, histoWrapper),
  fVetoTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("vetoTauSelection"),
                    iConfig.getUntrackedParameter<edm::ParameterSet>("fakeTauSFandSystematics"),
                    eventCounter, histoWrapper),
  fTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
  fFilter(iConfig.getParameter<bool>("filter")),
  fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc"))
{
  produces<Product>();
  produces<bool>();
}
HPlusVetoTauPtrSelectorFilter::~HPlusVetoTauPtrSelectorFilter() {}
void HPlusVetoTauPtrSelectorFilter::beginJob() {}

bool HPlusVetoTauPtrSelectorFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusVetoTauPtrSelectorFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Vertex> > hvert;
  iEvent.getByLabel(fVertexSrc, hvert);
  if(hvert->empty())
    throw cms::Exception("LogicError") << "Vertex collection " << fVertexSrc.encode() << " is empty!" << std::endl;

  // Obtain selected tau in event
  edm::Handle<edm::View<reco::Candidate> > hcand;
  iEvent.getByLabel(fTauSrc, hcand);

  bool passed = false;
  if (hcand->size() != 1) {
    if (fThrow || hcand->size() != 0)
      throw cms::Exception("LogicError") << "Tried to make jet selection with tau collection size " 
                                         << hcand->size() << " != 1!"
                                         << std::endl;
  } else {
    // Do veto tau selection
    std::auto_ptr<Product> ret(new Product());
    HPlus::VetoTauSelection::Data vetoTauData = fVetoTauSelection.analyze(iEvent, iSetup, hcand->ptrAt(0), hvert->ptrAt(0)->z());
    passed = vetoTauData.passedEvent();
    if (passed) {
      ret->push_back(vetoTauData.getSelectedVetoTaus()[0]);
      iEvent.put(ret);
    }
  }
  std::auto_ptr<bool> p(new bool(passed));

  iEvent.put(p);

  return !fFilter || (fFilter && passed);
}

void HPlusVetoTauPtrSelectorFilter::endJob() {
  eventCounter.endJob();
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusVetoTauPtrSelectorFilter);
