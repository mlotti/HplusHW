// -*- c++ -*-
#ifndef __BRANCHES__
#define __BRANCHES__

#include "BaseSelector.h"

#include "TTree.h"
#include "TBranch.h"
#include "Rtypes.h"
#include "Math/LorentzVector.h"
#include "Math/DisplacementVector3D.h"

#include<string>
#include<vector>

// From DataFormats/Math/interface/LorentzVector.h
namespace math {
  typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > XYZTLorentzVectorD;
  typedef XYZTLorentzVectorD XYZTLorentzVector;

  typedef ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<double> > XYZVectorD;
  typedef XYZVectorD XYZVector;
}

// Event information
class EventInfo {
public:
  EventInfo();
  ~EventInfo();

  void setupBranches(BranchManager& branchManager);

  unsigned event() { return fEvent->value(); }
  unsigned lumi() { return fLumi->value(); }
  unsigned run() { return fRun->value(); }

private:
  Branch<unsigned> *fEvent;
  Branch<unsigned> *fLumi;
  Branch<unsigned> *fRun;
};

namespace Impl {
  class ParticleBase {
  public:
    ParticleBase();
    explicit ParticleBase(size_t i): fIndex(i), fP4Set(false) {}
    ~ParticleBase();

    size_t index() const { return fIndex; }
    void setP4(const math::XYZTLorentzVector& p4_) {
      fP4 = p4_;
      fP4Set = true;
    }

  protected:
    const math::XYZTLorentzVector& getP4() const { return fP4; }
    bool isP4Set() const { return fP4Set; }

  private:
    math::XYZTLorentzVector fP4;
    size_t fIndex;
    bool fP4Set;
  };

  template <typename T>
  class Particle: public ParticleBase {
  public:
    Particle(): ParticleBase(), fCollection(0) {}
    Particle(T *coll, size_t i): ParticleBase(i), fCollection(coll) {}
    ~Particle() {}

    bool isValid() const { return fCollection != 0; }

    const math::XYZTLorentzVector& p4() {
      if(isP4Set())
        return getP4();
      else
        return originalP4();
    }

    const math::XYZTLorentzVector& originalP4() {
      return fCollection->fP4->value()[index()];
    }

  protected:
    T *fCollection;
  };
}

// Muons
class MuonCollection {
public:
  class Muon: public Impl::Particle<MuonCollection> {
    typedef Impl::Particle<MuonCollection> Base;
  public:
    enum CorrectionType {
      kUncorrected,
      kCorrected,
      kTuneP,
    };

    Muon(): Base(), fCorrectionType(kUncorrected) {}
    Muon(MuonCollection *mc, size_t i): Base(mc, i), fCorrectionType(kUncorrected) {}
    ~Muon();

    void ensureValidity() const;

    void assignP4();
    CorrectionType p4CorrectionType() const { return fCorrectionType; }

    const math::XYZTLorentzVector& correctedP4() { return fCollection->fCorrectedP4->value()[index()]; }

    const math::XYZVector& tunePP3() { return fCollection->fTunePP3->value()[index()]; }
    double tunePPtError() { return fCollection->fTunePPtError->value()[index()]; }

    int charge() { return fCollection->fCharge->value()[index()]; }
    double normalizedChi2() { return fCollection->fNormalizedChi2->value()[index()]; }
    double dB() { return fCollection->fDB->value()[index()]; }

    double trackIso() { return fCollection->fTrackIso->value()[index()]; }
    double caloIso() { return fCollection->fCaloIso->value()[index()]; }

    double chargedHadronIso() { return fCollection->fChargedHadronIso->value()[index()]; }
    double puChargedHadronIso() { return fCollection->fPuChargedHadronIso->value()[index()]; }
    double neutralHadronIso() { return fCollection->fNeutralHadronIso->value()[index()]; }
    double photonIso() { return fCollection->fPhotonIso->value()[index()]; }

    double idEfficiency() { return fCollection->fIdEfficiency->value()[index()]; }
    double triggerEfficiency() { return fCollection->fTriggerEfficiency->value()[index()]; }

