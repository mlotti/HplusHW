// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_CandViewClosestDeltaRSelector_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_CandViewClosestDeltaRSelector_h

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "DataFormats/Math/interface/deltaR.h"

//#include<iostream>

namespace hplus {
  template <typename T>
  class CandViewClosestDeltaRSelector: public edm::EDProducer {
  public:
    explicit CandViewClosestDeltaRSelector(const edm::ParameterSet&);
    ~CandViewClosestDeltaRSelector();

  private:
    typedef std::vector<T> CollectionType;

    virtual void produce(edm::Event&, const edm::EventSetup&);

    edm::InputTag srcCand_;
    edm::InputTag srcRef_;
    const double maxDR_;
  };

  template <typename T>
  CandViewClosestDeltaRSelector<T>::CandViewClosestDeltaRSelector(const edm::ParameterSet& iConfig):
    srcCand_(iConfig.getParameter<edm::InputTag>("src")),
    srcRef_(iConfig.getParameter<edm::InputTag>("refSrc")),
    maxDR_(iConfig.getParameter<double>("maxDeltaR"))
  {
    this->template produces<CollectionType>();
  }

  template <typename T>
  CandViewClosestDeltaRSelector<T>::~CandViewClosestDeltaRSelector() {}

  template <typename T>
  void CandViewClosestDeltaRSelector<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<T> > hcand;
    iEvent.getByLabel(srcCand_, hcand);

    edm::Handle<edm::View<reco::Candidate> > href;
    iEvent.getByLabel(srcRef_, href);

    std::auto_ptr<CollectionType> ret(new CollectionType());

    // The ordering is important, it is employed in the embedding validation
    // I.e. the order of selected T objects should match to the order of reference candidates
    for(edm::View<reco::Candidate>::const_iterator iRef = href->begin(); iRef != href->end(); ++iRef) {
      typename edm::View<T>::const_iterator iSel = hcand->end();
      double selDR = maxDR_;
      for(typename edm::View<T>::const_iterator iCand = hcand->begin(); iCand != hcand->end(); ++iCand) {
        double DR = reco::deltaR(*iCand, *iRef);
        if(DR < selDR) {
          selDR = DR;
          iSel = iCand;
        }
      }
      if(iSel != hcand->end()) {
        /*
        std::cout << "Reference object " << (iRef-href->begin()) << " pt " << iRef->pt() << " eta " << iRef->eta()
                  << " selected object " << (iSel-hcand->end()) << " pt " << iSel->pt() << " eta " << iSel->eta()
                  << std::endl;
        */
        ret->push_back(*iSel);
      }
    }

    //std::cout << "Inserting " << ret->size() << " objects" << std::endl;
    iEvent.put(ret);

  }
}



#endif
