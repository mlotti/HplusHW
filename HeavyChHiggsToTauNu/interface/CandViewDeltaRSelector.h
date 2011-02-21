// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_CandViewDeltaRSelector_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_CandViewDeltaRSelector_h

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"

#include "DataFormats/Math/interface/deltaR.h"


namespace hplus {
  template <typename T>
  class CandViewDeltaRSelector: public edm::EDProducer {
  public:
    explicit CandViewDeltaRSelector(const edm::ParameterSet&);
    ~CandViewDeltaRSelector();

  private:
    typedef std::vector<T> CollectionType;

    virtual void produce(edm::Event&, const edm::EventSetup&);

    edm::InputTag srcCand_;
    edm::InputTag srcRef_;
    const double maxDR_;
  };

  template <typename T>
  CandViewDeltaRSelector<T>::CandViewDeltaRSelector(const edm::ParameterSet& iConfig):
    srcCand_(iConfig.getParameter<edm::InputTag>("src")),
    srcRef_(iConfig.getParameter<edm::InputTag>("refSrc")),
    maxDR_(iConfig.getParameter<double>("deltaR"))
  {
    this->template produces<CollectionType>();
  }

  template <typename T>
  CandViewDeltaRSelector<T>::~CandViewDeltaRSelector() {}

  template <typename T>
  void CandViewDeltaRSelector<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle<edm::View<T> > hcand;
    iEvent.getByLabel(srcCand_, hcand);

    edm::Handle<edm::View<reco::Candidate> > href;
    iEvent.getByLabel(srcRef_, href);

    std::auto_ptr<CollectionType> ret(new CollectionType());

    for(typename edm::View<T>::const_iterator iCand = hcand->begin(); iCand != hcand->end(); ++iCand) {
      for(edm::View<reco::Candidate>::const_iterator iRef = href->begin(); iRef != href->end(); ++iRef) {
        if(reco::deltaR(*iCand, *iRef) < maxDR_) {
          ret->push_back(*iCand);
          break;
        }
      }
    }
  
    iEvent.put(ret);

  }
}



#endif
