#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include<string>

// Note: this class could otherwise be fully replaced with the generic
// CandViewNtpProducer, but that would produce vector<double> instead
// of double only. In other words, this class is suitable for *one tau
// only*. If more taus are needed, look for the CandViewNtpProducer
// first!

class HPlusTauNtupleProducer: public edm::EDProducer {
 public:

  explicit HPlusTauNtupleProducer(const edm::ParameterSet&);
  ~HPlusTauNtupleProducer();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  struct Discriminator {
    Discriminator(const std::string& d, const std::string& b): fDiscr(d), fBranch(b) {}
    std::string fDiscr;
    std::string fBranch;
  };

  std::vector<Discriminator> fTauDiscriminators;
  edm::InputTag fSrc;
  std::string fPrefix;
};

HPlusTauNtupleProducer::HPlusTauNtupleProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
  fPrefix(iConfig.getUntrackedParameter<std::string>("prefix"))
{
  std::string name;

  // tau branches
  name = "pt";
  produces<double>(name).setBranchAlias(fPrefix+name);
  name = "eta";
  produces<double>(name).setBranchAlias(fPrefix+name);
  name = "rtau";
  produces<double>(name).setBranchAlias(fPrefix+name);

  if(iConfig.exists("tauDiscriminators")) {
    std::vector<edm::ParameterSet> tauParam = iConfig.getUntrackedParameter<std::vector<edm::ParameterSet> >("tauDiscriminators");
    fTauDiscriminators.reserve(tauParam.size());
    for(size_t i=0; i<tauParam.size(); ++i) {
      name = tauParam[i].getUntrackedParameter<std::string>("branch");
      produces<double>(name).setBranchAlias(fPrefix+name);
      fTauDiscriminators.push_back(Discriminator(tauParam[i].getUntrackedParameter<std::string>("discriminator"), name));
    }
  }
}
HPlusTauNtupleProducer::~HPlusTauNtupleProducer() {}
void HPlusTauNtupleProducer::beginJob() {}

void HPlusTauNtupleProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > hcands;
  iEvent.getByLabel(fSrc, hcands);

  if(hcands->size() != 1)
    throw cms::Exception("LogicError") << "Expected exactly one tau, got " << hcands->size() << " from collection " << fSrc.encode() << std::endl;
  edm::Ptr<pat::Tau> tau(hcands->ptrAt(0));
  if(tau.get() == 0)
    throw cms::Exception("ProductNotFound") << "Objects in tau collection " << fSrc.encode() << " are not derived from pat::Tau!" << std::endl;

  // Take the pt and eta of tau
  iEvent.put(std::auto_ptr<double>(new double(tau->pt())), "pt");
  iEvent.put(std::auto_ptr<double>(new double(tau->eta())), "eta");

  std::auto_ptr<double> rtau(new double(0));
  if(tau->pt() > 0) {
    if(tau->isPFTau()) {
      reco::PFCandidateRef leadCand = tau->leadPFChargedHadrCand();
      if(leadCand.isNonnull())
        *rtau = leadCand->p()/tau->p();
    }
    else if(tau->isCaloTau()) {
      reco::TrackRef leadTrack = tau->leadTrack();
      if(leadTrack.isNonnull())
        *rtau = leadTrack->p()/tau->p();
    }
  }
  iEvent.put(rtau, "rtau");

  // Tau discriminators
  for(std::vector<Discriminator>::const_iterator iDiscr = fTauDiscriminators.begin(); iDiscr != fTauDiscriminators.end(); ++iDiscr) {
    iEvent.put(std::auto_ptr<double>(new double(tau->tauID(iDiscr->fDiscr))), iDiscr->fBranch);
  }
}

void HPlusTauNtupleProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTauNtupleProducer);