    bool triggerMatched() { return fCollection->fTriggerMatched->value()[index()]; }

    const math::XYZTLorentzVector& genMatchP4() { return fCollection->fGenMatchP4->value()[index()]; }
    int pdgId() { return fCollection->fPdgId->value()[index()]; }
    int motherPdgId() { return fCollection->fMotherPdgId->value()[index()]; }
    int grandMotherPdgId() { return fCollection->fGrandMotherPdgId->value()[index()]; }

  private:
    CorrectionType fCorrectionType;
  };


  MuonCollection(const std::string prefix = "muons");
  ~MuonCollection();

  void setIdEfficiencyName(const std::string& idEff) { fIdEfficiencyName = idEff; }
  void setTriggerEfficiencyName(const std::string& trigEff) { fTriggerEfficiencyName = trigEff; }

  void setupBranches(BranchManager& branchManager, bool isMC);
  size_t size() {
    return fP4->value().size();
  }
  Muon get(size_t i) {
    return Muon(this, i);
  }

protected:
  std::string fPrefix;

private:
  std::string fIdEfficiencyName;
  std::string fTriggerEfficiencyName;

  Branch<std::vector<math::XYZTLorentzVector> > *fP4;
  Branch<std::vector<math::XYZTLorentzVector> > *fCorrectedP4;

  Branch<std::vector<math::XYZVector> > *fTunePP3;
  Branch<std::vector<double> > *fTunePPtError;

  Branch<std::vector<int> > *fCharge;
  Branch<std::vector<double> > *fDB;
  Branch<std::vector<double> > *fNormalizedChi2;

  Branch<std::vector<double> > *fTrackIso;
  Branch<std::vector<double> > *fCaloIso;

  Branch<std::vector<double> > *fChargedHadronIso;
  Branch<std::vector<double> > *fPuChargedHadronIso;
  Branch<std::vector<double> > *fNeutralHadronIso;
  Branch<std::vector<double> > *fPhotonIso;

  Branch<std::vector<double> > *fIdEfficiency;
  Branch<std::vector<double> > *fTriggerEfficiency;

  Branch<std::vector<bool> > *fTriggerMatched;

  Branch<std::vector<math::XYZTLorentzVector> > *fGenMatchP4;
  Branch<std::vector<int> > *fPdgId;
  Branch<std::vector<int> > *fMotherPdgId;
  Branch<std::vector<int> > *fGrandMotherPdgId;
};

// Embedding muons
class EmbeddingMuonCollection: public MuonCollection {
public:
  class Muon: public MuonCollection::Muon {
  public:
    Muon();
    Muon(EmbeddingMuonCollection *mc, size_t i);
    ~Muon();

    double chargedHadronIsoEmb() { return static_cast<EmbeddingMuonCollection *>(fCollection)->fChargedHadronIsoEmb->value()[index()]; }
    double puChargedHadronIsoEmb() { return static_cast<EmbeddingMuonCollection *>(fCollection)->fPuChargedHadronIsoEmb->value()[index()]; }
    double neutralHadronIsoEmb() { return static_cast<EmbeddingMuonCollection *>(fCollection)->fNeutralHadronIsoEmb->value()[index()]; }
    double photonIsoEmb() { return static_cast<EmbeddingMuonCollection *>(fCollection)->fPhotonIsoEmb->value()[index()]; }

    double standardRelativeIsolation() {
      return (chargedHadronIso() + std::max(0.0, photonIso() + neutralHadronIso() - 0.5*puChargedHadronIso()))/p4().Pt();
    }
    double tauLikeIsolation() {
      return chargedHadronIsoEmb() + std::max(0.0, photonIsoEmb() - 0.5*puChargedHadronIsoEmb());
    }
  };

  EmbeddingMuonCollection(const std::string& postfix = "_01to04");
  ~EmbeddingMuonCollection();

  void setupBranches(BranchManager& branchManager, bool isMC);
  Muon get(size_t i) {
    return Muon(this, i);
  }

private:
  std::string fPostfix;

  Branch<std::vector<double> > *fChargedHadronIsoEmb;
  Branch<std::vector<double> > *fPuChargedHadronIsoEmb;
  Branch<std::vector<double> > *fNeutralHadronIsoEmb;
  Branch<std::vector<double> > *fPhotonIsoEmb;
};


// Electrons
class ElectronCollection {
public:
  class Electron: public Impl::Particle<ElectronCollection> {
    typedef Impl::Particle<ElectronCollection> Base;
  public:
    Electron(ElectronCollection *ec, size_t i): Base(ec, i) {}
    ~Electron();

    bool hasGsfTrack() { return fCollection->fHasGsfTrack->value()[index()]; }
    bool hasSuperCluster() { return fCollection->fHasSuperCluster->value()[index()]; }
    bool cutBasedIdVeto() { return fCollection->fCutBasedIdVeto->value()[index()]; }
    bool cutBasedIdLoose() { return fCollection->fCutBasedIdLoose->value()[index()]; }
    bool cutBasedIdMedium() { return fCollection->fCutBasedIdMedium->value()[index()]; }
    bool cutBasedIdTight() { return fCollection->fCutBasedIdTight->value()[index()]; }

    double superClusterEta() { return fCollection->fSuperClusterEta->value()[index()]; }

    const math::XYZTLorentzVector& genMatchP4() { return fCollection->fGenMatchP4->value()[index()]; }
    int pdgId() { return fCollection->fPdgId->value()[index()]; }
    int motherPdgId() { return fCollection->fMotherPdgId->value()[index()]; }
    int grandMotherPdgId() { return fCollection->fGrandMotherPdgId->value()[index()]; }
  };


  ElectronCollection(const std::string prefix = "electrons");
  ~ElectronCollection();

  void setupBranches(BranchManager& branchManager, bool isMC);

  size_t size() {
    return fP4->value().size();
  }
  Electron get(size_t i) {
    return Electron(this, i);
  }


protected:
  std::string fPrefix;

private:
  Branch<std::vector<math::XYZTLorentzVector> > *fP4;
  Branch<std::vector<bool> > *fHasGsfTrack;
  Branch<std::vector<bool> > *fHasSuperCluster;
  Branch<std::vector<bool> > *fCutBasedIdVeto;
  Branch<std::vector<bool> > *fCutBasedIdLoose;
  Branch<std::vector<bool> > *fCutBasedIdMedium;
  Branch<std::vector<bool> > *fCutBasedIdTight;

  Branch<std::vector<double> > *fSuperClusterEta;

  Branch<std::vector<math::XYZTLorentzVector> > *fGenMatchP4;
  Branch<std::vector<int> > *fPdgId;
  Branch<std::vector<int> > *fMotherPdgId;
  Branch<std::vector<int> > *fGrandMotherPdgId;
};


// Jets
class JetCollection {
public:
  class Jet: public Impl::Particle<JetCollection> {
    typedef Impl::Particle<JetCollection> Base;
  public:
    Jet(JetCollection *jc, size_t i): Base(jc, i) {}
    ~Jet();

    bool looseID() { return fCollection->fLooseId->value()[index()]; }
    bool tightID() { return fCollection->fTightId->value()[index()]; }

    unsigned numberOfDaughters() { return fCollection->fNumberOfDaughters->value()[index()]; }

    double csv() { return fCollection->fCSV->value()[index()]; }

    bool btagged() { return fCollection->fBTagged->value()[index()]; }
    float btagScaleFactor() { return fCollection->fBTagSF->value()[index()]; }
    float btagScaleFactorUncertainty() { return fCollection->fBTagSFUnc->value()[index()]; }
  };

  JetCollection(const std::string prefix = "jets");
  ~JetCollection();

  void setupBranches(BranchManager& branchManager);

  size_t size() {
    return fP4->value().size();
  }
  Jet get(size_t i) {
    return Jet(this, i);
  }


protected:
  std::string fPrefix;

private:
  Branch<std::vector<math::XYZTLorentzVector> > *fP4;
  Branch<std::vector<unsigned> > *fNumberOfDaughters;
  Branch<std::vector<bool> > *fLooseId;
  Branch<std::vector<bool> > *fTightId;
  Branch<std::vector<double> > *fCSV;
  Branch<std::vector<bool> > *fBTagged;
  Branch<std::vector<float> > *fBTagSF;
  Branch<std::vector<float> > *fBTagSFUnc;
};

