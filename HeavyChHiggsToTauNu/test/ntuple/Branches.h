// -*- c++ -*-
#ifndef __BRANCHES__
#define __BRANCHES__

#include "TTree.h"
#include "TBranch.h"
#include "Rtypes.h"
#include "Math/LorentzVector.h"

#include<string>
#include<vector>

class TTree;
class TBranch;

// From DataFormats/Math/interface/LorentzVector.h
namespace math {
  typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > XYZTLorentzVectorD;
  typedef XYZTLorentzVectorD XYZTLorentzVector;
}

// Generic branch
template <typename T>
class Branch {
public:
  Branch() {}
  ~Branch() {}

  void setupBranch(TTree *tree, const char *name) {
    tree->SetBranchAddress(name, &data, &branch);    
  }
  void setEntry(Long64_t e) { entry = e; cached = false; }
  const T& value() {
    if(!cached) {
      branch->GetEntry(entry);
      cached = true;
    }
    return data;
  }

private:
  Long64_t entry;
  T data;
  TBranch *branch;
  bool cached;
};

// Generic branch of a vector
template <typename T>
class BranchObj {
public:
  BranchObj(): data(0) {}
  ~BranchObj() {}

  void setupBranch(TTree *tree, const char *name) {
    tree->SetBranchAddress(name, &data, &branch);    
  }
  void setEntry(Long64_t e) { entry = e; cached = false; }
  const T& value() {
    if(!cached) {
      branch->GetEntry(entry);
      cached = true;
    }
    return *data;
  }

private:
  Long64_t entry;
  T *data;
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
    Muon(MuonCollection *mc, size_t i);
    ~Muon();

    size_t index() const { return fIndex; }

    const math::XYZTLorentzVector& p4() { return fCollection->fP4.value()[fIndex]; }
    double dB() { return fCollection->fDB.value()[fIndex]; }

    double trackIso() { return fCollection->fTrackIso.value()[fIndex]; }
    double caloIso() { return fCollection->fCaloIso.value()[fIndex]; }

    double chargedHadronIso() { return fCollection->fChargedHadronIso.value()[fIndex]; }
    double puChargedHadronIso() { return fCollection->fPuChargedHadronIso.value()[fIndex]; }
    double neutralHadronIso() { return fCollection->fNeutralHadronIso.value()[fIndex]; }
    double photonIso() { return fCollection->fPhotonIso.value()[fIndex]; }

    int pdgId() { return fCollection->fPdgId.value()[fIndex]; }
    int motherPdgId() { return fCollection->fMotherPdgId.value()[fIndex]; }
    int grandMotherPdgId() { return fCollection->fGrandMotherPdgId.value()[fIndex]; }

  protected:
    MuonCollection *fCollection;
    size_t fIndex;
  };


  MuonCollection(const std::string prefix = "muons");
  ~MuonCollection();

  void setupBranches(TTree *tree, bool isMC);
  void setEntry(Long64_t entry) {
    fP4.setEntry(entry);
    fDB.setEntry(entry);

    fTrackIso.setEntry(entry);
    fCaloIso.setEntry(entry);

    fChargedHadronIso.setEntry(entry);
    fPuChargedHadronIso.setEntry(entry);
    fNeutralHadronIso.setEntry(entry);
    fPhotonIso.setEntry(entry);

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
  BranchObj<std::vector<math::XYZTLorentzVector> > fP4;
  BranchObj<std::vector<double> > fDB;

  BranchObj<std::vector<double> > fTrackIso;
  BranchObj<std::vector<double> > fCaloIso;

  BranchObj<std::vector<double> > fChargedHadronIso;
  BranchObj<std::vector<double> > fPuChargedHadronIso;
  BranchObj<std::vector<double> > fNeutralHadronIso;
  BranchObj<std::vector<double> > fPhotonIso;

  BranchObj<std::vector<int> > fPdgId;
  BranchObj<std::vector<int> > fMotherPdgId;
  BranchObj<std::vector<int> > fGrandMotherPdgId;
};

// Embedding muons
class EmbeddingMuonCollection: public MuonCollection {
public:
  class Muon: public MuonCollection::Muon {
  public:
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

  BranchObj<std::vector<double> > fChargedHadronIsoEmb;
  BranchObj<std::vector<double> > fPuChargedHadronIsoEmb;
  BranchObj<std::vector<double> > fNeutralHadronIsoEmb;
  BranchObj<std::vector<double> > fPhotonIsoEmb;
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

  protected:
    JetCollection *fCollection;
    size_t fIndex;
  };

  JetCollection(const std::string prefix = "jets");
  ~JetCollection();

  void setupBranches(TTree *tree);
  void setEntry(Long64_t entry) {
    fP4.setEntry(entry);
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
  BranchObj<std::vector<math::XYZTLorentzVector> > fP4;
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

    double againstElectronLoose() { return fCollection->fAgainstElectronLoose.value()[fIndex]; }
    double againstElectronMedium() { return fCollection->fAgainstElectronMedium.value()[fIndex]; }
    double againstElectronTight() { return fCollection->fAgainstElectronTight.value()[fIndex]; }
    double againstElectronMVA() { return fCollection->fAgainstElectronMVA.value()[fIndex]; }

    double mediumCombinedIsolationDeltaBetaCorr() { return fCollection->fMediumCombinedIsolationDeltaBetaCorr.value()[fIndex]; }

  protected:
    TauCollection *fCollection;
    size_t fIndex;
  };

  TauCollection(const std::string prefix = "taus");
  ~TauCollection();

  void setupBranches(TTree *tree);
  void setEntry(Long64_t entry) {
    fP4.setEntry(entry);
    fLeadPFChargedHadrCandP4.setEntry(entry);
    fSignalPFChargedHadrCandsCount.setEntry(entry);
    fDecayMode.setEntry(entry);

    fDecayModeFinding.setEntry(entry);
    fAgainstMuonTight.setEntry(entry);
    fAgainstElectronLoose.setEntry(entry);
    fAgainstElectronMedium.setEntry(entry);
    fAgainstElectronTight.setEntry(entry);
    fAgainstElectronMVA.setEntry(entry);
    fMediumCombinedIsolationDeltaBetaCorr.setEntry(entry);
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
  BranchObj<std::vector<math::XYZTLorentzVector> > fP4;
  BranchObj<std::vector<math::XYZTLorentzVector> > fLeadPFChargedHadrCandP4;
  BranchObj<std::vector<unsigned> > fSignalPFChargedHadrCandsCount;
  BranchObj<std::vector<int> > fDecayMode;

  BranchObj<std::vector<double> > fDecayModeFinding;

  BranchObj<std::vector<double> > fAgainstMuonTight;

  BranchObj<std::vector<double> > fAgainstElectronLoose;
  BranchObj<std::vector<double> > fAgainstElectronMedium;
  BranchObj<std::vector<double> > fAgainstElectronTight;
  BranchObj<std::vector<double> > fAgainstElectronMVA;

  BranchObj<std::vector<double> > fMediumCombinedIsolationDeltaBetaCorr;
};


#endif
