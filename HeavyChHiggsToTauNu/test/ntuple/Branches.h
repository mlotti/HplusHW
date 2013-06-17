// -*- c++ -*-
#ifndef __BRANCHES__
#define __BRANCHES__

#include "TTree.h"
#include "TBranch.h"
#include "Rtypes.h"
#include "Math/LorentzVector.h"
#include "Math/DisplacementVector3D.h"

#include<string>
#include<vector>

class TTree;
class TBranch;

// From DataFormats/Math/interface/LorentzVector.h
namespace math {
  typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > XYZTLorentzVectorD;
  typedef XYZTLorentzVectorD XYZTLorentzVector;

  typedef ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<double> > XYZVectorD;
  typedef XYZVectorD XYZVector;
}

// Generic branch
template <typename T>
struct BranchTraits {
  typedef T *DataType;
  typedef const T& ReturnType;
  static ReturnType get(const T* data) { return *data; }
};
template <>
struct BranchTraits<bool> {
  typedef bool DataType;
  typedef bool ReturnType;
  static ReturnType get(bool data) { return data; }
};
template <>
struct BranchTraits<int> {
  typedef int DataType;
  typedef int ReturnType;
  static ReturnType get(int data) { return data; }
};
template <>
struct BranchTraits<unsigned int> {
  typedef unsigned int DataType;
  typedef unsigned int ReturnType;
  static ReturnType get(unsigned int data) { return data; }
};
template <>
struct BranchTraits<float> {
  typedef float DataType;
  typedef float ReturnType;
  static ReturnType get(float data) { return data; }
};
template <>
struct BranchTraits<double> {
  typedef double DataType;
  typedef double ReturnType;
  static ReturnType get(double data) { return data; }
};

template <typename T>
class Branch {
public:
  Branch(): entry(0), data(0), branch(0), cached(false) {}
  ~Branch() {}

  void setupBranch(TTree *tree, const char *name) {
    tree->SetBranchAddress(name, &data, &branch);    
  }
  void setEntry(Long64_t e) { entry = e; cached = false; }
  typename BranchTraits<T>::ReturnType value() {
    if(!cached) {
      branch->GetEntry(entry);
      cached = true;
    }
    return BranchTraits<T>::get(data);
  }

private:
  Long64_t entry;
  typename BranchTraits<T>::DataType data;
  TBranch *branch;
  bool cached;
};

// Event information
class EventInfo {
public:
  EventInfo();
  ~EventInfo();

  void setupBranches(TTree *tree);
  void setEntry(Long64_t entry) {
    fEvent.setEntry(entry);
    fLumi.setEntry(entry);
    fRun.setEntry(entry);
  }

  unsigned event() { return fEvent.value(); }
  unsigned lumi() { return fLumi.value(); }
  unsigned run() { return fRun.value(); }

private:
  Branch<unsigned> fEvent;
  Branch<unsigned> fLumi;
  Branch<unsigned> fRun;
};

// Muons
class MuonCollection {
public:
  class Muon {
  public:
    Muon();
    Muon(MuonCollection *mc, size_t i);
    ~Muon();

    bool isValid() const { return fCollection != 0; }
    void ensureValidity() const;

    size_t index() const { return fIndex; }

    const math::XYZTLorentzVector& p4() { return fCollection->fP4.value()[fIndex]; }
    const math::XYZTLorentzVector& correctedP4() { return fCollection->fCorrectedP4.value()[fIndex]; }

    const math::XYZVector& tunePP3() { return fCollection->fTunePP3.value()[fIndex]; }
    double tunePPtError() { return fCollection->fTunePPtError.value()[fIndex]; }

    int charge() { return fCollection->fCharge.value()[fIndex]; }
    double normalizedChi2() { return fCollection->fNormalizedChi2.value()[fIndex]; }
    double dB() { return fCollection->fDB.value()[fIndex]; }

    double trackIso() { return fCollection->fTrackIso.value()[fIndex]; }
    double caloIso() { return fCollection->fCaloIso.value()[fIndex]; }

    double chargedHadronIso() { return fCollection->fChargedHadronIso.value()[fIndex]; }
    double puChargedHadronIso() { return fCollection->fPuChargedHadronIso.value()[fIndex]; }
    double neutralHadronIso() { return fCollection->fNeutralHadronIso.value()[fIndex]; }
    double photonIso() { return fCollection->fPhotonIso.value()[fIndex]; }

    double idEfficiency() { return fCollection->fIdEfficiency.value()[fIndex]; }

    const math::XYZTLorentzVector& genMatchP4() { return fCollection->fGenMatchP4.value()[fIndex]; }
    int pdgId() { return fCollection->fPdgId.value()[fIndex]; }
    int motherPdgId() { return fCollection->fMotherPdgId.value()[fIndex]; }
    int grandMotherPdgId() { return fCollection->fGrandMotherPdgId.value()[fIndex]; }

  protected:
    MuonCollection *fCollection;
    size_t fIndex;
  };


  MuonCollection(const std::string prefix = "muons");
  ~MuonCollection();

  void setIdEfficiencyName(const std::string& idEff) { fIdEfficiencyName = idEff; }

  void setupBranches(TTree *tree, bool isMC);
  void setEntry(Long64_t entry) {
    fP4.setEntry(entry);
    fCorrectedP4.setEntry(entry);

    fTunePP3.setEntry(entry);
    fTunePPtError.setEntry(entry);

    fCharge.setEntry(entry);
    fDB.setEntry(entry);
    fNormalizedChi2.setEntry(entry);

    fTrackIso.setEntry(entry);
    fCaloIso.setEntry(entry);

    fChargedHadronIso.setEntry(entry);
    fPuChargedHadronIso.setEntry(entry);
    fNeutralHadronIso.setEntry(entry);
    fPhotonIso.setEntry(entry);

    fIdEfficiency.setEntry(entry);

    fPdgId.setEntry(entry);
    fMotherPdgId.setEntry(entry);
    fGrandMotherPdgId.setEntry(entry);
  }

  size_t size() {
    return fP4.value().size();
  }
  Muon get(size_t i) {
    return Muon(this, i);
  }


protected:
  std::string fPrefix;

private:
  std::string fIdEfficiencyName;

  Branch<std::vector<math::XYZTLorentzVector> > fP4;
  Branch<std::vector<math::XYZTLorentzVector> > fCorrectedP4;

  Branch<std::vector<math::XYZVector> > fTunePP3;
  Branch<std::vector<double> > fTunePPtError;

  Branch<std::vector<int> > fCharge;
  Branch<std::vector<double> > fDB;
  Branch<std::vector<double> > fNormalizedChi2;

  Branch<std::vector<double> > fTrackIso;
  Branch<std::vector<double> > fCaloIso;

  Branch<std::vector<double> > fChargedHadronIso;
  Branch<std::vector<double> > fPuChargedHadronIso;
  Branch<std::vector<double> > fNeutralHadronIso;
  Branch<std::vector<double> > fPhotonIso;

  Branch<std::vector<double> > fIdEfficiency;

  Branch<std::vector<math::XYZTLorentzVector> > fGenMatchP4;
  Branch<std::vector<int> > fPdgId;
  Branch<std::vector<int> > fMotherPdgId;
  Branch<std::vector<int> > fGrandMotherPdgId;
};

// Embedding muons
class EmbeddingMuonCollection: public MuonCollection {
public:
  class Muon: public MuonCollection::Muon {
  public:
    Muon();
    Muon(EmbeddingMuonCollection *mc, size_t i);
    ~Muon();

    double chargedHadronIsoEmb() { return static_cast<EmbeddingMuonCollection *>(fCollection)->fChargedHadronIsoEmb.value()[fIndex]; }
    double puChargedHadronIsoEmb() { return static_cast<EmbeddingMuonCollection *>(fCollection)->fPuChargedHadronIsoEmb.value()[fIndex]; }
    double neutralHadronIsoEmb() { return static_cast<EmbeddingMuonCollection *>(fCollection)->fNeutralHadronIsoEmb.value()[fIndex]; }
    double photonIsoEmb() { return static_cast<EmbeddingMuonCollection *>(fCollection)->fPhotonIsoEmb.value()[fIndex]; }

    double standardRelativeIsolation() {
      return (chargedHadronIso() + std::max(0.0, photonIso() + neutralHadronIso() - 0.5*puChargedHadronIso()))/p4().Pt();
    }
    double tauLikeIsolation() {
      return chargedHadronIsoEmb() + std::max(0.0, photonIsoEmb() - 0.5*puChargedHadronIsoEmb());
    }
  };

  EmbeddingMuonCollection(const std::string& postfix = "_01to04");
  ~EmbeddingMuonCollection();

  void setupBranches(TTree *tree, bool isMC);
  void setEntry(Long64_t entry) {
    MuonCollection::setEntry(entry);

    fChargedHadronIsoEmb.setEntry(entry);
    fPuChargedHadronIsoEmb.setEntry(entry);
    fNeutralHadronIsoEmb.setEntry(entry);
    fPhotonIsoEmb.setEntry(entry);
  }
  Muon get(size_t i) {
    return Muon(this, i);
  }

private:
  std::string fPostfix;

  Branch<std::vector<double> > fChargedHadronIsoEmb;
  Branch<std::vector<double> > fPuChargedHadronIsoEmb;
  Branch<std::vector<double> > fNeutralHadronIsoEmb;
  Branch<std::vector<double> > fPhotonIsoEmb;
};


// Electrons
class ElectronCollection {
public:
  class Electron {
  public:
    Electron(ElectronCollection *mc, size_t i);
    ~Electron();

    size_t index() const { return fIndex; }

    const math::XYZTLorentzVector& p4() { return fCollection->fP4.value()[fIndex]; }

    bool hasGsfTrack() { return fCollection->fHasGsfTrack.value()[fIndex]; }
    bool hasSuperCluster() { return fCollection->fHasSuperCluster.value()[fIndex]; }
    bool cutBasedIdVeto() { return fCollection->fCutBasedIdVeto.value()[fIndex]; }
    bool cutBasedIdLoose() { return fCollection->fCutBasedIdLoose.value()[fIndex]; }
    bool cutBasedIdMedium() { return fCollection->fCutBasedIdMedium.value()[fIndex]; }
    bool cutBasedIdTight() { return fCollection->fCutBasedIdTight.value()[fIndex]; }

    double superClusterEta() { return fCollection->fSuperClusterEta.value()[fIndex]; }

    const math::XYZTLorentzVector& genMatchP4() { return fCollection->fGenMatchP4.value()[fIndex]; }
    int pdgId() { return fCollection->fPdgId.value()[fIndex]; }
    int motherPdgId() { return fCollection->fMotherPdgId.value()[fIndex]; }
    int grandMotherPdgId() { return fCollection->fGrandMotherPdgId.value()[fIndex]; }

  protected:
    ElectronCollection *fCollection;
    size_t fIndex;
  };


  ElectronCollection(const std::string prefix = "electrons");
  ~ElectronCollection();

  void setupBranches(TTree *tree, bool isMC);
  void setEntry(Long64_t entry) {
    fP4.setEntry(entry);

    fHasGsfTrack.setEntry(entry);
    fHasSuperCluster.setEntry(entry);
    fCutBasedIdVeto.setEntry(entry);
    fCutBasedIdLoose.setEntry(entry);
    fCutBasedIdMedium.setEntry(entry);
    fCutBasedIdTight.setEntry(entry);

    fSuperClusterEta.setEntry(entry);

    fPdgId.setEntry(entry);
    fMotherPdgId.setEntry(entry);
    fGrandMotherPdgId.setEntry(entry);
  }

  size_t size() {
    return fP4.value().size();
  }
  Electron get(size_t i) {
    return Electron(this, i);
  }


protected:
  std::string fPrefix;

private:
  Branch<std::vector<math::XYZTLorentzVector> > fP4;
  Branch<std::vector<bool> > fHasGsfTrack;
  Branch<std::vector<bool> > fHasSuperCluster;
  Branch<std::vector<bool> > fCutBasedIdVeto;
  Branch<std::vector<bool> > fCutBasedIdLoose;
  Branch<std::vector<bool> > fCutBasedIdMedium;
  Branch<std::vector<bool> > fCutBasedIdTight;

  Branch<std::vector<double> > fSuperClusterEta;

  Branch<std::vector<math::XYZTLorentzVector> > fGenMatchP4;
  Branch<std::vector<int> > fPdgId;
  Branch<std::vector<int> > fMotherPdgId;
  Branch<std::vector<int> > fGrandMotherPdgId;
};


// Jets
class JetCollection {
public:
  class Jet {
  public:
    Jet(JetCollection *mc, size_t i);
    ~Jet();

    size_t index() const { return fIndex; }
    const math::XYZTLorentzVector& p4() { return fCollection->fP4.value()[fIndex]; }

    bool looseID() { return fCollection->fLooseId.value()[fIndex]; }
    bool tightID() { return fCollection->fTightId.value()[fIndex]; }

    unsigned numberOfDaughters() { return fCollection->fNumberOfDaughters.value()[fIndex]; }

  protected:
    JetCollection *fCollection;
    size_t fIndex;
  };

  JetCollection(const std::string prefix = "jets");
  ~JetCollection();

  void setupBranches(TTree *tree);
  void setEntry(Long64_t entry) {
    fP4.setEntry(entry);
    fNumberOfDaughters.setEntry(entry);
    fLooseId.setEntry(entry);
    fTightId.setEntry(entry);
  }

  size_t size() {
    return fP4.value().size();
  }
  Jet get(size_t i) {
    return Jet(this, i);
  }


protected:
  std::string fPrefix;

private:
  Branch<std::vector<math::XYZTLorentzVector> > fP4;
  Branch<std::vector<unsigned> > fNumberOfDaughters;
  Branch<std::vector<bool> > fLooseId;
  Branch<std::vector<bool> > fTightId;
};

class JetDetailsCollection: public JetCollection {
public:
  class Jet: public JetCollection::Jet {
  public:
    Jet(JetDetailsCollection *jdc, size_t i);
    ~Jet();

    int chargedHadronMultiplicity() { return static_cast<JetDetailsCollection *>(fCollection)->fChm.value()[fIndex]; }
    int neutralHadronMultiplicity() { return static_cast<JetDetailsCollection *>(fCollection)->fNhm.value()[fIndex]; }
    int electronMultiplicity() { return static_cast<JetDetailsCollection *>(fCollection)->fElm.value()[fIndex]; }
    int photonMultiplicity() { return static_cast<JetDetailsCollection *>(fCollection)->fPhm.value()[fIndex]; }
    int muonMultiplicity() { return static_cast<JetDetailsCollection *>(fCollection)->fMum.value()[fIndex]; }

    double chargedHadronFraction() { return static_cast<JetDetailsCollection *>(fCollection)->fChf.value()[fIndex]; }
    double neutralHadronFraction() { return static_cast<JetDetailsCollection *>(fCollection)->fNhf.value()[fIndex]; }
    double electronFraction() { return static_cast<JetDetailsCollection *>(fCollection)->fElf.value()[fIndex]; }
    double photonFraction() { return static_cast<JetDetailsCollection *>(fCollection)->fPhf.value()[fIndex]; }
    double muonFraction() { return static_cast<JetDetailsCollection *>(fCollection)->fMuf.value()[fIndex]; }
  };

  JetDetailsCollection(const std::string prefix = "jets");
  ~JetDetailsCollection();

  void setupBranches(TTree *tree);
  void setEntry(Long64_t entry) {
    JetCollection::setEntry(entry);

    fChm.setEntry(entry);
    fNhm.setEntry(entry);
    fElm.setEntry(entry);
    fPhm.setEntry(entry);
    fMum.setEntry(entry);
    fChf.setEntry(entry);
    fNhf.setEntry(entry);
    fElf.setEntry(entry);
    fPhf.setEntry(entry);
    fMuf.setEntry(entry);
  }
  Jet get(size_t i) {
    return Jet(this, i);
  }

private:
  Branch<std::vector<int> > fChm;
  Branch<std::vector<int> > fNhm;
  Branch<std::vector<int> > fElm;
  Branch<std::vector<int> > fPhm;
  Branch<std::vector<int> > fMum;
  Branch<std::vector<double> > fChf;
  Branch<std::vector<double> > fNhf;
  Branch<std::vector<double> > fElf;
  Branch<std::vector<double> > fPhf;
  Branch<std::vector<double> > fMuf;
};


