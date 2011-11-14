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
      double origX = (*iObj)->userFloat("originalPx");
      double origY = (*iObj)->userFloat("originalPy");
      clusteredP4 += reco::Candidate::LorentzVector(origX, origY, 0, std::sqrt(origX*origX + origY*origY));
      clusteredP4Variated += (*iObj)->p4();
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

  edm::Handle<edm::View<reco::Candidate> > htaus;
  iEvent.getByLabel(tauSrc, htaus);

  edm::Handle<edm::View<pat::Jet> > hjets;
  iEvent.getByLabel(jetSrc, hjets);

  edm::PtrVector<pat::Tau> taus;
  for(size_t i=0; i<htaus->size(); ++i) {
    edm::Ptr<reco::Candidate> ptr = htaus->ptrAt(i);
    taus.push_back(edm::Ptr<pat::Tau>(ptr.id(), dynamic_cast<const pat::Tau *>(ptr.get()), ptr.key()));
  }
  edm::PtrVector<pat::Jet> jets = hjets->ptrVector();

  for(edm::View<pat::MET>::const_iterator iMet = hmets->begin(); iMet != hmets->end(); ++iMet) {
    reco::Candidate::LorentzVector clusteredP4;
    reco::Candidate::LorentzVector clusteredP4Variated;

    addClusteredP4(clusteredP4, clusteredP4Variated, taus.begin(), taus.end());

    /*
    std::cout << "Tau clustered " << clusteredP4.Pt() << " " << clusteredP4.Phi() << " " << clusteredP4 << std::endl
              << "     variated " << clusteredP4Variated.Pt() << " " << clusteredP4Variated.Phi() << " " << clusteredP4Variated << std::endl;
    */

    addClusteredP4(clusteredP4, clusteredP4Variated, jets.begin(), jets.end());

    /*
    std::cout << "Jet clustered " << clusteredP4.Pt() << " " << clusteredP4 << std::endl
              << "     variated " << clusteredP4Variated.Pt() << " " << clusteredP4Variated << std::endl;
    */

    reco::Candidate::LorentzVector p4 = iMet->p4();
    //std::cout << "MET original " << p4.Pt() << " " << p4.Phi() << " " << p4 << std::endl;
    p4 -= clusteredP4;
    //std::cout << "    - clustered " << p4.Pt() << " " << p4.Phi() << " " << p4 << std::endl;
    p4 *= (1 + unclusteredVariation);
    //std::cout << "    variated " << p4.Pt() << " " << p4.Phi() << " " << p4 << std::endl;
    p4 += clusteredP4Variated;
    //std::cout << "    + clustered " << p4.Pt() << " " << p4.Phi() << " " << p4 << std::endl;
    p4.SetPz(0);
    p4.SetE(p4.Pt());
    //std::cout << "    final " << p4.Pt() << " " << p4.Phi() << " " << p4 << std::endl;
    pat::MET met = *iMet;
    met.setP4(p4);
    //std::cout << "    final " << p4.Et() << " " << p4.Phi() << " " << p4 << std::endl;
    //std::cout << "    final " << met.et() << std::endl;
    rescaledMets->push_back(met);
  }
  iEvent.put(rescaledMets);
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusMetEnergyScaleVariation);
