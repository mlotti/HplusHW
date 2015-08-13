// -*- c++ -*-
#ifndef DataFormat_Tau_h
#define DataFormat_Tau_h

#include "DataFormat/interface/TauGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

#include <vector>

class Tau;

enum TauDecayMatchType {
  kTauDecayUnknown = 0,
  kUToTau = 1,
  kDToTau = 2,
  kSToTau = 3,
  kCToTau = 4,
  kBToTau = 5,
  kElectronToTau = 11,
  kMuonToTau = 13,
  kTauDecaysToHadrons = 15,
  kGluonToTau = 21,
  kTauDecaysToElectron = 1511,
  kTauDecaysToMuon = 1513
};

enum TauOriginType {
  kTauOriginUnknown = 0,
  kFromZ = 23,
  kFromW = 24,
  kFromHplus = 37,
  kFromOtherSource = 999
};

class TauCollection: public TauGeneratedCollection, public ParticleIteratorAdaptor<TauCollection> {
public:
  using value_type = Tau;

  TauCollection() { initialize(); }
  explicit TauCollection(const std::string& prefix): TauGeneratedCollection(prefix) { initialize(); }
  ~TauCollection() {}
  
  // Discriminators
  void setConfigurableDiscriminators(const std::vector<std::string>& names) {
    fConfigurableDiscriminatorNames = names;
  }
  void setAgainstElectronDiscriminator(const std::string& name);
  void setAgainstMuonDiscriminator(const std::string& name);
  void setIsolationDiscriminator(const std::string& name);
  bool againstElectronDiscriminatorIsValid() const;
  bool againstMuonDiscriminatorIsValid() const;
  bool isolationDiscriminatorIsValid() const;

  void setupBranches(BranchManager& mgr);

  Tau operator[](size_t i) const;
  std::vector<Tau> toVector() const;

  friend class Tau;
  friend class TauGenerated<TauCollection>;
  friend class Particle<TauCollection>;

protected:
  std::vector<const Branch<std::vector<bool>> *> fConfigurableDiscriminators;
  const Branch<std::vector<bool>>* fAgainstElectronDiscriminator;
  const Branch<std::vector<bool>>* fAgainstMuonDiscriminator;
  const Branch<std::vector<bool>>* fIsolationDiscriminator;

private:
  /// Initialize data members
  void initialize();
  
  std::vector<std::string> fConfigurableDiscriminatorNames;
  std::string fAgainstElectronDiscriminatorName;
  std::string fAgainstMuonDiscriminatorName;
  std::string fIsolationDiscriminatorName;
  bool bValidityOfAgainstElectronDiscr;
  bool bValidityOfAgainstMuonDiscr;
  bool bValidityOfIsolationDiscr;
};

class Tau: public TauGenerated<TauCollection> {
public:
  Tau() {}
  Tau(const TauCollection* coll, size_t index): TauGenerated(coll, index) {}
  ~Tau() {}

  bool configurableDiscriminators() const {
    for(auto& disc: fCollection->fConfigurableDiscriminators) {
      if(!disc->value()[index()])
        return false;
    }
    return true;
  }
  bool againstElectronDiscriminator() const {
    if (!fCollection->againstElectronDiscriminatorIsValid())
      return true;
    return fCollection->fAgainstElectronDiscriminator->value()[index()];
  }
  bool againstMuonDiscriminator() const {
    if (!fCollection->againstMuonDiscriminatorIsValid())
      return true;
    return fCollection->fAgainstMuonDiscriminator->value()[index()];
  }
  bool isolationDiscriminator() const {
    if (!fCollection->isolationDiscriminatorIsValid())
      return true;
    return fCollection->fIsolationDiscriminator->value()[index()];
  }
  /// Operator defined for using std::sort on vector<Tau>
  bool operator<(const Tau& tau) const {
    // Descending order by tau pT
    return (this->pt() > tau.pt());
  }
};

inline
Tau TauCollection::operator[](size_t i) const {
  return Tau(this, i);
}

inline
std::vector<Tau> TauCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
