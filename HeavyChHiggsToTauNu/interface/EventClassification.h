// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_EventClassification_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_EventClassification_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/BaseSelection.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventCounter.h"

#include "FWCore/Framework/interface/Event.h"


namespace edm {
  class Event;
  class ParameterSet;
  class EventSetup;
}

namespace reco {
  class Candidate;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  void checkIfGenuineTau(const edm::Event& iEvent, const edm::Ptr<pat::Tau>& tau);
  // Alternative way
  //void checkIfGenuineTau(const edm::Event& iEvent, const reco::Candidate&tau);
}

/*   class EventClassification: public BaseSelection { */
/*   public: */
/*     class Data { */
/*     public: */

/*       Data(); */
/*       Data(const GenParticle *analysis); */
/*       ~Data(); */

/*       void check() const; */

/*       const edm::Ptr<reco::GenMET>& getGenMET() const { */
/*         check(); */
/*         return fAnalysis->fGenMet; */
/*       } */
/*     private: */
/*       const GenParticleAnalysis *fAnalysis; */
/*     }; */

#endif
