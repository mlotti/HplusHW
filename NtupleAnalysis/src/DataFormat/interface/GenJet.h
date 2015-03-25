// -*- c++ -*-
#ifndef DataFormat_GenJet_h
#define DataFormat_GenJet_h

#include "DataFormat/interface/GenJetGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

class GenJet;

class GenJetCollection: public GenJetGeneratedCollection, public ParticleIteratorAdaptor<GenJetCollection> {
public:
  using value_type = GenJet;

  GenJetCollection() {}
  GenJetCollection(const std::string& prefix): GenJetGeneratedCollection(prefix) {}
  ~GenJetCollection() {}

  void setupBranches(BranchManager& mgr);

  GenJet operator[](size_t i) const;
  std::vector<GenJet> toVector() const;

  friend class GenJet;
  friend class GenJetGenerated<GenJetCollection>;
  friend class Particle<GenJetCollection>;

protected:
};

class GenJet: public GenJetGenerated<GenJetCollection> {
public:
  GenJet() {}
  GenJet(const GenJetCollection* coll, size_t index): GenJetGenerated(coll, index) {}
  ~GenJet() {}
};

inline
GenJet GenJetCollection::operator[](size_t i) const {
  return GenJet(this, i);
}

inline
std::vector<GenJet> GenJetCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
