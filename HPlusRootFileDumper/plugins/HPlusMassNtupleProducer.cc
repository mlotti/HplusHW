#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include<string>

// Note: this class could otherwise be fully replaced with the generic
// CandViewNtpProducer, but that would produce vector<double> instead
// of double only. In other words, this class is suitable for *one
// candidate only*. If more taus are needed, look for the
// CandViewNtpProducer first!

class HPlusMassNtupleProducer: public edm::EDProducer {
 public:

  explicit HPlusMassNtupleProducer(const edm::ParameterSet&);
  ~HPlusMassNtupleProducer();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  edm::InputTag fSrc;
  std::string fAlias;
};

HPlusMassNtupleProducer::HPlusMassNtupleProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getUntrackedParameter<edm::InputTag>("src")),
  fAlias(iConfig.getUntrackedParameter<std::string>("alias"))
{
  produces<double>().setBranchAlias(fAlias);
}
HPlusMassNtupleProducer::~HPlusMassNtupleProducer() {}
void HPlusMassNtupleProducer::beginJob() {}

void HPlusMassNtupleProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > hcands;
  iEvent.getByLabel(fSrc, hcands);

  if(hcands->size() != 1)
    throw cms::Exception("LogicError") << "Expected exactly one candidate, got " << hcands->size() << " from collection " << fSrc.encode() << std::endl;
    
  iEvent.put(std::auto_ptr<double>(new double((*hcands)[0].mass())));
}

void HPlusMassNtupleProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusMassNtupleProducer);
