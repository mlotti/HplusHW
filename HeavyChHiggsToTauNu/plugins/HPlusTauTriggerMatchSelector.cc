#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"

#include "DataFormats/Math/interface/deltaR.h"

#include<algorithm>

class HPlusTauTriggerMatchSelector: public edm::EDProducer {
public:
  HPlusTauTriggerMatchSelector(const edm::ParameterSet& iConfig);
  ~HPlusTauTriggerMatchSelector();

private:
  void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

  edm::InputTag fTauSrc;
  edm::InputTag fPatTriggerSrc;
  double fDeltaR;
  std::vector<std::string> fFilterNames;
};

HPlusTauTriggerMatchSelector::HPlusTauTriggerMatchSelector(const edm::ParameterSet& iConfig):
  fTauSrc(iConfig.getParameter<edm::InputTag>("tauSrc")),
  fPatTriggerSrc(iConfig.getParameter<edm::InputTag>("patTriggerEventSrc")),
  fDeltaR(iConfig.getParameter<double>("deltaR")),
  fFilterNames(iConfig.getParameter<std::vector<std::string> >("filterNames"))
{
  produces<std::vector<pat::Tau> >();
}

HPlusTauTriggerMatchSelector::~HPlusTauTriggerMatchSelector() {}

void HPlusTauTriggerMatchSelector::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<pat::Tau> > htaus;
  iEvent.getByLabel(fTauSrc, htaus);

  edm::Handle<pat::TriggerEvent> htrigger;
  iEvent.getByLabel(fPatTriggerSrc, htrigger);

  pat::TriggerObjectRefVector filterObjects;
  for(size_t i=0; i<fFilterNames.size(); ++i) {
    pat::TriggerObjectRefVector tmp = htrigger->filterObjects(fFilterNames[i]);
    std::copy(tmp.begin(), tmp.end(), std::back_inserter(filterObjects));
  }

  std::auto_ptr<std::vector<pat::Tau> > result(new std::vector<pat::Tau>());
  for(size_t iTau = 0; iTau < htaus->size(); ++iTau) {
    bool match = false;
    for(size_t iTrigger =0; iTrigger < filterObjects.size(); ++iTrigger) {
      if(reco::deltaR(htaus->at(iTau), *(filterObjects[iTrigger])) < fDeltaR) {
        match = true;
        break;
      }
    }
    if(match) {
      pat::Tau copy = htaus->at(iTau);
      result->push_back(copy);
    }
  }

  iEvent.put(result);
}

DEFINE_FWK_MODULE(HPlusTauTriggerMatchSelector);
