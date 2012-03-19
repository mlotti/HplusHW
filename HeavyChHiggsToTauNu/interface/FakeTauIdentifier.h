// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_FakeTauIdentifier_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_FakeTauIdentifier_h

#include "HiggsAnalysis/HeavyChHiggsToTauNu/interface/EventWeight.h"

#include "TH1F.h"


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
      kkNoMC,
      kkElectronToTau,
      kkMuonToTau,
      kkTauToTau,
      kkJetToTau,
      kkElectronToTauAndTauOutsideAcceptance,
      kkMuonToTauAndTauOutsideAcceptance,
      kkTauToTauAndTauOutsideAcceptance,
      kkJetToTauAndTauOutsideAcceptance
    };
    enum MCSelectedTauOriginType {
      kkUnknownOrigin,
      kkFromW,
      kkFromZ,
      kkFromHplus,
      kkFromWTau,
      kkFromZTauTau,
      kkFromHplusTau
    };

    FakeTauIdentifier(EventWeight& eventWeight, std::string label);
    ~FakeTauIdentifier();
    
    MCSelectedTauMatchType matchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau);
    bool isFakeTau(MCSelectedTauMatchType type) { return !(type == kkTauToTau || type == kkTauToTauAndTauOutsideAcceptance); }
    
  private:
    EventWeight& fEventWeight;
    
    TH1* hTauMatchType;
    TH1* hTauOrigin;
    TH1* hMuOrigin;
    TH1* hElectronOrigin;
  };
}

#endif
