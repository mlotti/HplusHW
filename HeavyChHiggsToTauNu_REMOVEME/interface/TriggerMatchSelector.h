// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_TriggerMatchSelector_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_TriggerMatchSelector_h

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "CommonTools/UtilAlgos/interface/SelectionAdderTrait.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/TriggerObject.h"

#include "DataFormats/Math/interface/deltaR.h"

#include<algorithm>

namespace HPlus {
  template <typename InputCollection,
            typename OutputCollection = typename helper::SelectedOutputCollectionTrait<InputCollection>::type,
            typename RefAdder = typename helper::SelectionAdderTrait<InputCollection, OutputCollection>::type>
  class TriggerMatchSelector: public edm::EDProducer {
    typedef const typename InputCollection::value_type * reference;
    typedef std::pair<reference, size_t> pair;

  public:
    explicit TriggerMatchSelector(const edm::ParameterSet& iConfig):
      fCandSrc(iConfig.getParameter<edm::InputTag>("src")),
      fPatTriggerSrc(iConfig.getParameter<edm::InputTag>("patTriggerEventSrc")),
      fDeltaR(iConfig.getParameter<double>("deltaR")),
      fFilterNames(iConfig.getParameter<std::vector<std::string> >("filterNames"))
    {
      produces<OutputCollection>();
    }

    ~TriggerMatchSelector() {}

    virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
      edm::Handle<InputCollection> hcands;
      iEvent.getByLabel(fCandSrc, hcands);

      edm::Handle<pat::TriggerEvent> htrigger;
      iEvent.getByLabel(fPatTriggerSrc, htrigger);

      pat::TriggerObjectRefVector filterObjects;
      for(size_t i=0; i<fFilterNames.size(); ++i) {
        pat::TriggerObjectRefVector tmp = htrigger->filterObjects(fFilterNames[i]);
        std::copy(tmp.begin(), tmp.end(), std::back_inserter(filterObjects));
      }

      std::auto_ptr<OutputCollection> result(new OutputCollection());
      for(size_t iCand = 0; iCand < hcands->size(); ++iCand) {
        bool match = false;
        for(size_t iTrigger =0; iTrigger < filterObjects.size(); ++iTrigger) {
          if(reco::deltaR(hcands->at(iCand), *(filterObjects[iTrigger])) < fDeltaR) {
            match = true;
            break;
          }
        }
        if(match)
          addRef_(*result, hcands, iCand);
      }
      iEvent.put(result);
    }


    edm::InputTag fCandSrc;
    edm::InputTag fPatTriggerSrc;
    double fDeltaR;
    std::vector<std::string> fFilterNames;

    RefAdder addRef_;
  };
}

#endif
