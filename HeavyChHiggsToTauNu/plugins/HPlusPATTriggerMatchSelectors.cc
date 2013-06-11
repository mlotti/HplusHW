#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"

#include "DataFormats/Math/interface/deltaR.h"

#include<algorithm>

namespace {
  template <typename T>
  class PATTriggerMatchSelector: public edm::EDProducer {
  public:
    PATTriggerMatchSelector(const edm::ParameterSet& iConfig);
    ~PATTriggerMatchSelector();

  private:
    void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);

    edm::InputTag fSrc;
    edm::InputTag fPatTriggerSrc;
    double fDeltaR;
    std::vector<std::string> fFilterNames;
  };

  template <typename T>
  PATTriggerMatchSelector<T>::PATTriggerMatchSelector(const edm::ParameterSet& iConfig):
    fSrc(iConfig.getParameter<edm::InputTag>("src")),
    fPatTriggerSrc(iConfig.getParameter<edm::InputTag>("patTriggerEventSrc")),
    fDeltaR(iConfig.getParameter<double>("deltaR")),
    fFilterNames(iConfig.getParameter<std::vector<std::string> >("filterNames"))
  {
    produces<std::vector<T> >();
  }

  template <typename T>
  PATTriggerMatchSelector<T>::~PATTriggerMatchSelector() {}

  template <typename T>
  void PATTriggerMatchSelector<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<T> > hcands;
    iEvent.getByLabel(fSrc, hcands);

    edm::Handle<pat::TriggerEvent> htrigger;
    iEvent.getByLabel(fPatTriggerSrc, htrigger);

    pat::TriggerObjectRefVector filterObjects;
    for(size_t i=0; i<fFilterNames.size(); ++i) {
      pat::TriggerObjectRefVector tmp = htrigger->filterObjects(fFilterNames[i]);
      std::copy(tmp.begin(), tmp.end(), std::back_inserter(filterObjects));
    }

    std::auto_ptr<std::vector<T> > result(new std::vector<T>());
    for(size_t iCand = 0; iCand < hcands->size(); ++iCand) {
      bool match = false;
      for(size_t iTrigger =0; iTrigger < filterObjects.size(); ++iTrigger) {
        if(reco::deltaR(hcands->at(iCand), *(filterObjects[iTrigger])) < fDeltaR) {
          match = true;
          break;
        }
      }
      if(match) {
        T copy = hcands->at(iCand);
        result->push_back(copy);
      }
    }

    iEvent.put(result);
  }
}

typedef PATTriggerMatchSelector<pat::Tau> HPlusTauTriggerMatchSelector;
DEFINE_FWK_MODULE(HPlusTauTriggerMatchSelector);

typedef PATTriggerMatchSelector<pat::Muon> HPlusMuonTriggerMatchSelector;
DEFINE_FWK_MODULE(HPlusMuonTriggerMatchSelector);
