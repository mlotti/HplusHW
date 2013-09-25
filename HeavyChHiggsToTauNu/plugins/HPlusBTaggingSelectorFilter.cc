#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BTagging.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/PtrVectorCast.h"

class HPlusBTaggingPtrSelectorFilter: public edm::EDFilter {
 public:

  explicit HPlusBTaggingPtrSelectorFilter(const edm::ParameterSet&);
  ~HPlusBTaggingPtrSelectorFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventWeight eventWeight;
  HPlus::HistoWrapper histoWrapper;
  HPlus::EventCounter eventCounter;
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
  eventWeight(iConfig),
  histoWrapper(eventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  eventCounter(iConfig, eventWeight, histoWrapper),
  fBTagging(iConfig.getUntrackedParameter<edm::ParameterSet>("btagging"), eventCounter, histoWrapper),
  fJetSrc(iConfig.getParameter<edm::InputTag>("jetSrc")),
  fFilter(iConfig.getParameter<bool>("filter")),
  fThrow(iConfig.getUntrackedParameter<bool>("throw"))
{
  produces<Product>();
  produces<edm::ValueMap<bool> >("tagged");
  produces<edm::ValueMap<float> >("scaleFactor");
  produces<edm::ValueMap<float> >("scaleFactorUncertainty");
  produces<bool>();
}
HPlusBTaggingPtrSelectorFilter::~HPlusBTaggingPtrSelectorFilter() {}
void HPlusBTaggingPtrSelectorFilter::beginJob() {}

bool HPlusBTaggingPtrSelectorFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusBTaggingPtrSelectorFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  bool passed = false;
  edm::Handle<edm::View<reco::Candidate> > hjets;
  if(iEvent.getByLabel(fJetSrc, hjets) || fThrow) {
    edm::PtrVector<pat::Jet> casted = HPlus::PtrVectorCast<pat::Jet>(hjets->ptrVector());

    HPlus::BTagging::Data btagData = fBTagging.analyze(iEvent, iSetup, casted);

    std::auto_ptr<Product> product(new Product(hjets->id()));
    if(btagData.passedEvent()) {
      passed = true;
      edm::PtrVector<pat::Jet> selected = btagData.getSelectedJets();
      for(size_t i=0; i<selected.size(); ++i) {
        product->push_back(selected[i]);
      }
    }
    iEvent.put(product);

    HPlus::BTagging::PerJetInfo jetInfos = fBTagging.getPerJetInfo(casted, btagData, iEvent.isRealData());
    std::auto_ptr<edm::ValueMap<bool> > tagged(new edm::ValueMap<bool>());
    std::auto_ptr<edm::ValueMap<float> > scaleFactor(new edm::ValueMap<float>());
    // Remark: The event scale factor is the product of the jet scale factor terms
    std::auto_ptr<edm::ValueMap<float> > scaleFactorUncertainty(new edm::ValueMap<float>());
    // Remark: The event SF uncertainty can be roughly estimated as the jet SF uncertainty terms added in quadrature
    {
      edm::ValueMap<bool>::Filler filler(*tagged);
      filler.insert(hjets, jetInfos.tagged.begin(), jetInfos.tagged.end());
      filler.fill();
    }
    {
      edm::ValueMap<float>::Filler filler(*scaleFactor);
      filler.insert(hjets, jetInfos.scaleFactor.begin(), jetInfos.scaleFactor.end());
      filler.fill();
    }
    {
      edm::ValueMap<float>::Filler filler(*scaleFactorUncertainty);
      filler.insert(hjets, jetInfos.uncertainty.begin(), jetInfos.uncertainty.end());
      filler.fill();
    }

    iEvent.put(tagged, "tagged");
    iEvent.put(scaleFactor, "scaleFactor");
    iEvent.put(scaleFactorUncertainty, "scaleFactorUncertainty");
  }
  std::auto_ptr<bool> p(new bool(passed));
  iEvent.put(p);

  return !fFilter || (fFilter && passed);
}

void HPlusBTaggingPtrSelectorFilter::endJob() {
  eventCounter.endJob();
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusBTaggingPtrSelectorFilter);
