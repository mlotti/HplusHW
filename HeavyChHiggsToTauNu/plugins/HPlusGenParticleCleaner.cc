#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/Math/interface/deltaR.h"

#include<vector>


class HPlusGenParticleCleaner: public edm::EDProducer {
 public:

  explicit HPlusGenParticleCleaner(const edm::ParameterSet&);
  ~HPlusGenParticleCleaner();

 private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  edm::InputTag src;
  edm::InputTag candSrc;
  const double maxDeltaR;
};

HPlusGenParticleCleaner::HPlusGenParticleCleaner(const edm::ParameterSet& iConfig):
  src(iConfig.getParameter<edm::InputTag>("src")),
  candSrc(iConfig.getParameter<edm::InputTag>("candSrc")),
  maxDeltaR(iConfig.getParameter<double>("maxDeltaR"))
{
  produces<reco::GenParticleRefVector>();
}
HPlusGenParticleCleaner::~HPlusGenParticleCleaner() {}

void HPlusGenParticleCleaner::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  //edm::Handle<edm::View<reco::GenParticle> > hgen;
  edm::Handle<reco::GenParticleRefVector> hgen;
  iEvent.getByLabel(src, hgen);

  edm::Handle<edm::View<reco::Candidate> > hcand;
  iEvent.getByLabel(candSrc, hcand);

  std::auto_ptr<reco::GenParticleRefVector> ret(new reco::GenParticleRefVector());

  for(size_t i=0; i<hgen->size(); ++i) {
    bool matched = false;
    for(edm::View<reco::Candidate>::const_iterator iCand = hcand->begin(); iCand != hcand->end(); ++iCand) {
      if(reco::deltaR(*iCand, *(hgen->at(i))) < maxDeltaR) {
        matched = true;
        break;
      }
    }
    if(!matched)
      //ret->push_back(edm::Ref<reco::GenParticleCollection>(hgen, i));
      //ret->push_back(hgen->refAt(i));
      ret->push_back(hgen->at(i));
  }

  iEvent.put(ret);
}

DEFINE_FWK_MODULE(HPlusGenParticleCleaner);
