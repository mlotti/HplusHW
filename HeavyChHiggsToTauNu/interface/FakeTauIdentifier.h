// -*- c++ -*-
#ifndef HiggsAnalysis_HeavyChHiggsToTauNu_FakeTauIdentifier_h
#define HiggsAnalysis_HeavyChHiggsToTauNu_FakeTauIdentifier_h

#include "FWCore/Utilities/interface/InputTag.h"

#include <string>

namespace edm {
  class Event;
  class ParameterSet;
}

namespace reco {
  class Candidate;
  class GenParticle;
}

namespace HPlus {
  class HistoWrapper;
  class WrappedTH1;

  class FakeTauIdentifier {
  public:
    enum MCSelectedTauMatchType {
      kkNoMC = 0,
      kkElectronToTau,
      kkElectronFromTauDecayToTau,
      kkMuonToTau,
      kkMuonFromTauDecayToTau,
      kkTauToTau,
      kkOneProngTauToTau,
      kkJetToTau,
      kkElectronToTauAndTauOutsideAcceptance,
      kkElectronFromTauDecayToTauAndTauOutsideAcceptance,
      kkMuonToTauAndTauOutsideAcceptance,
      kkMuonFromTauDecayToTauAndTauOutsideAcceptance,
      kkTauToTauAndTauOutsideAcceptance,
      kkOneProngTauToTauAndTauOutsideAcceptance,
      kkJetToTauAndTauOutsideAcceptance,
      kkNumberOfSelectedTauMatchTypes
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

    class Data {
    public:
      Data();
      ~Data();

      MCSelectedTauMatchType getTauMatchType() const { return fTauMatchType; }
      MCSelectedTauOriginType getTauOriginType() const { return fTauOriginType; }
      const reco::GenParticle *getTauMatchGenParticle() const { return fTauMatchGenParticle; }

      friend class FakeTauIdentifier;

    private:
      MCSelectedTauMatchType fTauMatchType;
      MCSelectedTauOriginType fTauOriginType;
      const reco::GenParticle *fTauMatchGenParticle;
    };

    FakeTauIdentifier(const edm::ParameterSet& iConfig, HistoWrapper& histoWrapper, std::string label);
    ~FakeTauIdentifier();

    Data matchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau);
    Data silentMatchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau);
    bool isFakeTau(MCSelectedTauMatchType type) { return !isGenuineTau(type); }
    bool isGenuineTau(MCSelectedTauMatchType type) { return (type == kkTauToTau || type == kkTauToTauAndTauOutsideAcceptance || isGenuineOneProngTau(type)); }
    bool isGenuineOneProngTau(MCSelectedTauMatchType type) { return (type == kkOneProngTauToTau || type == kkOneProngTauToTauAndTauOutsideAcceptance); }
    
    double getFakeTauScaleFactor(MCSelectedTauMatchType matchType, double eta);
    double getFakeTauSystematics(MCSelectedTauMatchType matchType, double eta);

    bool isElectronToTau(MCSelectedTauMatchType type) { return (type == kkElectronToTau || type == kkElectronFromTauDecayToTau ||
      type == kkElectronToTauAndTauOutsideAcceptance || type == kkElectronFromTauDecayToTauAndTauOutsideAcceptance); }
    bool isMuonToTau(MCSelectedTauMatchType type) { return (type == kkMuonToTau || type == kkMuonFromTauDecayToTau ||
      type == kkMuonToTauAndTauOutsideAcceptance || type == kkMuonFromTauDecayToTauAndTauOutsideAcceptance); }
    bool isJetToTau(MCSelectedTauMatchType type) { return (type == kkJetToTau || type == kkJetToTauAndTauOutsideAcceptance); }
    bool isElectronOrMuonFromTauDecay(MCSelectedTauMatchType type) { return (type == kkElectronFromTauDecayToTau || type == kkElectronToTauAndTauOutsideAcceptance ||
      type == kkMuonFromTauDecayToTau || type == kkMuonFromTauDecayToTauAndTauOutsideAcceptance); }

    bool isEmbeddingGenuineTau(MCSelectedTauMatchType type) { return (!isFakeTau(type) || isElectronOrMuonFromTauDecay(type)); }

  private:
    Data privateMatchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau, bool silentMode);
    
    edm::InputTag fVisibleMCTauSrc;
    edm::InputTag fVisibleMCTauOneProngSrc;
    const double fMatchingConditionDeltaR;
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
