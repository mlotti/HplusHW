#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/METReco/interface/CaloMET.h"

#include<vector>


class HPlusCaloMETSumProducer: public edm::EDProducer {
 public:

  explicit HPlusCaloMETSumProducer(const edm::ParameterSet&);
  ~HPlusCaloMETSumProducer();

 private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  std::vector<edm::InputTag> src;
};

HPlusCaloMETSumProducer::HPlusCaloMETSumProducer(const edm::ParameterSet& iConfig):
  src(iConfig.getParameter<std::vector<edm::InputTag> >("src"))
{
  if(src.empty())
    throw cms::Exception("Configuration") << "At least one src reco::MET must be given" << std::endl;
  produces<std::vector<reco::CaloMET> >();
}
HPlusCaloMETSumProducer::~HPlusCaloMETSumProducer() {}

void HPlusCaloMETSumProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<reco::CaloMET> > hmet;
  iEvent.getByLabel(src[0], hmet);

  reco::MET::LorentzVector metP4 = hmet->at(0).p4();
  reco::MET::Point vertex = hmet->at(0).vertex();
  double sumet = hmet->at(0).sumEt();
  for(size_t i=1; i<src.size(); ++i) {
    iEvent.getByLabel(src[i], hmet);
    metP4 += hmet->at(0).p4();
    sumet += hmet->at(0).sumEt();
  }

  metP4.SetE(std::sqrt(metP4.px()*metP4.px() + metP4.py()*metP4.py()));

  SpecificCaloMETData specific;
  specific.CaloMETInmHF = 0.0;
  specific.CaloMETInpHF = 0.0;
  specific.CaloMETPhiInmHF = 0.0;
  specific.CaloMETPhiInpHF = 0.0;
  specific.CaloSETInmHF = 0.0;
  specific.CaloSETInpHF = 0.0;
  specific.EmEtInEB = 0.0;
  specific.EmEtInEE = 0.0;
  specific.EmEtInHF = 0.0;
  specific.EtFractionEm = 0.0;
  specific.EtFractionHadronic = 0.0;
  specific.HadEtInHB = 0.0;
  specific.HadEtInHE = 0.0;
  specific.HadEtInHF = 0.0;
  specific.HadEtInHO = 0.0;
  specific.MaxEtInEmTowers = 0.0;
  specific.MaxEtInHadTowers = 0.0;
  specific.METSignificance = 0.0;
  std::auto_ptr<std::vector<reco::CaloMET> > ret(new std::vector<reco::CaloMET>());
  ret->push_back(reco::CaloMET(specific, sumet, metP4, vertex));

  iEvent.put(ret);
}

DEFINE_FWK_MODULE(HPlusCaloMETSumProducer);
