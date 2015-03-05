// -*- c++ -*-
#ifndef DataFormat_Electron_h
#define DataFormat_Electron_h

#include "DataFormat/interface/ElectronGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

class Electron;

class ElectronCollection: public ElectronGeneratedCollection, public ParticleIteratorAdaptor<ElectronCollection> {
public:
  using value_type = Electron;

  ElectronCollection() {}
  ElectronCollection(const std::string& prefix): ElectronGeneratedCollection(prefix) {}
  ~ElectronCollection() {}

  void setupBranches(BranchManager& mgr);

  Electron operator[](size_t i);
  std::vector<Electron> toVector();

  friend class Electron;
  friend class ElectronGenerated;
  friend class Particle<ElectronCollection>;

protected:
};

class Electron: public ElectronGenerated {
public:
  Electron() {}
  Electron(ElectronCollection* coll, size_t index): ElectronGenerated(coll, index) {}
  ~Electron() {}
};

inline
Electron ElectronCollection::operator[](size_t i) {
  return Electron(this, i);
}

inline
std::vector<Electron> ElectronCollection::toVector() {
  return ParticleCollectionBase::toVector(*this);
}

#endif
