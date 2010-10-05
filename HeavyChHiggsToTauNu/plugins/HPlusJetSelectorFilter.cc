#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
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
  HPlus::JetSelection fJetSelection;
  edm::InputTag fTauSrc;

  // Let's use reco::Candidate as the output type, as the required
  // dictionaries for edm::PtrVector<pat:Jet> do not exist, and I
  // don't want to use edm::Ref (as edm::Ptr is supposed to be better
  // in all ways) and I don't want to create the dictionaries myself. 
  typedef edm::PtrVector<reco::Candidate> Product;
};

HPlusJetPtrSelectorFilter::HPlusJetPtrSelectorFilter(const edm::ParameterSet& iConfig):
  eventCounter(),
  fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter),
  fTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc"))
{
  eventCounter.produces(this);
  produces<Product>();
}
HPlusJetPtrSelectorFilter::~HPlusJetPtrSelectorFilter() {}
void HPlusJetPtrSelectorFilter::beginJob() {}

bool HPlusJetPtrSelectorFilter::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusJetPtrSelectorFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > hcand;
  iEvent.getByLabel(fTauSrc, hcand);

  if(!fJetSelection.analyze(iEvent, iSetup, hcand->ptrVector())) return false;

  iEvent.put(std::auto_ptr<Product>(new Product(fJetSelection.getSelectedJets())));
  return true;
}

bool HPlusJetPtrSelectorFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return false;
}

void HPlusJetPtrSelectorFilter::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusJetPtrSelectorFilter);
