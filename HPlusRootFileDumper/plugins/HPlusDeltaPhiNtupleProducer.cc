#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/METReco/interface/MET.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Math/interface/deltaPhi.h"

#include<string>

class HPlusDeltaPhiNtupleProducer: public edm::EDProducer {
 public:

  explicit HPlusDeltaPhiNtupleProducer(const edm::ParameterSet&);
  ~HPlusDeltaPhiNtupleProducer();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  edm::InputTag fSrc1;
  edm::InputTag fSrc2;
  std::string fAlias;
};

HPlusDeltaPhiNtupleProducer::HPlusDeltaPhiNtupleProducer(const edm::ParameterSet& iConfig):
  fSrc1(iConfig.getParameter<edm::InputTag>("src1")),
  fSrc2(iConfig.getParameter<edm::InputTag>("src2")),
  fAlias(iConfig.getParameter<std::string>("alias"))
{
  produces<double>().setBranchAlias(fAlias);
}
HPlusDeltaPhiNtupleProducer::~HPlusDeltaPhiNtupleProducer() {}
void HPlusDeltaPhiNtupleProducer::beginJob() {}

void HPlusDeltaPhiNtupleProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::Candidate> > hcands1;
  iEvent.getByLabel(fSrc1, hcands1);
  if(hcands1->size() != 1)
    throw cms::Exception("LogicError") << "Expected exactly one candidate, got " << hcands1->size() << " from collection " << fSrc1.encode() << std::endl;

  edm::Handle<edm::View<reco::Candidate> > hcands2;
  iEvent.getByLabel(fSrc2, hcands2);
  if(hcands2->size() != 1)
    throw cms::Exception("LogicError") << "Expected exactly one candidate, got " << hcands2->size() << " from collection " << fSrc2.encode() << std::endl;

  iEvent.put(std::auto_ptr<double>(new double(reco::deltaPhi((*hcands1)[0].phi(), (*hcands2)[0].phi()))));
}

void HPlusDeltaPhiNtupleProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusDeltaPhiNtupleProducer);
