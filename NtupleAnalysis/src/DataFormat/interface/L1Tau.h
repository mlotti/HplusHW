// -*- c++ -*-
#ifndef DataFormat_L1Tau_h
#define DataFormat_L1Tau_h

#include "DataFormat/interface/L1TauGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

#include <vector>

class L1Tau;

class L1TauCollection: public L1TauGeneratedCollection, public ParticleIteratorAdaptor<L1TauCollection> {
public:
  using value_type = L1Tau;

  L1TauCollection() {}
  explicit L1TauCollection(const std::string& prefix): L1TauGeneratedCollection(prefix) {}
  ~L1TauCollection() {}

  void setupBranches(BranchManager& mgr);

  L1Tau operator[](size_t i) const;
  std::vector<L1Tau> toVector() const;

  friend class L1Tau;
  friend class L1TauGenerated<L1TauCollection>;
  friend class Particle<L1TauCollection>;

protected:

private:

};

class L1Tau: public L1TauGenerated<L1TauCollection> {
public:
  L1Tau() {}
  L1Tau(const L1TauCollection* coll, size_t index): L1TauGenerated(coll, index) {}
  ~L1Tau() {}
  
};

inline
L1Tau L1TauCollection::operator[](size_t i) const {
  return L1Tau(this, i);
}

inline
std::vector<L1Tau> L1TauCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
