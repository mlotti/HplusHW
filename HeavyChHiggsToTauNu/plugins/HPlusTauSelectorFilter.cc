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
  HPlus::TauSelection fTauSelection;

  // Let's use reco::Candidate as the output type, as the required
  // dictionaries for edm::PtrVector<pat:Tau> do not exist, and I
  // don't want to use edm::Ref (as edm::Ptr is supposed to be better
  // in all ways) and I don't want to create the dictionaries myself. 
  typedef edm::PtrVector<reco::Candidate> Product;
};

HPlusTauPtrSelectorFilter::HPlusTauPtrSelectorFilter(const edm::ParameterSet& iConfig):
  eventCounter(),
  eventWeight(iConfig),
  fTauSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("tauSelection"), eventCounter, eventWeight)
{
  eventCounter.produces(this);
  produces<Product>();
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusTauPtrSelectorFilter::~HPlusTauPtrSelectorFilter() {}
void HPlusTauPtrSelectorFilter::beginJob() {}

bool HPlusTauPtrSelectorFilter::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusTauPtrSelectorFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  HPlus::TauSelection::Data tauData = fTauSelection.analyze(iEvent, iSetup);
  if(!tauData.passedEvent()) return false;

  //iEvent.put(std::auto_ptr<Product>(new Product(fTauSelection.getSelectedTaus())));
  std::auto_ptr<Product> ret(new Product());
  ret->push_back(tauData.getSelectedTaus()[0]);
  iEvent.put(ret);
  return true;
}

bool HPlusTauPtrSelectorFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return false;
}

void HPlusTauPtrSelectorFilter::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTauPtrSelectorFilter);
