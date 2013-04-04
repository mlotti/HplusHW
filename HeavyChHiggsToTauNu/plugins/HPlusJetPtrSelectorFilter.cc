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

#include<algorithm>
#include<iterator>

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
  HPlus::HistoWrapper histoWrapper;
  HPlus::EventCounter eventCounter;
  HPlus::JetSelection fJetSelection;
  edm::InputTag fTauSrc;
  bool fRemoveTau;
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
  histoWrapper(eventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  eventCounter(iConfig, eventWeight, histoWrapper),
  fJetSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("jetSelection"), eventCounter, histoWrapper),
  fTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
  fRemoveTau(iConfig.getParameter<bool>("removeTau")),
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
  HPlus::JetSelection::Data jetData;

  if(fRemoveTau) {
    edm::Handle<edm::View<reco::Candidate> > hcand;
    iEvent.getByLabel(fTauSrc, hcand);

    if (hcand->size() != 1) {
      if(fThrow || hcand->size() != 0)
        throw cms::Exception("LogicError") << "Tried to make jet selection with tau collection size " 
                                           << hcand->size() << " != 1!"
                                           << std::endl;
    }
    else {
      jetData = fJetSelection.analyze(iEvent, iSetup, hcand->ptrAt(0));
    }
  }
  else {
    jetData = fJetSelection.silentAnalyze(iEvent, iSetup);
  }
   
  bool passed = false;
  std::auto_ptr<Product> selectedJets(new Product());
  if(jetData.passedEvent()) {
    passed = true;
    for(size_t i=0; i<jetData.getSelectedJets().size(); ++i) {
      selectedJets->push_back(jetData.getSelectedJets()[i]);
    }
  }
  iEvent.put(selectedJets);

  std::auto_ptr<bool> p(new bool(passed));
  iEvent.put(p);

  return !fFilter || (fFilter && passed);
}

void HPlusJetPtrSelectorFilter::endJob() {
  eventCounter.endJob();
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusJetPtrSelectorFilter);
