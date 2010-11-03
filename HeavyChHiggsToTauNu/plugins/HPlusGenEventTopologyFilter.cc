#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

class HPlusGenEventTopologyFilter: public edm::EDFilter {
 public:

  explicit HPlusGenEventTopologyFilter(const edm::ParameterSet&);
  ~HPlusGenEventTopologyFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  edm::InputTag src_;
  StringCutObjectSelector<reco::GenParticle> particle_;
  StringCutObjectSelector<reco::GenParticle> daughter_;
  unsigned int minParticles_;
  unsigned int minDaughters_;
};

HPlusGenEventTopologyFilter::HPlusGenEventTopologyFilter(const edm::ParameterSet& iConfig):
  src_(iConfig.getParameter<edm::InputTag>("src")),
  particle_(iConfig.getParameter<std::string>("particle")),
  daughter_(iConfig.getParameter<std::string>("daughter")),
  minParticles_(iConfig.getParameter<unsigned int>("minParticles")),
  minDaughters_(iConfig.getParameter<unsigned int>("minDaughters"))
{
}
HPlusGenEventTopologyFilter::~HPlusGenEventTopologyFilter() {}
void HPlusGenEventTopologyFilter::beginJob() {}

bool HPlusGenEventTopologyFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::GenParticle> > hgen;
  iEvent.getByLabel(src_, hgen);

  unsigned int nParticles = 0;
  for(edm::View<reco::GenParticle>::const_iterator iGen = hgen->begin(); iGen != hgen->end(); ++iGen) {
    if(particle_(*iGen)) {
      unsigned int nDaughters=0;
      for(size_t i=0; i<iGen->numberOfDaughters(); ++i) {
        if(daughter_(*dynamic_cast<const reco::GenParticle *>(iGen->daughter(i))))
          ++nDaughters;
      }
      if(nDaughters >= minDaughters_)
        ++nParticles;
    }
  }
  if(nParticles >= minParticles_)
    return true;
  else
    return false;
}

void HPlusGenEventTopologyFilter::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusGenEventTopologyFilter);
