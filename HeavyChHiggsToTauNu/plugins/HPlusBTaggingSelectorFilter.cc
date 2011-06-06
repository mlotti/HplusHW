#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"

class HPlusBTaggingPtrSelectorFilter: public edm::EDFilter {
 public:

  explicit HPlusBTaggingPtrSelectorFilter(const edm::ParameterSet&);
  ~HPlusBTaggingPtrSelectorFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::BTagging fBTagging;
  edm::InputTag fJetSrc;
  bool fFilter;
  bool fThrow;

  // Let's use reco::Candidate as the output type, as the required
  // dictionaries for edm::PtrVector<pat:Jet> do not exist, and I
  // don't want to use edm::Ref (as edm::Ptr is supposed to be better
  // in all ways) and I don't want to create the dictionaries myself. 
  typedef edm::PtrVector<reco::Candidate> Product;
};

HPlusBTaggingPtrSelectorFilter::HPlusBTaggingPtrSelectorFilter(const edm::ParameterSet& iConfig):
  eventCounter(),
  eventWeight(iConfig),
  fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("btagging"), eventCounter, eventWeight),
  fJetSrc(iConfig.getParameter<edm::InputTag>("jetSrc")),
  fFilter(iConfig.getParameter<bool>("filter")),
  fThrow(iConfig.getUntrackedParameter<bool>("throw"))
{
  eventCounter.produces(this);
  produces<Product>();
  produces<bool>();
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusBTaggingPtrSelectorFilter::~HPlusBTaggingPtrSelectorFilter() {}
void HPlusBTaggingPtrSelectorFilter::beginJob() {}

bool HPlusBTaggingPtrSelectorFilter::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusBTaggingPtrSelectorFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  std::auto_ptr<bool> passed(new bool(false));

  edm::Handle<edm::View<reco::Candidate> > hjets;
  if(iEvent.getByLabel(fJetSrc, hjets) || fThrow) {
    edm::PtrVector<pat::Jet> casted(hjets->id());
    for(size_t i=0; i<hjets->size(); ++i) {
      edm::Ptr<reco::Candidate> ptr = hjets->ptrAt(i);
      casted.push_back(edm::Ptr<pat::Jet>(ptr.id(), dynamic_cast<const pat::Jet *>(ptr.get()), ptr.key()));
    }
  
    HPlus::BTagging::Data btagData = fBTagging.analyze(casted);
    if(btagData.passedEvent()) {
      std::auto_ptr<Product> product(new Product(hjets->id()));
      edm::PtrVector<pat::Jet> selected = btagData.getSelectedJets();
      for(size_t i=0; i<selected.size(); ++i) {
        product->push_back(selected[i]);
      }
      iEvent.put(product);
    }
  }
  iEvent.put(passed);
  return !fFilter || (fFilter && *passed);
}

bool HPlusBTaggingPtrSelectorFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return false;
}

void HPlusBTaggingPtrSelectorFilter::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusBTaggingPtrSelectorFilter);
