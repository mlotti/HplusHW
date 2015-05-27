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
      kkElectronToTauAndTauJetInsideAcceptance,
      kkElectronFromTauDecayToTauAndTauJetInsideAcceptance,
      kkMuonToTauAndTauJetInsideAcceptance,
      kkMuonFromTauDecayToTauAndTauJetInsideAcceptance,
      kkTauToTauAndTauJetInsideAcceptance,
      kkOneProngTauToTauAndTauJetInsideAcceptance,
      kkJetToTauAndTauJetInsideAcceptance,
      kkNumberOfSelectedTauMatchTypes
    };
    enum MCSelectedTauOriginType {
      kkUnknownOrigin = 0,
      kkFromW,
      kkFromZ,
      kkFromHplus,
      kkFromWTau,
      kkFromZTauTau,
      kkFromHplusTau
    };
    enum MCBackgroundType {
      kkUnknown = 0,
      kkEWKFakeTauLike, // e/mu/jet -> identified tau, identified tau matches to visible tau lepton, tau lepton(s) in accepance
      kkEmbeddingLikeSingleTauInAcceptance, // genuine tau identified, matches to vis. tau lepton, one tau lepton in accepance
      kkEmbeddingLikeMultipleTausInAcceptance // genuine tau identified, matches to vis. tau lepton, more than one tau lepton in accepance
    };
    class Data {
    public:
      Data();
      ~Data();

      const MCSelectedTauMatchType getTauMatchType() const { return fTauMatchType; }
      const MCSelectedTauOriginType getTauOriginType() const { return fTauOriginType; }
      const reco::GenParticle *getTauMatchGenParticle() const { return fTauMatchGenParticle; }
      const bool isFakeTau() const { return FakeTauIdentifier::isFakeTau(fTauMatchType); }
      const bool isGenuineTau() const { return FakeTauIdentifier::isGenuineTau(fTauMatchType); }
      const bool isGenuineOneProngTau() const { return FakeTauIdentifier::isGenuineOneProngTau(fTauMatchType); }

      //const double getFakeTauScaleFactor(double eta) const;
      //const double getFakeTauSystematics(double eta) const;

      const bool isElectronToTau() const { return FakeTauIdentifier::isElectronToTau(fTauMatchType); }
      const bool isMuonToTau() const { return FakeTauIdentifier::isMuonToTau(fTauMatchType); }
      const bool isJetToTau() const { return FakeTauIdentifier::isJetToTau(fTauMatchType); }
      const bool isElectronOrMuonFromTauDecay() const { return FakeTauIdentifier::isElectronOrMuonFromTauDecay(fTauMatchType); }

      const MCBackgroundType getBackgroundType() const { return fBackgroundType; }
      const bool isEWKFakeTauLike() const { return fBackgroundType == kkEWKFakeTauLike; }
      const bool isEmbeddingGenuineTauLike() const { return isEmbeddingGenuineTauLikeWithSingleTauInAcceptance() || isEmbeddingGenuineTauLikeWithMultipleTausInAcceptance(); }
      const bool isEmbeddingGenuineTauLikeWithSingleTauInAcceptance() const { return fBackgroundType == kkEmbeddingLikeSingleTauInAcceptance; }
      const bool isEmbeddingGenuineTauLikeWithMultipleTausInAcceptance() const { return fBackgroundType == kkEmbeddingLikeMultipleTausInAcceptance; }

      friend class FakeTauIdentifier;

    private:
      MCSelectedTauMatchType fTauMatchType;
      MCSelectedTauOriginType fTauOriginType;
      MCBackgroundType fBackgroundType;
      const reco::GenParticle *fTauMatchGenParticle;
    };

    FakeTauIdentifier(const edm::ParameterSet& iConfig, const edm::ParameterSet& tauIDConfig,HistoWrapper& histoWrapper, std::string label);
    ~FakeTauIdentifier();

    Data matchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau);
    Data silentMatchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau);
    static const bool isFakeTau(MCSelectedTauMatchType type) { return !isGenuineTau(type); }
    static const bool isGenuineTau(MCSelectedTauMatchType type) { return (type == kkTauToTau || type == kkTauToTauAndTauJetInsideAcceptance || isGenuineOneProngTau(type)); }
    static const bool isGenuineOneProngTau(MCSelectedTauMatchType type) { return (type == kkOneProngTauToTau || type == kkOneProngTauToTauAndTauJetInsideAcceptance); }

    double getFakeTauScaleFactor(MCSelectedTauMatchType matchType, double eta);
    double getFakeTauSystematics(MCSelectedTauMatchType matchType, double eta);

    static const bool isElectronToTau(MCSelectedTauMatchType type) { return (type == kkElectronToTau || type == kkElectronFromTauDecayToTau ||
      type == kkElectronToTauAndTauJetInsideAcceptance || type == kkElectronFromTauDecayToTauAndTauJetInsideAcceptance); }
    static const bool isMuonToTau(MCSelectedTauMatchType type) { return (type == kkMuonToTau || type == kkMuonFromTauDecayToTau ||
      type == kkMuonToTauAndTauJetInsideAcceptance || type == kkMuonFromTauDecayToTauAndTauJetInsideAcceptance); }
    static const bool isJetToTau(MCSelectedTauMatchType type) { return (type == kkJetToTau || type == kkJetToTauAndTauJetInsideAcceptance); }
    static const bool isElectronOrMuonFromTauDecay(MCSelectedTauMatchType type) { return (type == kkElectronFromTauDecayToTau || type == kkElectronToTauAndTauJetInsideAcceptance ||
      type == kkMuonFromTauDecayToTau || type == kkMuonFromTauDecayToTauAndTauJetInsideAcceptance); }

  private:
    Data privateMatchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau, bool silentMode);

    edm::InputTag fVisibleMCTauSrc;
    edm::InputTag fVisibleMCTauOneProngSrc;
    const double fMatchingConditionDeltaR;
    // Scale factors for tau ID and X->tau fakes mis-ID
    const double fSFGenuineTauBarrel;
    const double fSFGenuineTauEndcap;
    const double fSFFakeTauBarrelElectron;
    const double fSFFakeTauEndcapElectron;
    const double fSFFakeTauBarrelMuon;
    const double fSFFakeTauEndcapMuon;
    const double fSFFakeTauBarrelJet;
    const double fSFFakeTauEndcapJet;
    // Systematic uncertainties for tau ID and X->tau fakes mis-ID
    const double fSystematicsGenuineTauBarrel;
    const double fSystematicsGenuineTauEndcap;
    const double fSystematicsFakeTauBarrelElectron;
    const double fSystematicsFakeTauEndcapElectron;
    const double fSystematicsFakeTauBarrelMuon;
    const double fSystematicsFakeTauEndcapMuon;
    const double fSystematicsFakeTauBarrelJet;
    const double fSystematicsFakeTauEndcapJet;
    // Cut values for acceptance (taken from tau ID config)
    const double fPtAcceptance;
    const double fEtaAcceptance;

    WrappedTH1* hTauMatchType;
    WrappedTH1* hTauOrigin;
    WrappedTH1* hMuOrigin;
    WrappedTH1* hElectronOrigin;
  };
}

#endif
