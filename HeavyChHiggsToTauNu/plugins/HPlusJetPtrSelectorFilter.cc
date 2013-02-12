#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"

class HPlusJetPtrSelectorFilter: public edm::EDFilter {
 public:

  explicit HPlusJetPtrSelectorFilter(const edm::ParameterSet&);
  ~HPlusJetPtrSelectorFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventWeight eventWeight;
  HPlus::EventCounter eventCounter;
  HPlus::HistoWrapper histoWrapper;
  HPlus::JetSelection fJetSelection;
  edm::InputTag fTauSrc;
  bool fFilter;
  bool fThrow;

  // Let's use reco::Candidate as the output type, as the required
  // dictionaries for edm::PtrVector<pat:Jet> do not exist, and I
  // don't want to use edm::Ref (as edm::Ptr is supposed to be better
  // in all ways) and I don't want to create the dictionaries myself. 
  typedef edm::PtrVector<reco::Candidate> Product;
};

HPlusJetPtrSelectorFilter::HPlusJetPtrSelectorFilter(const edm::ParameterSet& iConfig):
  eventWeight(iConfig),
  eventCounter(iConfig, eventWeight),
  histoWrapper(eventWeight, "Debug"),
  fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, histoWrapper),
  fTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
  fFilter(iConfig.getParameter<bool>("filter")),
  fThrow(iConfig.getParameter<bool>("throw"))
{
  produces<Product>();
  produces<bool>();
}
HPlusJetPtrSelectorFilter::~HPlusJetPtrSelectorFilter() {}
void HPlusJetPtrSelectorFilter::beginJob() {}

bool HPlusJetPtrSelectorFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusJetPtrSelectorFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > hcand;
  iEvent.getByLabel(fTauSrc, hcand);

  bool passed = false;
  if (hcand->size() != 1) {
    if(fThrow || hcand->size() != 0)
      throw cms::Exception("LogicError") << "Tried to make jet selection with tau collection size " 
                                         << hcand->size() << " != 1!"
                                         << std::endl;
  }
  else {
    HPlus::JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, hcand->ptrAt(0));
    if(jetData.passedEvent()) {
      passed = true;
      iEvent.put(std::auto_ptr<Product>(new Product(jetData.getSelectedJets())));
    }
  }
  std::auto_ptr<bool> p(new bool(passed));
  iEvent.put(p);

  return !fFilter || (fFilter && passed);
}

void HPlusJetPtrSelectorFilter::endJob() {
  eventCounter.endJob();
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusJetPtrSelectorFilter);
