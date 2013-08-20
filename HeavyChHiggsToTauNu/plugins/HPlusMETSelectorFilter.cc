#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/HistoWrapper.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/METSelection.h"

class HPlusMETPtrSelectorFilter: public edm::EDFilter {
 public:

  explicit HPlusMETPtrSelectorFilter(const edm::ParameterSet&);
  ~HPlusMETPtrSelectorFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);

  HPlus::EventWeight eventWeight;
  HPlus::HistoWrapper histoWrapper;
  HPlus::EventCounter eventCounter;
  HPlus::METSelection fMETSelection;
  edm::InputTag fVertexSrc;
  edm::InputTag fTauSrc;
  edm::InputTag fJetSrc;
};

HPlusMETPtrSelectorFilter::HPlusMETPtrSelectorFilter(const edm::ParameterSet& iConfig):
  eventWeight(iConfig),
  histoWrapper(eventWeight, iConfig.getUntrackedParameter<std::string>("histogramAmbientLevel")),
  eventCounter(iConfig, eventWeight, histoWrapper),
  fMETSelection(iConfig.getUntrackedParameter<edm::ParameterSet>("MET"), eventCounter, histoWrapper, "MET", iConfig.getUntrackedParameter<std::string>("tauIsolationDiscriminator")),
  fVertexSrc(iConfig.getParameter<edm::InputTag>("vertexSrc")),
  fTauSrc(iConfig.getUntrackedParameter<edm::InputTag>("tauSrc")),
  fJetSrc(iConfig.getUntrackedParameter<edm::InputTag>("jetSrc"))
{
}
HPlusMETPtrSelectorFilter::~HPlusMETPtrSelectorFilter() {}
void HPlusMETPtrSelectorFilter::beginJob() {}

bool HPlusMETPtrSelectorFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  eventCounter.endLuminosityBlock(iBlock, iSetup);
  return true;
}

bool HPlusMETPtrSelectorFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Vertex> > hvert;
  iEvent.getByLabel(fVertexSrc, hvert);
  if(hvert->empty())
    throw cms::Exception("LogicError") << "Vertex collection " << fVertexSrc.encode() << " is empty!" << std::endl;

  edm::Handle<edm::View<pat::Tau> > htaus;
  iEvent.getByLabel(fTauSrc, htaus);
  if(htaus->size() == 0)
    throw cms::Exception("Assert") << "At least one tau required, got 0" << std::endl;

  edm::Handle<edm::View<pat::Jet> > hjets;
  iEvent.getByLabel(fJetSrc, hjets);

  HPlus::METSelection::Data metData = fMETSelection.analyze(iEvent, iSetup, static_cast<int>(hvert->ptrVector().size()), htaus->ptrAt(0), hjets->ptrVector());
  if(!metData.passedEvent()) return false;
  return true;
}

void HPlusMETPtrSelectorFilter::endJob() {
  eventCounter.endJob();
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusMETPtrSelectorFilter);
