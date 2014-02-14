#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "TF1.h"

#include<cmath>


class HPlusWTauMuWeightProducer: public edm::EDProducer {
public:
  explicit HPlusWTauMuWeightProducer(const edm::ParameterSet&);
  ~HPlusWTauMuWeightProducer();

private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  const edm::InputTag fSrc; 
  const std::string fAlias;
  const TF1 fFormula;
  const double fVariationAmount;
  const bool fEnabled;
  const bool fVariationEnabled;
};

HPlusWTauMuWeightProducer::HPlusWTauMuWeightProducer(const edm::ParameterSet& iConfig):
  fSrc(iConfig.getParameter<edm::InputTag>("muonSrc")),
  fAlias(iConfig.getParameter<std::string>("alias")),
  fFormula("WTauMu", iConfig.getParameter<std::string>("formula").c_str()),
  fVariationAmount(iConfig.getParameter<double>("variationAmount")),
  fEnabled(iConfig.getParameter<bool>("enabled")),
  fVariationEnabled(iConfig.getParameter<bool>("variationEnabled"))
{
  produces<double>().setBranchAlias(fAlias);
}

HPlusWTauMuWeightProducer::~HPlusWTauMuWeightProducer() {}

void HPlusWTauMuWeightProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  double weight = 1.0;

  if(fEnabled) {
    edm::Handle<edm::View<pat::Muon> > hmuons;
    iEvent.getByLabel(fSrc, hmuons);
    
    weight = fFormula.Eval(hmuons->at(0).pt());
    if(fVariationEnabled) {
      weight *= (1+fVariationAmount);
    }
    if(weight > 1.0)
      weight = 1.0;
    if(weight < 0.0)
      weight = 0.0;
  }

  iEvent.put(std::auto_ptr<double>(new double(weight)));
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusWTauMuWeightProducer);
