#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/METReco/interface/MET.h"

#include "TLorentzVector.h"

namespace {
}

class HPlusTransverseMassProducer: public edm::EDProducer {
public:
  HPlusTransverseMassProducer(const edm::ParameterSet& iConfig);
  ~HPlusTransverseMassProducer();
  
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();
  
private:
  double recoalgo(const reco::Candidate& j1, const reco::MET& met) const;

  typedef std::vector<reco::LeafCandidate> Product;

  const edm::InputTag taus_;
  const edm::InputTag met_;
  const double tauMass_;
};

HPlusTransverseMassProducer::HPlusTransverseMassProducer(const edm::ParameterSet& iConfig):
  taus_(iConfig.getParameter<edm::InputTag>("tauSrc")),
  met_(iConfig.getParameter<edm::InputTag>("metSrc")),
  tauMass_(iConfig.getParameter<double>("tauMass")) {

  produces<Product>();
}

HPlusTransverseMassProducer::~HPlusTransverseMassProducer() {}


void HPlusTransverseMassProducer::beginJob() {}

void HPlusTransverseMassProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > taus;
  iEvent.getByLabel(taus_, taus);

  edm::Handle<edm::View<reco::Candidate> > met;
  iEvent.getByLabel(met_, met);

  if(met->size() != 1)
    throw cms::Exception("LogicError") << "MET collection " << met_.encode() << " has " << met->size() << " != 1 elements!" << std::endl;

  edm::Ptr<reco::MET> metPtr(met->ptrAt(0));
  if(metPtr.get() == 0) // check that the implicit dynamic_cast to reco::MET succeeds
    throw cms::Exception("ProductNotFound") << "\"MET\" object in collection " << met_.encode() << " is not derived from reco::MET" << std::endl;

  std::auto_ptr<Product> result(new Product());
  result->reserve(taus->size());

  for(edm::View<reco::Candidate>::const_iterator iTau = taus->begin(); iTau != taus->end(); ++iTau) {
    reco::LeafCandidate cand;
    cand.setMass(recoalgo(*iTau, *metPtr));
    result->push_back(cand);
  }

  iEvent.put(result);
}

double HPlusTransverseMassProducer::recoalgo(const reco::Candidate& j1, const reco::MET& met) const {
  // Construct tau vector, mtau = 1.777 GeV/c2
  TLorentzVector myTau;
  myTau.SetXYZM(j1.px(), j1.py(), j1.pz(), tauMass_); 
  // Calculate cosine of angle between jet and met direction
  double myEtMiss = sqrt(met.px()*met.px() + met.py()+met.py());
  double myCosPhi = 100;
  if (myEtMiss > 0 && myTau.Pt() > 0)
    myCosPhi = (myTau.X()*met.px() + myTau.Y()*met.py()) / (myTau.Pt()*myEtMiss);
  // Calculate transverse mass
  double myTransverseMass = -999;
  double myTransverseMassSquared = 0;
  if (myCosPhi < 10)
    myTransverseMassSquared = 2 * myTau.Et() * myEtMiss * (1.0-myCosPhi);
  if (myTransverseMassSquared >= 0)
    myTransverseMass = TMath::Sqrt(myTransverseMassSquared);
  return myTransverseMass;
}

void HPlusTransverseMassProducer::endJob() {}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTransverseMassProducer);
