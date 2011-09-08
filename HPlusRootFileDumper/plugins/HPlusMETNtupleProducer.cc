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

  typedef math::XYZTLorentzVector XYZTLorentzVector;

  edm::InputTag fSrc;
};

HPlusMETNtupleProducer::HPlusMETNtupleProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getParameter<edm::InputTag>("src"))
{
  std::string alias(iConfig.getParameter<std::string>("alias"));
  produces<XYZTLorentzVector>().setBranchAlias(alias);
}
HPlusMETNtupleProducer::~HPlusMETNtupleProducer() {}
void HPlusMETNtupleProducer::beginJob() {}

void HPlusMETNtupleProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::MET> > hcands;
  iEvent.getByLabel(fSrc, hcands);

  iEvent.put(std::auto_ptr<XYZTLorentzVector>(new XYZTLorentzVector((*hcands)[0].p4())));
}

void HPlusMETNtupleProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusMETNtupleProducer);
