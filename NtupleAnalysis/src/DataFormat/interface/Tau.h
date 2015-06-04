// -*- c++ -*-
#ifndef DataFormat_Tau_h
#define DataFormat_Tau_h

#include "DataFormat/interface/TauGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

#include <vector>

class Tau;

class TauCollection: public TauGeneratedCollection, public ParticleIteratorAdaptor<TauCollection> {
public:
  using value_type = Tau;

  TauCollection() {}
  explicit TauCollection(const std::string& prefix): TauGeneratedCollection(prefix) {}
  ~TauCollection() {}

  void setConfigurableDiscriminators(const std::vector<std::string>& names) {
    fConfigurableDiscriminatorNames = names;
  }
  void setAgainstElectronDiscriminator(const std::string& name) {
    fAgainstElectronDiscriminatorName = name;
  }
  void setAgainstMuonDiscriminator(const std::string& name) {
    fAgainstMuonDiscriminatorName = name;
  }
  void setIsolationDiscriminator(const std::string& name) {
    fIsolationDiscriminatorName = name;
  }

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
  std::vector<std::string> fConfigurableDiscriminatorNames;
  std::string fAgainstElectronDiscriminatorName;
  std::string fAgainstMuonDiscriminatorName;
  std::string fIsolationDiscriminatorName;
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
    return fCollection->fAgainstElectronDiscriminator->value()[index()];
  }
  bool againstMuonDiscriminator() const {
    return fCollection->fAgainstMuonDiscriminator->value()[index()];
  }
  bool isolationDiscriminator() const {
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
