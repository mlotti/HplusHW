#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/VertexWeight.h"

class HPlusVertexWeightProducer: public edm::EDProducer {
public:
  explicit HPlusVertexWeightProducer(const edm::ParameterSet&);
  ~HPlusVertexWeightProducer();

private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  HPlus::VertexWeight fVertexWeight;
  std::string fAlias;
};

HPlusVertexWeightProducer::HPlusVertexWeightProducer(const edm::ParameterSet& iConfig):
  fVertexWeight(iConfig),
  fAlias(iConfig.getParameter<std::string>("alias"))
{
  produces<double>().setBranchAlias(fAlias);
}
HPlusVertexWeightProducer::~HPlusVertexWeightProducer() {}

void HPlusVertexWeightProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  iEvent.put(std::auto_ptr<double>(new double(fVertexWeight.getWeight(iEvent, iSetup))));
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusVertexWeightProducer);
