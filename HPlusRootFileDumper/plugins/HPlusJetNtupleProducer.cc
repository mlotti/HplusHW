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
    Discriminator(const std::string& d, const std::string& b): fDiscr(d), fBranch(b) {}
    std::string fDiscr;
    std::string fBranch;
  };

  std::vector<Discriminator> fBDiscriminators;
  edm::InputTag fSrc;
  std::string fPrefix;
};

HPlusJetNtupleProducer::HPlusJetNtupleProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getParameter<edm::InputTag>("src")),
  fPrefix(iConfig.getParameter<std::string>("prefix"))
{
  std::string name;

  // jet branches
  name = "number";
  produces<int>(name).setBranchAlias(fPrefix+name);

  // b-tagging branches (one branch per discriminator, value is the
  // maximum over the jets passing the pt/eta cuts)
  if(iConfig.exists("bDiscriminators")) {
    std::vector<edm::ParameterSet> btagParam = iConfig.getParameter<std::vector<edm::ParameterSet> >("bDiscriminators");
    fBDiscriminators.reserve(btagParam.size()); 

    for(size_t i=0; i<btagParam.size(); ++i) {
      name = btagParam[i].getParameter<std::string>("branch");
      produces<float>(name).setBranchAlias(fPrefix+name);
      fBDiscriminators.push_back(Discriminator(btagParam[i].getParameter<std::string>("discriminator"), name));
    }
  }
}
HPlusJetNtupleProducer::~HPlusJetNtupleProducer() {}
void HPlusJetNtupleProducer::beginJob() {}

void HPlusJetNtupleProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > hcands;
  iEvent.getByLabel(fSrc, hcands);

  edm::PtrVector<pat::Jet> jets;
  jets.reserve(hcands->size());
  for(size_t i=0; i<hcands->size(); ++i) {
    edm::Ptr<pat::Jet> jet(hcands->ptrAt(i));
    if(jet.get() == 0)
      throw cms::Exception("ProductNotFound") << "Objects in jet collection " << fSrc.encode() << " are not derived from pat::Jet!" << std::endl;
    jets.push_back(jet);
  }

  // For each b discriminator, take the maximum value over the
  // selected jets (this is enough if we seek for one b-tagged jet,
  // for 2 b-tagged jets we would need the 2nd maximum value)
  for(std::vector<Discriminator>::const_iterator iDiscr = fBDiscriminators.begin(); iDiscr != fBDiscriminators.end(); ++iDiscr) {
    float maxDiscr = std::numeric_limits<float>::quiet_NaN();
    if(!jets.empty()) {
      maxDiscr = jets[0]->bDiscriminator(iDiscr->fDiscr);
    }
    for(size_t i=1; i<jets.size(); ++i) {
      maxDiscr = std::max(maxDiscr, jets[i]->bDiscriminator(iDiscr->fDiscr));
    }

    iEvent.put(std::auto_ptr<float>(new float(maxDiscr)), iDiscr->fBranch);
  }

  iEvent.put(std::auto_ptr<int>(new int(jets.size())), "number");
}

void HPlusJetNtupleProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusJetNtupleProducer);
