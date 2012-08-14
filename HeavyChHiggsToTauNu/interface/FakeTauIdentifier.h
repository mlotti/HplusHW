// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_FakeTauIdentifier_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_FakeTauIdentifier_h

#include <string>

namespace edm {
  class Event;
  class ParameterSet;
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

    FakeTauIdentifier(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper, std::string label);
    ~FakeTauIdentifier();

    MCSelectedTauMatchType matchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau);
    bool isFakeTau(MCSelectedTauMatchType type) { return !(type == kkTauToTau || type == kkTauToTauAndTauOutsideAcceptance); }

    double getFakeTauScaleFactor(MCSelectedTauMatchType matchType, double eta);
    double getFakeTauSystematics(MCSelectedTauMatchType matchType, double eta);

  private:
    // Scale factors for X->tau fakes
    const double fSFFakeTauBarrelElectron;
    const double fSFFakeTauEndcapElectron;
    const double fSFFakeTauBarrelMuon;
    const double fSFFakeTauEndcapMuon;
    const double fSFFakeTauBarrelJet;
    const double fSFFakeTauEndcapJet;
    // Systematic uncertainties for X->tau fakes
    const double fSystematicsFakeTauBarrelElectron;
    const double fSystematicsFakeTauEndcapElectron;
    const double fSystematicsFakeTauBarrelMuon;
    const double fSystematicsFakeTauEndcapMuon;
    const double fSystematicsFakeTauBarrelJet;
    const double fSystematicsFakeTauEndcapJet;

    WrappedTH1* hTauMatchType;
    WrappedTH1* hTauOrigin;
    WrappedTH1* hMuOrigin;
    WrappedTH1* hElectronOrigin;
  };
}

#endif
