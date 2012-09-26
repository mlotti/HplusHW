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

#endif
