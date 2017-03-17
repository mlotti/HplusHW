// -*- c++ -*-
#ifndef DataFormat_L1IsoTau_h
#define DataFormat_L1IsoTau_h

#include "DataFormat/interface/L1IsoTauGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

#include <vector>

class L1IsoTau;

class L1IsoTauCollection: public L1IsoTauGeneratedCollection, public ParticleIteratorAdaptor<L1IsoTauCollection> {
public:
  using value_type = L1IsoTau;

  L1IsoTauCollection() {}
  explicit L1IsoTauCollection(const std::string& prefix): L1IsoTauGeneratedCollection(prefix) {}
  ~L1IsoTauCollection() {}

  void setupBranches(BranchManager& mgr);

  L1IsoTau operator[](size_t i) const;
  std::vector<L1IsoTau> toVector() const;

  friend class L1IsoTau;
  friend class L1IsoTauGenerated<L1IsoTauCollection>;
  friend class Particle<L1IsoTauCollection>;

protected:

private:

};

class L1IsoTau: public L1IsoTauGenerated<L1IsoTauCollection> {
public:
  L1IsoTau() {}
  L1IsoTau(const L1IsoTauCollection* coll, size_t index): L1IsoTauGenerated(coll, index) {}
  ~L1IsoTau() {}
  
};

inline
L1IsoTau L1IsoTauCollection::operator[](size_t i) const {
  return L1IsoTau(this, i);
}

inline
std::vector<L1IsoTau> L1IsoTauCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