// Taus
class TauCollection {
public:
  class Tau {
  public:
    Tau(TauCollection *mc, size_t i);
    ~Tau();

    size_t index() const { return fIndex; }
    const math::XYZTLorentzVector& p4() { return fCollection->fP4.value()[fIndex]; }
    const math::XYZTLorentzVector& leadPFChargedHadrCandP4() { return fCollection->fLeadPFChargedHadrCandP4.value()[fIndex]; }
    unsigned signalPFChargedHadrCandsCount() { return fCollection->fSignalPFChargedHadrCandsCount.value()[fIndex]; }
    int decayMode() { return fCollection->fDecayMode.value()[fIndex]; }

    double rtau() { return leadPFChargedHadrCandP4().P() / p4().P() -1e-10; }

    double decayModeFinding() { return fCollection->fDecayModeFinding.value()[fIndex]; }

    double againstMuonTight() { return fCollection->fAgainstMuonTight.value()[fIndex]; }
    double againstMuonTight2() { return fCollection->fAgainstMuonTight2.value()[fIndex]; }

    double againstElectronLoose() { return fCollection->fAgainstElectronLoose.value()[fIndex]; }
    double againstElectronMedium() { return fCollection->fAgainstElectronMedium.value()[fIndex]; }
    double againstElectronTight() { return fCollection->fAgainstElectronTight.value()[fIndex]; }
    double againstElectronMVA() { return fCollection->fAgainstElectronMVA.value()[fIndex]; }
    double againstElectronTightMVA3() { return fCollection->fAgainstElectronTightMVA3.value()[fIndex]; }

    double mediumCombinedIsolationDeltaBetaCorr() { return fCollection->fMediumCombinedIsolationDeltaBetaCorr.value()[fIndex]; }
    double mediumCombinedIsolationDeltaBetaCorr3Hits() { return fCollection->fMediumCombinedIsolationDeltaBetaCorr3Hits.value()[fIndex]; }

    const math::XYZTLorentzVector& genMatchP4() { return fCollection->fGenMatchP4.value()[fIndex]; }
    const math::XYZTLorentzVector& genMatchVisibleP4() { return fCollection->fGenMatchVisibleP4.value()[fIndex]; }
    int pdgId() { return fCollection->fPdgId.value()[fIndex]; }
    int motherPdgId() { return fCollection->fMotherPdgId.value()[fIndex]; }
    int grandMotherPdgId() { return fCollection->fGrandMotherPdgId.value()[fIndex]; }
    int daughterPdgId() { return fCollection->fDaughterPdgId.value()[fIndex]; }

  protected:
    TauCollection *fCollection;
    size_t fIndex;
  };

  TauCollection(const std::string prefix = "taus");
  ~TauCollection();

  void setupBranches(TTree *tree, bool isMC);
  void setEntry(Long64_t entry) {
    fP4.setEntry(entry);
    fLeadPFChargedHadrCandP4.setEntry(entry);
    fSignalPFChargedHadrCandsCount.setEntry(entry);
    fDecayMode.setEntry(entry);

    fDecayModeFinding.setEntry(entry);
    fAgainstMuonTight.setEntry(entry);
    fAgainstMuonTight2.setEntry(entry);
    fAgainstElectronLoose.setEntry(entry);
    fAgainstElectronMedium.setEntry(entry);
    fAgainstElectronTight.setEntry(entry);
    fAgainstElectronMVA.setEntry(entry);
    fAgainstElectronTightMVA3.setEntry(entry);
    fMediumCombinedIsolationDeltaBetaCorr.setEntry(entry);
    fMediumCombinedIsolationDeltaBetaCorr3Hits.setEntry(entry);

    fGenMatchP4.setEntry(entry);
    fGenMatchVisibleP4.setEntry(entry);
    fPdgId.setEntry(entry);
    fMotherPdgId.setEntry(entry);
    fGrandMotherPdgId.setEntry(entry);
    fDaughterPdgId.setEntry(entry);
  }

