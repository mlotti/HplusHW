#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/OrphanHandle.h"

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
  bool fAllowEmptyTau;
  bool fFilter;
  bool fThrow;
  bool fProducePt20;

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
  fAllowEmptyTau(iConfig.getParameter<bool>("allowEmptyTau")),
  fFilter(iConfig.getParameter<bool>("filter")),
  fThrow(iConfig.getParameter<bool>("throw")),
  fProducePt20(iConfig.getParameter<bool>("producePt20"))
{
  if(fProducePt20) {
    produces<Product>("selectedJets");
    produces<Product>("selectedJetsPt20");
  }
  else {
    produces<Product>();
  }
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

    if(fAllowEmptyTau && hcand->size() == 0) {
      jetData = fJetSelection.silentAnalyze(iEvent, iSetup);
    }
    else if (hcand->size() != 1) {
      if(fThrow)
        throw cms::Exception("LogicError") << "Tried to make jet selection with tau collection size " 
                                           << hcand->size() << " != 1!"
                                           << std::endl;
    }
    else {
      jetData = fJetSelection.silentAnalyze(iEvent, iSetup, hcand->ptrAt(0));
    }
  }
  else {
    jetData = fJetSelection.silentAnalyze(iEvent, iSetup);
  }
   
  bool passed = false;
  std::auto_ptr<Product> selectedJets(new Product());
  std::auto_ptr<Product> selectedJetsPt20(new Product());
  if(jetData.passedEvent()) {
    passed = true;
    for(size_t i=0; i<jetData.getSelectedJets().size(); ++i) {
      selectedJets->push_back(jetData.getSelectedJets()[i]);
    }
    for(size_t i=0; i<jetData.getSelectedJetsPt20().size(); ++i) {
      selectedJetsPt20->push_back(jetData.getSelectedJetsPt20()[i]);
    }
  }
  if(fProducePt20) {
    edm::OrphanHandle<Product> h1 = iEvent.put(selectedJetsPt20, "selectedJetsPt20");
    edm::OrphanHandle<Product> h2 = iEvent.put(selectedJets, "selectedJets");
    //std::cout << "selectedJetsPt20 id " << h1.id() << " selectedJets id " << h2.id() << std::endl;
  }
  else {
    iEvent.put(selectedJets);
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
