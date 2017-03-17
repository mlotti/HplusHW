// -*- c++ -*-
#ifndef DataFormat_L1Jet_h
#define DataFormat_L1Jet_h

#include "DataFormat/interface/L1JetGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

#include <vector>

class L1Jet;

class L1JetCollection: public L1JetGeneratedCollection, public ParticleIteratorAdaptor<L1JetCollection> {
public:
  using value_type = L1Jet;

  L1JetCollection() {}
  explicit L1JetCollection(const std::string& prefix): L1JetGeneratedCollection(prefix) {}
  ~L1JetCollection() {}

  void setupBranches(BranchManager& mgr);

  L1Jet operator[](size_t i) const;
  std::vector<L1Jet> toVector() const;

  friend class L1Jet;
  friend class L1JetGenerated<L1JetCollection>;
  friend class Particle<L1JetCollection>;

protected:

private:

};

class L1Jet: public L1JetGenerated<L1JetCollection> {
public:
  L1Jet() {}
  L1Jet(const L1JetCollection* coll, size_t index): L1JetGenerated(coll, index) {}
  ~L1Jet() {}
  
};

inline
L1Jet L1JetCollection::operator[](size_t i) const {
  return L1Jet(this, i);
}

inline
std::vector<L1Jet> L1JetCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
