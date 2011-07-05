#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/JetSelection.h"

class HPlusJetPtrSelectorFilter: public edm::EDFilter {
 public:

  explicit HPlusJetPtrSelectorFilter(const edm::ParameterSet&);
  ~HPlusJetPtrSelectorFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::JetSelection fJetSelection;
  edm::InputTag fTauSrc;
  bool fFilter;

  // Let's use reco::Candidate as the output type, as the required
  // dictionaries for edm::PtrVector<pat:Jet> do not exist, and I
  // don't want to use edm::Ref (as edm::Ptr is supposed to be better
  // in all ways) and I don't want to create the dictionaries myself. 
  typedef edm::PtrVector<reco::Candidate> Product;
};

HPlusJetPtrSelectorFilter::HPlusJetPtrSelectorFilter(const edm::ParameterSet& iConfig):
  eventCounter(),
  eventWeight(iConfig),
  fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, eventWeight),
  fTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
  fFilter(iConfig.getParameter<bool>("filter"))
{
  eventCounter.produces(this);
  produces<Product>();
  produces<bool>();
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusJetPtrSelectorFilter::~HPlusJetPtrSelectorFilter() {}
void HPlusJetPtrSelectorFilter::beginJob() {}

bool HPlusJetPtrSelectorFilter::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusJetPtrSelectorFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  std::auto_ptr<bool> passed(new bool(false));

  edm::Handle<edm::View<reco::Candidate> > hcand;
  iEvent.getByLabel(fTauSrc, hcand);

  HPlus::JetSelection::Data jetData = fJetSelection.analyze(iEvent, iSetup, hcand->ptrVector());
  if(jetData.passedEvent()) {
    *passed = true;
    iEvent.put(std::auto_ptr<Product>(new Product(jetData.getSelectedJets())));
  }
  iEvent.put(passed);

  return !fFilter || (fFilter && *passed);
}

bool HPlusJetPtrSelectorFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return false;
}

void HPlusJetPtrSelectorFilter::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusJetPtrSelectorFilter);
