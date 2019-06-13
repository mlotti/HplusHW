// -*- c++ -*-
#ifndef DataFormat_Electron_h
#define DataFormat_Electron_h

#include "DataFormat/interface/ElectronGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

class Electron;

class ElectronCollection: public ElectronGeneratedCollection, public ParticleIteratorAdaptor<ElectronCollection> {
public:
  using value_type = Electron;

  ElectronCollection() { initialize(); }
  ElectronCollection(const std::string& prefix): ElectronGeneratedCollection(prefix) { initialize(); }
  ~ElectronCollection() {}

  void setupBranches(BranchManager& mgr);

  void setElectronIDDiscriminator(const std::string& name);
  bool electronIDDiscriminatorIsValid() const;
  
  Electron operator[](size_t i) const;
  std::vector<Electron> toVector() const;

  friend class Electron;
  friend class ElectronGenerated<ElectronCollection>;
  friend class Particle<ElectronCollection>;

protected:
  const Branch<std::vector<bool>>* fElectronIDDiscriminator;
  
private:
  void initialize();
  
  std::string fElectronIDDiscriminatorName;
  bool bValidityOfElectronIDDiscr;
};

class Electron: public ElectronGenerated<ElectronCollection> {
public:
  Electron() {}
  Electron(const ElectronCollection* coll, size_t index): ElectronGenerated(coll, index) {}
  ~Electron() {}

  bool electronIDDiscriminator() const {
    if (!fCollection->electronIDDiscriminatorIsValid())
      return true;
    return fCollection->fElectronIDDiscriminator->value()[index()];
  }
  /// Operator defined for using std::sort on vector<Tau>
  bool operator<(const Electron& electron) const {
    // Descending order by e pT
    return (this->pt() > electron.pt());
  }
};

inline
Electron ElectronCollection::operator[](size_t i) const {
  return Electron(this, i);
}

inline
std::vector<Electron> ElectronCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
