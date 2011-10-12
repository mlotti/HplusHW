#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include<vector>

namespace {
  template <class T>
  void addClusteredP4(reco::Candidate::LorentzVector& clusteredP4,
                      reco::Candidate::LorentzVector& clusteredP4Variated,
                      T begin, T end) {
    for(T iObj = begin; iObj != end; ++iObj) {
      double origX = iObj->userFloat("originalPx");
      double origY = iObj->userFloat("originalPy");
      clusteredP4 += reco::Candidate::LorentzVector(origX, origY, 0, std::sqrt(origX*origX + origY*origY));
      clusteredP4Variated += iObj->p4();
    }
  }
}

class HPlusMetEnergyScaleVariation: public edm::EDProducer {
public:
  explicit HPlusMetEnergyScaleVariation(const edm::ParameterSet&);
  ~HPlusMetEnergyScaleVariation();

private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  edm::InputTag metSrc;
  edm::InputTag tauSrc;
  edm::InputTag jetSrc;
  const double unclusteredVariation;
};

HPlusMetEnergyScaleVariation::HPlusMetEnergyScaleVariation(const edm::ParameterSet& iConfig):
  metSrc(iConfig.getParameter<edm::InputTag>("metSrc")),
  tauSrc(iConfig.getParameter<edm::InputTag>("tauSrc")),
  jetSrc(iConfig.getParameter<edm::InputTag>("jetSrc")),
  unclusteredVariation(iConfig.getParameter<double>("unclusteredVariation"))
{
  produces<pat::METCollection>();
}
HPlusMetEnergyScaleVariation::~HPlusMetEnergyScaleVariation() {}

void HPlusMetEnergyScaleVariation::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  std::auto_ptr<pat::METCollection> rescaledMets(new pat::METCollection);

  typedef pat::Jet::LorentzVector LorentzVector;

  edm::Handle<edm::View<pat::MET> > hmets;
  iEvent.getByLabel(metSrc, hmets);

  edm::Handle<edm::View<pat::Tau> > htaus;
  iEvent.getByLabel(tauSrc, htaus);

  edm::Handle<edm::View<pat::Jet> > hjets;
  iEvent.getByLabel(jetSrc, hjets);

  for(edm::View<pat::MET>::const_iterator iMet = hmets->begin(); iMet != hmets->end(); ++iMet) {
    reco::Candidate::LorentzVector clusteredP4;
    reco::Candidate::LorentzVector clusteredP4Variated;

    addClusteredP4(clusteredP4, clusteredP4Variated, htaus->begin(), htaus->end());
    addClusteredP4(clusteredP4, clusteredP4Variated, hjets->begin(), hjets->end());

    reco::Candidate::LorentzVector p4 = iMet->p4();
    p4 -= clusteredP4;
    p4 *= (1 + unclusteredVariation);
    p4 += clusteredP4Variated;
    p4.SetPz(0);
    p4.SetE(p4.Pt());
    pat::MET met = *iMet;
    met.setP4(p4);
    rescaledMets->push_back(met);
  }
  iEvent.put(rescaledMets);
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusMetEnergyScaleVariation);
