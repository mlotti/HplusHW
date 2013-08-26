#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
//#include "DataFormats/Common/interface/Ptr.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/Framework/interface/Event.h"

class HPlusMCHasBJetFilter: public edm::EDFilter {
 public:

  explicit HPlusMCHasBJetFilter(const edm::ParameterSet&);
  ~HPlusMCHasBJetFilter();

 private:
  virtual void beginJob();
  virtual bool filter(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  virtual bool endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup);
  bool bHasBjets;
};

HPlusMCHasBJetFilter::HPlusMCHasBJetFilter(const edm::ParameterSet& pset) :
  bHasBjets(pset.getUntrackedParameter<bool>("hasBjets")) {
}
HPlusMCHasBJetFilter::~HPlusMCHasBJetFilter() {}
void HPlusMCHasBJetFilter::beginJob() {}

bool HPlusMCHasBJetFilter::endLuminosityBlock(edm::LuminosityBlock& iBlock, const edm::EventSetup & iSetup) {
  return true;
}

bool HPlusMCHasBJetFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  bool myBFound = false;
  edm::Handle <reco::GenParticleCollection> genParticles;
  iEvent.getByLabel("genParticles", genParticles);
  for (size_t i=0; i < genParticles->size(); ++i){
    const reco::Candidate & p = (*genParticles)[i];
    int id = p.pdgId();
    if (std::abs(id) == 5)
      myBFound = true;
  }
  if (bHasBjets)
    return myBFound;
  return !myBFound;
}

void HPlusMCHasBJetFilter::endJob() {

}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusMCHasBJetFilter);
