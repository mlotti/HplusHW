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

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/TransverseMass.h"

class HPlusTransverseMassProducer: public edm::EDProducer {
public:
  HPlusTransverseMassProducer(const edm::ParameterSet& iConfig);
  ~HPlusTransverseMassProducer();
  
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();
  
private:
  typedef std::vector<reco::LeafCandidate> Product;

  const edm::InputTag taus_;
  const edm::InputTag met_;
};

HPlusTransverseMassProducer::HPlusTransverseMassProducer(const edm::ParameterSet& iConfig):
  taus_(iConfig.getParameter<edm::InputTag>("tauSrc")),
  met_(iConfig.getParameter<edm::InputTag>("metSrc")) {

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
    cand.setMass(HPlus::TransverseMass::reconstruct(*iTau, *metPtr));
    result->push_back(cand);
  }

  iEvent.put(result);
}


void HPlusTransverseMassProducer::endJob() {}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTransverseMassProducer);