  size_t size() {
    return fP4.value().size();
  }
  Tau get(size_t i) {
    return Tau(this, i);
  }


protected:
  std::string fPrefix;

private:
  Branch<std::vector<math::XYZTLorentzVector> > fP4;
  Branch<std::vector<math::XYZTLorentzVector> > fLeadPFChargedHadrCandP4;
  Branch<std::vector<unsigned> > fSignalPFChargedHadrCandsCount;
  Branch<std::vector<int> > fDecayMode;

  Branch<std::vector<double> > fDecayModeFinding;

  Branch<std::vector<double> > fAgainstMuonTight;
  Branch<std::vector<double> > fAgainstMuonTight2;

  Branch<std::vector<double> > fAgainstElectronLoose;
  Branch<std::vector<double> > fAgainstElectronMedium;
  Branch<std::vector<double> > fAgainstElectronTight;
  Branch<std::vector<double> > fAgainstElectronMVA;
  Branch<std::vector<double> > fAgainstElectronTightMVA3;

  Branch<std::vector<double> > fMediumCombinedIsolationDeltaBetaCorr;
  Branch<std::vector<double> > fMediumCombinedIsolationDeltaBetaCorr3Hits;

  Branch<std::vector<math::XYZTLorentzVector> > fGenMatchP4;
  Branch<std::vector<math::XYZTLorentzVector> > fGenMatchVisibleP4;
  Branch<std::vector<int> > fPdgId;
  Branch<std::vector<int> > fMotherPdgId;
  Branch<std::vector<int> > fGrandMotherPdgId;
  Branch<std::vector<int> > fDaughterPdgId;
};


// GenParticles
class GenParticleCollection {
public:
  class GenParticle {
  public:
    GenParticle();
    GenParticle(GenParticleCollection *gpc, size_t i);
    ~GenParticle();

    bool isValid() const { return fCollection != 0; }

    size_t index() const { return fIndex; }
    const math::XYZTLorentzVector& p4() { return fCollection->fP4.value()[fIndex]; }
    int pdgId() { return fCollection->fPdgId.value()[fIndex]; }
    int motherPdgId() { return fCollection->fMotherPdgId.value()[fIndex]; }
    int grandMotherPdgId() { return fCollection->fGrandMotherPdgId.value()[fIndex]; }

    // Tau specific
    int daughterPdgId() { return fCollection->fDaughterPdgId.value()[fIndex]; }
    const math::XYZTLorentzVector& visibleP4() { return fCollection->fVisibleP4.value()[fIndex]; }

  protected:
    GenParticleCollection *fCollection;
    size_t fIndex;
  };

  GenParticleCollection(const std::string& prefix, bool isTau=false);
  ~GenParticleCollection();

  void setupBranches(TTree *tree);
  void setEntry(Long64_t entry) {
    fP4.setEntry(entry);
    fPdgId.setEntry(entry);
    fMotherPdgId.setEntry(entry);
    fGrandMotherPdgId.setEntry(entry);

    fDaughterPdgId.setEntry(entry);
    fVisibleP4.setEntry(entry);
  }

  size_t size() {
    return fP4.value().size();
  }
  GenParticle get(size_t i) {
    return GenParticle(this, i);
  }

protected:
  std::string fPrefix;
  bool fIsTau;

private:
  Branch<std::vector<math::XYZTLorentzVector> > fP4;
  Branch<std::vector<int> > fPdgId;
  Branch<std::vector<int> > fMotherPdgId;
  Branch<std::vector<int> > fGrandMotherPdgId;

  Branch<std::vector<int> > fDaughterPdgId;
  Branch<std::vector<math::XYZTLorentzVector> > fVisibleP4;
};

#endif
