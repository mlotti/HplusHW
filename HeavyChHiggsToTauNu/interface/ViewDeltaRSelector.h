// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ViewDeltaRSelector_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ViewDeltaRSelector_h

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "DataFormats/Math/interface/deltaR.h"


namespace HPlus {
  template <typename CandType, typename RefType>
  class ViewDeltaRSelector: public edm::EDProducer {
  public:
    explicit ViewDeltaRSelector(const edm::ParameterSet&);
    ~ViewDeltaRSelector();

  private:
    typedef std::vector<CandType> CollectionType;

    virtual void produce(edm::Event&, const edm::EventSetup&);

    edm::InputTag srcCand_;
    edm::InputTag srcRef_;
    const double maxDR_;
  };

  template <typename CandType, typename RefType>
  ViewDeltaRSelector<CandType, RefType>::ViewDeltaRSelector(const edm::ParameterSet& iConfig):
    srcCand_(iConfig.getParameter<edm::InputTag>("src")),
    srcRef_(iConfig.getParameter<edm::InputTag>("refSrc")),
    maxDR_(iConfig.getParameter<double>("deltaR"))
  {
    this->template produces<CollectionType>();
  }

  template <typename CandType, typename RefType>
  ViewDeltaRSelector<CandType, RefType>::~ViewDeltaRSelector() {}

  template <typename CandType, typename RefType>
  void ViewDeltaRSelector<CandType, RefType>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<CandType> > hcand;
    iEvent.getByLabel(srcCand_, hcand);

    edm::Handle<edm::View<RefType> > href;
    iEvent.getByLabel(srcRef_, href);

    std::auto_ptr<CollectionType> ret(new CollectionType());

    for(typename edm::View<CandType>::const_iterator iCand = hcand->begin(); iCand != hcand->end(); ++iCand) {
      for(edm::View<reco::Candidate>::const_iterator iRef = href->begin(); iRef != href->end(); ++iRef) {
        if(reco::deltaR(*iCand, *iRef) < maxDR_) {
          ret->push_back(*iCand);
        }
      }
    }
  
    iEvent.put(ret);

  }
}



#endif
