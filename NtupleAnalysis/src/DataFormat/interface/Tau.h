// -*- c++ -*-
#ifndef DataFormat_Tau_h
#define DataFormat_Tau_h

#include "DataFormat/interface/TauGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

class Tau;

class TauCollection: public TauGeneratedCollection, public ParticleIteratorAdaptor<TauCollection> {
public:
  using value_type = Tau;

  TauCollection() {}
  TauCollection(const std::string& prefix): TauGeneratedCollection(prefix) {}
  ~TauCollection() {}

  void setupBranches(BranchManager& mgr);

  Tau operator[](size_t i);
  std::vector<Tau> toVector();

  friend class Tau;
  friend class TauGenerated;
  friend class Particle<TauCollection>;

protected:
};

class Tau: public TauGenerated {
public:
  Tau() {}
  Tau(TauCollection* coll, size_t index): TauGenerated(coll, index) {}
  ~Tau() {}
};

inline
Tau TauCollection::operator[](size_t i) {
  return Tau(this, i);
}

inline
std::vector<Tau> TauCollection::toVector() {
  return ParticleCollection::toVector(*this);
}

#endif
