#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
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

  virtual bool beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::VetoTauSelection fVetoTauSelection;
  edm::InputTag fTauSrc;
  bool fFilter;
  bool fThrow;

  // Let's use reco::Candidate as the output type, as the required
  // dictionaries for edm::PtrVector<pat:Tau> do not exist, and I
  // don't want to use edm::Ref (as edm::Ptr is supposed to be better
  // in all ways) and I don't want to create the dictionaries myself. 
  typedef edm::PtrVector<reco::Candidate> Product;
};

HPlusVetoTauPtrSelectorFilter::HPlusVetoTauPtrSelectorFilter(const edm::ParameterSet& iConfig):
  eventCounter(),
  eventWeight(iConfig),
  fVetoTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("vetoTauSelection"), eventCounter, eventWeight),
  fTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
  fFilter(iConfig.getParameter<bool>("filter"))
{
  eventCounter.produces(this);
  produces<Product>();
  produces<bool>();
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusVetoTauPtrSelectorFilter::~HPlusVetoTauPtrSelectorFilter() {}
void HPlusVetoTauPtrSelectorFilter::beginJob() {}

bool HPlusVetoTauPtrSelectorFilter::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusVetoTauPtrSelectorFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
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
    HPlus::VetoTauSelection::Data vetoTauData = fVetoTauSelection.analyze(iEvent, iSetup, hcand->ptrAt(0));
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

bool HPlusVetoTauPtrSelectorFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return false;
}

void HPlusVetoTauPtrSelectorFilter::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusVetoTauPtrSelectorFilter);
