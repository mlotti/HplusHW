// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_ViewClosestDeltaRSelector_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_ViewClosestDeltaRSelector_h

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/Math/interface/deltaR.h"

//#include<iostream>
#include<string>

namespace HPlus {
  template <typename CandType, typename RefType>
  class ViewClosestDeltaRSelector: public edm::EDProducer {
  public:
    explicit ViewClosestDeltaRSelector(const edm::ParameterSet&);
    ~ViewClosestDeltaRSelector();

  private:
    typedef std::vector<CandType> CollectionType;

    virtual void produce(edm::Event&, const edm::EventSetup&);

    edm::InputTag srcCand_;
    edm::InputTag srcRef_;
    std::string moduleLabel_;
    const double maxDR_;
  };

  template <typename CandType, typename RefType>
  ViewClosestDeltaRSelector<CandType, RefType>::ViewClosestDeltaRSelector(const edm::ParameterSet& iConfig):
    srcCand_(iConfig.getParameter<edm::InputTag>("src")),
    srcRef_(iConfig.getParameter<edm::InputTag>("refSrc")),
    moduleLabel_(iConfig.getParameter<std::string>("@module_label")),
    maxDR_(iConfig.getParameter<double>("maxDeltaR"))
  {
    this->template produces<CollectionType>();
  }

  template <typename CandType, typename RefType>
  ViewClosestDeltaRSelector<CandType, RefType>::~ViewClosestDeltaRSelector() {}

  template <typename CandType, typename RefType>
  void ViewClosestDeltaRSelector<CandType, RefType>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<CandType> > hcand;
    iEvent.getByLabel(srcCand_, hcand);

    edm::Handle<edm::View<RefType> > href;
    iEvent.getByLabel(srcRef_, href);

    std::auto_ptr<CollectionType> ret(new CollectionType());

    // The ordering is important, it is employed in the embedding validation
    // I.e. the order of selected CandType objects should match to the order of reference candidates
    for(typename edm::View<RefType>::const_iterator iRef = href->begin(); iRef != href->end(); ++iRef) {
      typename edm::View<CandType>::const_iterator iSel = hcand->end();
      double selDR = maxDR_;
      for(typename edm::View<CandType>::const_iterator iCand = hcand->begin(); iCand != hcand->end(); ++iCand) {
        double DR = reco::deltaR(*iCand, *iRef);
        if(DR < selDR) {
          selDR = DR;
          iSel = iCand;
        }
      }
      if(iSel != hcand->end()) {
        /*
        std::cout << moduleLabel_ << ": Reference object " << (iRef-href->begin()) << " (pt,eta,phi) " << iRef->pt() << ", " << iRef->eta() << ", " << iRef->phi()
                  << ") selected object " << (iSel-hcand->begin()) << " (pt,eta,phi) " << iSel->pt() << ", " << iSel->eta() << ", " << iSel->phi()
                  << ") deltaR " << selDR
                  << std::endl;
        */
        ret->push_back(*iSel);
      }
    }

    //std::cout << moduleLabel_ << ": Inserting " << ret->size() << " objects" << std::endl;
    iEvent.put(ret);

  }
}



#endif
