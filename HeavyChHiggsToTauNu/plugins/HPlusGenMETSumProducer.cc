#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/METReco/interface/GenMET.h"

#include<vector>


class HPlusGenMETSumProducer: public edm::EDProducer {
 public:

  explicit HPlusGenMETSumProducer(const edm::ParameterSet&);
  ~HPlusGenMETSumProducer();

 private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  std::vector<edm::InputTag> src;
};

HPlusGenMETSumProducer::HPlusGenMETSumProducer(const edm::ParameterSet& iConfig):
  src(iConfig.getParameter<std::vector<edm::InputTag> >("src"))
{
  if(src.empty())
    throw cms::Exception("Configuration") << "At least one src GenMET must be given" << std::endl;
  produces<std::vector<reco::GenMET> >();
}
HPlusGenMETSumProducer::~HPlusGenMETSumProducer() {}

void HPlusGenMETSumProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::GenMET> > hmet;
  iEvent.getByLabel(src[0], hmet);

  reco::GenMET::LorentzVector metP4 = hmet->at(0).p4();
  reco::GenMET::Point vertex = hmet->at(0).vertex();
  double sumet = hmet->at(0).sumEt();
  for(size_t i=1; i<src.size(); ++i) {
    iEvent.getByLabel(src[i], hmet);
    metP4 += hmet->at(0).p4();
    sumet += hmet->at(0).sumEt();
  }

  metP4.SetE(std::sqrt(metP4.px()*metP4.px() + metP4.py()*metP4.py()));

  SpecificGenMETData specific;
  specific.NeutralEMEtFraction = 0.0;
  specific.NeutralEMEtFraction = 0.0;
  specific.NeutralHadEtFraction = 0.0;
  specific.ChargedEMEtFraction = 0.0;
  specific.ChargedHadEtFraction = 0.0;
  specific.MuonEtFraction = 0.0;
  specific.InvisibleEtFraction = 0.0;

  std::auto_ptr<std::vector<reco::GenMET> > ret(new std::vector<reco::GenMET>());
  ret->push_back(reco::GenMET(specific, sumet, metP4, vertex));

  iEvent.put(ret);
}

DEFINE_FWK_MODULE(HPlusGenMETSumProducer);
