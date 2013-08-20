#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/GenParticleTools.h"

#include<vector>

class HPlusGenVisibleTauComputer: public edm::EDProducer {
public:
  explicit HPlusGenVisibleTauComputer(const edm::ParameterSet& iConfig):
    fSrc(iConfig.getParameter<edm::InputTag>("src")) {
    produces<std::vector<math::XYZTLorentzVector> >();
  }
  ~HPlusGenVisibleTauComputer() {}

private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<reco::GenParticle> > hcand;
    iEvent.getByLabel(fSrc, hcand);

    std::auto_ptr<std::vector<math::XYZTLorentzVector> > prod(new std::vector<math::XYZTLorentzVector>());
    prod->reserve(hcand->size());
    for(edm::View<reco::GenParticle>::const_iterator iCand = hcand->begin(); iCand != hcand->end(); ++iCand) {
      prod->push_back(HPlus::GenParticleTools::calculateVisibleTau(&(*iCand)));
    }

    iEvent.put(prod);
  }

  edm::InputTag fSrc;
};

DEFINE_FWK_MODULE(HPlusGenVisibleTauComputer);
