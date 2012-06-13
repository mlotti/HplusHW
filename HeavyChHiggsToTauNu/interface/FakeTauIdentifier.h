// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_FakeTauIdentifier_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_FakeTauIdentifier_h

namespace edm {
  class Event;
}

namespace reco {
  class Candidate;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

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

    FakeTauIdentifier(HistoWrapper& histoWrapper, std::string label);
    ~FakeTauIdentifier();
    
    MCSelectedTauMatchType matchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau);
    bool isFakeTau(MCSelectedTauMatchType type) { return !(type == kkTauToTau || type == kkTauToTauAndTauOutsideAcceptance); }
    
  private:
    WrappedTH1* hTauMatchType;
    WrappedTH1* hTauOrigin;
    WrappedTH1* hMuOrigin;
    WrappedTH1* hElectronOrigin;
  };
}

#endif
