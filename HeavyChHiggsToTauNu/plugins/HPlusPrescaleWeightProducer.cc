#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Utilities/interface/InputTag.h"

#include "CommonTools/TriggerUtils/interface/PrescaleWeightProvider.h"

#include<string>

class HPlusPrescaleWeightProducer: public edm::EDProducer {
 public:

  explicit HPlusPrescaleWeightProducer(const edm::ParameterSet&);
  ~HPlusPrescaleWeightProducer();

 private:
  virtual void beginRun(edm::Run& iRun, const edm::EventSetup& iSetup);
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  PrescaleWeightProvider fPrescale;
  std::string fAlias;
};

HPlusPrescaleWeightProducer::HPlusPrescaleWeightProducer(const edm::ParameterSet& iConfig):
  fPrescale(iConfig),
  fAlias(iConfig.getParameter<std::string>("alias"))
{
  produces<double>().setBranchAlias(fAlias);
}
HPlusPrescaleWeightProducer::~HPlusPrescaleWeightProducer() {}

void HPlusPrescaleWeightProducer::beginRun(edm::Run& iRun, const edm::EventSetup& iSetup) {
  fPrescale.initRun(iRun, iSetup);
}

void HPlusPrescaleWeightProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  iEvent.put(std::auto_ptr<double>(new double(fPrescale.prescaleWeight(iEvent, iSetup))));
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusPrescaleWeightProducer);
