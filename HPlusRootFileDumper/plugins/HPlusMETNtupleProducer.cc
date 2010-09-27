#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/METReco/interface/MET.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include<string>

// Note: this class could otherwise be fully replaced with the generic
// CandViewNtpProducer, but that would produce vector<double> instead
// of double only. 

class HPlusMETNtupleProducer: public edm::EDProducer {
 public:

  explicit HPlusMETNtupleProducer(const edm::ParameterSet&);
  ~HPlusMETNtupleProducer();

 private:
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  edm::InputTag fSrc;
  std::string fAlias;
};

HPlusMETNtupleProducer::HPlusMETNtupleProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getParameter<edm::InputTag>("src")),
  fAlias(iConfig.getParameter<std::string>("alias"))
{
  produces<double>().setBranchAlias(fAlias);
}
HPlusMETNtupleProducer::~HPlusMETNtupleProducer() {}
void HPlusMETNtupleProducer::beginJob() {}

void HPlusMETNtupleProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::MET> > hcands;
  iEvent.getByLabel(fSrc, hcands);

  iEvent.put(std::auto_ptr<double>(new double((*hcands)[0].et())));
}

void HPlusMETNtupleProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusMETNtupleProducer);
