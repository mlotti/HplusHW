#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TauSelection.h"

namespace {
  template <typename T1, typename T2>
  void pushBack(edm::PtrVector<T1>& container, const edm::Ptr<T2>& ptr) {
    container.push_back(ptr);
  }

  template <typename T>
  void pushBack(std::vector<T>& container, const edm::Ptr<T>& ptr) {
    container.push_back(*ptr);
  }
}


template <typename Product>
class HPlusTauSelectorFilterT: public edm::EDFilter {
 public:

  explicit HPlusTauSelectorFilterT(const edm::ParameterSet& iConfig):
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
  ~HPlusTauSelectorFilterT() {}

 private:
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    std::auto_ptr<Product> ret(new Product());
    HPlus::TauSelection::Data tauData = fOneProngTauSelection.analyze(iEvent, iSetup);
    bool passed = tauData.passedEvent();
    if(passed) {
      pushBack(*ret, tauData.getSelectedTau());
    }
    std::auto_ptr<bool> p(new bool(passed));

    iEvent.put(ret);
    iEvent.put(p);

    return !fFilter || (fFilter && passed);
  }

  virtual bool beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
    eventCounter.beginLuminosityBlock(iBlock, iSetup);
    return true;
  }
  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
    eventCounter.endLuminosityBlock(iBlock, iSetup);
    return true;
  }

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::TauSelection fOneProngTauSelection;
  bool fFilter;
};


// Let's use reco::Candidate as the output type, as the required
// dictionaries for edm::PtrVector<pat:Tau> do not exist, and I
// don't want to use edm::Ref (as edm::Ptr is supposed to be better
// in all ways) and I don't want to create the dictionaries myself. 
typedef HPlusTauSelectorFilterT< edm::PtrVector<reco::Candidate> > HPlusTauPtrSelectorFilter;
DEFINE_FWK_MODULE(HPlusTauPtrSelectorFilter);

typedef HPlusTauSelectorFilterT< std::vector<pat::Tau> > HPlusTauSelectorFilter;
DEFINE_FWK_MODULE(HPlusTauSelectorFilter);

