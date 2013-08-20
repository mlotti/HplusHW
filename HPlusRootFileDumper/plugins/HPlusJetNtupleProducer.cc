#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include<string>

// Note: this class could otherwise be fully replaced with the generic
// CandViewNtpProducer, but that would produce vector<double> instead
// of double only. In other words, this class is suitable for *one jet
// only*. If more taus are needed, look for the CandViewNtpProducer
// first!

class HPlusJetNtupleProducer: public edm::EDProducer {
 public:

  explicit HPlusJetNtupleProducer(const edm::ParameterSet&);
  ~HPlusJetNtupleProducer();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  struct Discriminator {
    Discriminator(const std::string& d): fDiscr(d) {}
    std::string fDiscr;
    std::vector<float> fValues;
  };

  typedef math::XYZTLorentzVector XYZTLorentzVector;
  typedef math::XYZPoint XYZPoint;

  std::vector<Discriminator> fBDiscriminators;
  edm::InputTag fSrc;
};

HPlusJetNtupleProducer::HPlusJetNtupleProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getParameter<edm::InputTag>("src"))
{
  std::string prefix(iConfig.getParameter<std::string>("prefix"));
  std::string name;

  // jet branches
  name = "p4";
  produces<std::vector<XYZTLorentzVector> >(name).setBranchAlias(prefix+name);

  // b-tagging branches (one branch per discriminator, value is the
  // maximum over the jets passing the pt/eta cuts)
  if(iConfig.exists("bDiscriminators")) {
    std::vector<std::string> btagParam = iConfig.getParameter<std::vector<std::string> >("bDiscriminators");
    fBDiscriminators.reserve(btagParam.size()); 

    for(size_t i=0; i<btagParam.size(); ++i) {
      name = btagParam[i];
      produces<std::vector<float> >(name).setBranchAlias(prefix+"btag_"+name);
      fBDiscriminators.push_back(Discriminator(name));
    }
  }
}
HPlusJetNtupleProducer::~HPlusJetNtupleProducer() {}
void HPlusJetNtupleProducer::beginJob() {}

void HPlusJetNtupleProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > hcands;
  iEvent.getByLabel(fSrc, hcands);

  std::auto_ptr<std::vector<XYZTLorentzVector> > p4s(new std::vector<XYZTLorentzVector>());
  p4s->reserve(hcands->size());

  for(size_t i=0; i<fBDiscriminators.size(); ++i) {
    fBDiscriminators[i].fValues.reserve(hcands->size());
  }

  for(size_t i=0; i<hcands->size(); ++i) {
    edm::Ptr<pat::Jet> jet(hcands->ptrAt(i));
    if(jet.get() == 0)
      throw cms::Exception("ProductNotFound") << "Object " << i << " in jet collection " << fSrc.encode() << " is not derived from pat::Jet" << std::endl;

    p4s->push_back(XYZTLorentzVector(jet->p4()));
    for(std::vector<Discriminator>::iterator iDiscr = fBDiscriminators.begin(); iDiscr != fBDiscriminators.end(); ++iDiscr) {
      iDiscr->fValues.push_back(jet->bDiscriminator(iDiscr->fDiscr));
    }
  }

  iEvent.put(p4s, "p4");

  for(std::vector<Discriminator>::iterator iDiscr = fBDiscriminators.begin(); iDiscr != fBDiscriminators.end(); ++iDiscr) {
    iEvent.put(std::auto_ptr<std::vector<float> >(new std::vector<float>(iDiscr->fValues)), iDiscr->fDiscr);
    iDiscr->fValues.clear();
  }
}

void HPlusJetNtupleProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusJetNtupleProducer);
