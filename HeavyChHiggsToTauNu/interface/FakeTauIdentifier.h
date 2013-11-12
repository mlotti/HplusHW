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

      const bool isEmbeddingGenuineTau() const { return FakeTauIdentifier::isEmbeddingGenuineTau(fTauMatchType); }

      friend class FakeTauIdentifier;

    private:
      MCSelectedTauMatchType fTauMatchType;
      MCSelectedTauOriginType fTauOriginType;
      const reco::GenParticle *fTauMatchGenParticle;
    };

    FakeTauIdentifier(const edm::ParameterSet& iConfig, const edm::ParameterSet& tauIDConfig,HistoWrapper& histoWrapper, std::string label);
    ~FakeTauIdentifier();

    Data matchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau);
    Data silentMatchTauToMC(const edm::Event& iEvent, const reco::Candidate& tau);
    static const bool isFakeTau(MCSelectedTauMatchType type) { return !isGenuineTau(type); }
    static const bool isGenuineTau(MCSelectedTauMatchType type) { return (type == kkTauToTau || type == kkTauToTauAndTauOutsideAcceptance || isGenuineOneProngTau(type)); }
    static const bool isGenuineOneProngTau(MCSelectedTauMatchType type) { return (type == kkOneProngTauToTau || type == kkOneProngTauToTauAndTauOutsideAcceptance); }

    double getFakeTauScaleFactor(MCSelectedTauMatchType matchType, double eta);
    double getFakeTauSystematics(MCSelectedTauMatchType matchType, double eta);

    static const bool isElectronToTau(MCSelectedTauMatchType type) { return (type == kkElectronToTau || type == kkElectronFromTauDecayToTau ||
      type == kkElectronToTauAndTauOutsideAcceptance || type == kkElectronFromTauDecayToTauAndTauOutsideAcceptance); }
    static const bool isMuonToTau(MCSelectedTauMatchType type) { return (type == kkMuonToTau || type == kkMuonFromTauDecayToTau ||
      type == kkMuonToTauAndTauOutsideAcceptance || type == kkMuonFromTauDecayToTauAndTauOutsideAcceptance); }
    static const bool isJetToTau(MCSelectedTauMatchType type) { return (type == kkJetToTau || type == kkJetToTauAndTauOutsideAcceptance); }
    static const bool isElectronOrMuonFromTauDecay(MCSelectedTauMatchType type) { return (type == kkElectronFromTauDecayToTau || type == kkElectronToTauAndTauOutsideAcceptance ||
      type == kkMuonFromTauDecayToTau || type == kkMuonFromTauDecayToTauAndTauOutsideAcceptance); }
    // For embedding, consider events where selected tau is hadronic tau and there is no second tau LEPTON in acceptance
    static const bool isEmbeddingGenuineTau(MCSelectedTauMatchType type) { return type == kkTauToTau; }

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
