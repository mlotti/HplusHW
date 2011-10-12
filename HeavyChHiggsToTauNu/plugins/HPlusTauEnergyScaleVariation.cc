#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"

#include "DataFormats/PatCandidates/interface/Tau.h"

class HPlusTauEnergyScaleVariation: public edm::EDProducer {
public:
  explicit HPlusTauEnergyScaleVariation(const edm::ParameterSet&);
  ~HPlusTauEnergyScaleVariation();

private:
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  edm::InputTag src;
  const double energyVariation;
  const double energyEtaVariation;
};

HPlusTauEnergyScaleVariation::HPlusTauEnergyScaleVariation(const edm::ParameterSet& iConfig):
  src(iConfig.getParameter<edm::InputTag>("src")),
  energyVariation(iConfig.getParameter<double>("energyVariation")),
  energyEtaVariation(iConfig.getParameter<double>("energyEtaVariation"))
{
  produces<pat::TauCollection>();

  if (energyVariation < -1. || energyVariation > 1.) {
    throw cms::Exception("Configuration") << "Invalid value for energyVariation! Please provide a value between -1..1 (value=" << energyVariation << ").";
  }
  if (energyEtaVariation < -1. || energyEtaVariation > 1.) {
    throw cms::Exception("Configuration") << "Invalid value for energyEtaVariation! Please provide a value between -1..1 (value=" << energyEtaVariation << ").";
  }
}
HPlusTauEnergyScaleVariation::~HPlusTauEnergyScaleVariation() {}

void HPlusTauEnergyScaleVariation::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  std::auto_ptr<pat::TauCollection> rescaledTaus(new pat::TauCollection);

  typedef pat::Tau::LorentzVector LorentzVector;

  edm::Handle<edm::View<pat::Tau> > htaus;
  iEvent.getByLabel(src, htaus);

  for(edm::View<pat::Tau>::const_iterator iTau = htaus->begin(); iTau != htaus->end(); ++iTau) {
    double myChange = std::sqrt(energyVariation*energyVariation 
                                + energyEtaVariation*energyEtaVariation / iTau->eta() / iTau->eta());
    double myFactor = 1. + myChange;
    if (energyVariation < 0) myFactor = 1. - myChange;
    LorentzVector p4 = iTau->p4()*myFactor; 

    pat::Tau tau = *iTau;
    tau.setP4(iTau->p4()*myFactor);
    tau.addUserFloat("originalPx", iTau->px());
    tau.addUserFloat("originalPy", iTau->py());
    rescaledTaus->push_back(tau);
  }
  iEvent.put(rescaledTaus);
}

//define this as a plug-in
DEFINE_FWK_MODULE(HPlusTauEnergyScaleVariation);