class JetDetailsCollection: public JetCollection {
public:
  class Jet: public JetCollection::Jet {
  public:
    Jet(JetDetailsCollection *jdc, size_t i);
    ~Jet();

    int chargedHadronMultiplicity() { return static_cast<JetDetailsCollection *>(fCollection)->fChm->value()[index()]; }
    int neutralHadronMultiplicity() { return static_cast<JetDetailsCollection *>(fCollection)->fNhm->value()[index()]; }
    int electronMultiplicity() { return static_cast<JetDetailsCollection *>(fCollection)->fElm->value()[index()]; }
    int photonMultiplicity() { return static_cast<JetDetailsCollection *>(fCollection)->fPhm->value()[index()]; }
    int muonMultiplicity() { return static_cast<JetDetailsCollection *>(fCollection)->fMum->value()[index()]; }

    double chargedHadronFraction() { return static_cast<JetDetailsCollection *>(fCollection)->fChf->value()[index()]; }
    double neutralHadronFraction() { return static_cast<JetDetailsCollection *>(fCollection)->fNhf->value()[index()]; }
    double electronFraction() { return static_cast<JetDetailsCollection *>(fCollection)->fElf->value()[index()]; }
    double photonFraction() { return static_cast<JetDetailsCollection *>(fCollection)->fPhf->value()[index()]; }
    double muonFraction() { return static_cast<JetDetailsCollection *>(fCollection)->fMuf->value()[index()]; }
  };

  JetDetailsCollection(const std::string prefix = "jets");
  ~JetDetailsCollection();

  void setupBranches(BranchManager& branchManager);
  Jet get(size_t i) {
    return Jet(this, i);
  }

private:
  Branch<std::vector<int> > *fChm;
  Branch<std::vector<int> > *fNhm;
  Branch<std::vector<int> > *fElm;
  Branch<std::vector<int> > *fPhm;
  Branch<std::vector<int> > *fMum;
  Branch<std::vector<double> > *fChf;
  Branch<std::vector<double> > *fNhf;
  Branch<std::vector<double> > *fElf;
  Branch<std::vector<double> > *fPhf;
  Branch<std::vector<double> > *fMuf;
};


// Taus
class TauCollection {
public:
  class Tau: public Impl::Particle<TauCollection> {
    typedef Impl::Particle<TauCollection> Base;
  public:
    Tau(TauCollection *tc, size_t i): Base(tc, i) {}
    ~Tau();

    const math::XYZTLorentzVector& leadPFChargedHadrCandP4() { return fCollection->fLeadPFChargedHadrCandP4->value()[index()]; }
    unsigned signalPFChargedHadrCandsCount() { return fCollection->fSignalPFChargedHadrCandsCount->value()[index()]; }
    int decayMode() { return fCollection->fDecayMode->value()[index()]; }

    double rtau() { return leadPFChargedHadrCandP4().P() / p4().P() -1e-10; }

    double decayModeFinding() { return fCollection->fDecayModeFinding->value()[index()]; }

    double againstMuonTight() { return fCollection->fAgainstMuonTight->value()[index()]; }
    double againstMuonTight2() { return fCollection->fAgainstMuonTight2->value()[index()]; }

    double againstElectronLoose() { return fCollection->fAgainstElectronLoose->value()[index()]; }
    double againstElectronMedium() { return fCollection->fAgainstElectronMedium->value()[index()]; }
    double againstElectronTight() { return fCollection->fAgainstElectronTight->value()[index()]; }
    double againstElectronMVA() { return fCollection->fAgainstElectronMVA->value()[index()]; }
    double againstElectronTightMVA3() { return fCollection->fAgainstElectronTightMVA3->value()[index()]; }

    double mediumCombinedIsolationDeltaBetaCorr() { return fCollection->fMediumCombinedIsolationDeltaBetaCorr->value()[index()]; }
    double mediumCombinedIsolationDeltaBetaCorr3Hits() { return fCollection->fMediumCombinedIsolationDeltaBetaCorr3Hits->value()[index()]; }

    const math::XYZTLorentzVector& genMatchP4() { return fCollection->fGenMatchP4->value()[index()]; }
    const math::XYZTLorentzVector& genMatchVisibleP4() { return fCollection->fGenMatchVisibleP4->value()[index()]; }
    int pdgId() { return fCollection->fPdgId->value()[index()]; }
    int motherPdgId() { return fCollection->fMotherPdgId->value()[index()]; }
    int grandMotherPdgId() { return fCollection->fGrandMotherPdgId->value()[index()]; }
    int daughterPdgId() { return fCollection->fDaughterPdgId->value()[index()]; }
  };

  TauCollection(const std::string prefix = "taus");
  ~TauCollection();

  void setupBranches(BranchManager& branchManager, bool isMC);

  size_t size() {
    return fP4->value().size();
  }
  Tau get(size_t i) {
    return Tau(this, i);
  }


protected:
  std::string fPrefix;

private:
  Branch<std::vector<math::XYZTLorentzVector> > *fP4;
  Branch<std::vector<math::XYZTLorentzVector> > *fLeadPFChargedHadrCandP4;
  Branch<std::vector<unsigned> > *fSignalPFChargedHadrCandsCount;
  Branch<std::vector<int> > *fDecayMode;

  Branch<std::vector<double> > *fDecayModeFinding;

  Branch<std::vector<double> > *fAgainstMuonTight;
  Branch<std::vector<double> > *fAgainstMuonTight2;

  Branch<std::vector<double> > *fAgainstElectronLoose;
  Branch<std::vector<double> > *fAgainstElectronMedium;
  Branch<std::vector<double> > *fAgainstElectronTight;
  Branch<std::vector<double> > *fAgainstElectronMVA;
  Branch<std::vector<double> > *fAgainstElectronTightMVA3;

  Branch<std::vector<double> > *fMediumCombinedIsolationDeltaBetaCorr;
  Branch<std::vector<double> > *fMediumCombinedIsolationDeltaBetaCorr3Hits;

  Branch<std::vector<math::XYZTLorentzVector> > *fGenMatchP4;
  Branch<std::vector<math::XYZTLorentzVector> > *fGenMatchVisibleP4;
  Branch<std::vector<int> > *fPdgId;
  Branch<std::vector<int> > *fMotherPdgId;
  Branch<std::vector<int> > *fGrandMotherPdgId;
  Branch<std::vector<int> > *fDaughterPdgId;
};


// GenParticles
class GenParticleCollection {
public:
  class GenParticle: public Impl::Particle<GenParticleCollection> {
    typedef Impl::Particle<GenParticleCollection> Base;
  public:
    GenParticle();
    GenParticle(GenParticleCollection *gpc, size_t i): Base(gpc, i) {}
    ~GenParticle();

    int pdgId() { return fCollection->fPdgId->value()[index()]; }
    int motherPdgId() { return fCollection->fMotherPdgId->value()[index()]; }
    int grandMotherPdgId() { return fCollection->fGrandMotherPdgId->value()[index()]; }

    // Tau specific
    int daughterPdgId() { return fCollection->fDaughterPdgId->value()[index()]; }
    const math::XYZTLorentzVector& visibleP4() { return fCollection->fVisibleP4->value()[index()]; }
 };

  GenParticleCollection(const std::string& prefix, bool isTau=false);
  ~GenParticleCollection();

  void setupBranches(BranchManager& branchManager);

  size_t size() {
    return fP4->value().size();
  }
  GenParticle get(size_t i) {
    return GenParticle(this, i);
  }

protected:
  std::string fPrefix;
  bool fIsTau;

private:
  Branch<std::vector<math::XYZTLorentzVector> > *fP4;
  Branch<std::vector<int> > *fPdgId;
  Branch<std::vector<int> > *fMotherPdgId;
  Branch<std::vector<int> > *fGrandMotherPdgId;

  Branch<std::vector<int> > *fDaughterPdgId;
  Branch<std::vector<math::XYZTLorentzVector> > *fVisibleP4;
};

#endif
