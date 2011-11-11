// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_FakeTauIdentifier_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_FakeTauIdentifier_h


//#include "DataFormats/Common/interface/Ptr.h"
//#include "DataFormats/PatCandidates/interface/Tau.h"



namespace edm {
  class Event;
}

namespace reco {
  class Candidate;
}

namespace HPlus {
  class FakeTauIdentifier {
  public:
    enum MCSelectedTauMatchType {
      kkElectronToTau,
      kkMuonToTau,
      kkTauToTau,
      kkJetToTau,
      kkNoMC,
      kkElectronToTauAndTauOutsideAcceptance,
      kkMuonToTauAndTauOutsideAcceptance,
      kkTauToTauAndTauOutsideAcceptance,
      kkJetToTauAndTauOutsideAcceptance
    };

    static MCSelectedTauMatchType matchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau);
    static bool isFakeTau(MCSelectedTauMatchType type) { return !(type == kkTauToTau || type == kkTauToTauAndTauOutsideAcceptance); }
    
  };
}

#endif
