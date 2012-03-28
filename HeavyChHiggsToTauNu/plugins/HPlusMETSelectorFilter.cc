#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"

class HPlusMETPtrSelectorFilter: public edm::EDFilter {
 public:

  explicit HPlusMETPtrSelectorFilter(const edm::ParameterSet&);
  ~HPlusMETPtrSelectorFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventCounter eventCounter;
  HPlus::EventWeight eventWeight;
  HPlus::METSelection fMETSelection;
  edm::InputTag fTauSrc;
  edm::InputTag fJetSrc;
};

HPlusMETPtrSelectorFilter::HPlusMETPtrSelectorFilter(const edm::ParameterSet& iConfig):
  eventCounter(),
  eventWeight(iConfig),
  fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, eventWeight, "MET"),
  fTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
  fJetSrc(iConfig.getUntrackedParameter<edm::InputTag>("jetSrc"))
{
  eventCounter.produces(this);
  eventCounter.setWeightPointer(eventWeight.getWeightPtr());
}
HPlusMETPtrSelectorFilter::~HPlusMETPtrSelectorFilter() {}
void HPlusMETPtrSelectorFilter::beginJob() {}

bool HPlusMETPtrSelectorFilter::beginLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.beginLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusMETPtrSelectorFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<pat::Tau> > htaus;
  iEvent.getByLabel(fTauSrc, htaus);
  if(htaus->size() == 0)
    throw cms::Exception("Assert") << "At least one tau required, got 0" << std::endl;

  edm::Handle<edm::View<pat::Jet> > hjets;
  iEvent.getByLabel(fJetSrc, hjets);

  HPlus::METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, htaus->ptrAt(0), hjets->ptrVector());
  if(!metData.passedEvent()) return false;
  return true;
}

bool HPlusMETPtrSelectorFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup& iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return false;
}

void HPlusMETPtrSelectorFilter::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusMETPtrSelectorFilter);
