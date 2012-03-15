#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"

class HPlusTauPtrSelectorFilter: public edm::EDFilter {
 public:

  explicit HPlusTauPtrSelectorFilter(const edm::ParameterSet&);
  ~HPlusTauPtrSelectorFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::TauSelection fOneProngTauSelection;
  bool fFilter;

  // Let's use reco::Candidate as the output type, as the required
  // dictionaries for edm::PtrVector<pat:Tau> do not exist, and I
  // don't want to use edm::Ref (as edm::Ptr is supposed to be better
  // in all ways) and I don't want to create the dictionaries myself. 
  typedef edm::PtrVector<reco::Candidate> Product;
};

HPlusTauPtrSelectorFilter::HPlusTauPtrSelectorFilter(const edm::ParameterSet& iConfig):
  eventCounter(),
  eventWeight(iConfig),
  fOneProngTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight),
  fFilter(iConfig.getParameter<bool>("filter"))
{
  eventCounter.produces(this);
  produces<Product>();
  produces<bool>();
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusTauPtrSelectorFilter::~HPlusTauPtrSelectorFilter() {}
void HPlusTauPtrSelectorFilter::beginJob() {}

bool HPlusTauPtrSelectorFilter::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusTauPtrSelectorFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  std::auto_ptr<Product> ret(new Product());
  HPlus::TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);
  bool passed = tauData.passedEvent();
  if(passed)
    ret->push_back(tauData.getSelectedTaus()[0]);
  std::auto_ptr<bool> p(new bool(passed));

  iEvent.put(ret);
  iEvent.put(p);

  return !fFilter || (fFilter && passed);
}

bool HPlusTauPtrSelectorFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return false;
}

void HPlusTauPtrSelectorFilter::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTauPtrSelectorFilter);
