// -*- c++ -*-
#ifndef DataFormat_GenParticle_h
#define DataFormat_GenParticle_h

#include "DataFormat/interface/GenParticleGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

class GenParticle;

class GenParticleCollection: public GenParticleGeneratedCollection, public ParticleIteratorAdaptor<GenParticleCollection> {
public:
  using value_type = GenParticle;

  GenParticleCollection() {}
  GenParticleCollection(const std::string& prefix): GenParticleGeneratedCollection(prefix) {}
  ~GenParticleCollection() {}

  void setupBranches(BranchManager& mgr);

  GenParticle operator[](size_t i) const;
  std::vector<GenParticle> toVector() const;

  friend class GenParticle;
  friend class GenParticleGenerated<GenParticleCollection>;
  friend class Particle<GenParticleCollection>;

protected:
};

class GenParticle: public GenParticleGenerated<GenParticleCollection> {
public:
  GenParticle() {}
  GenParticle(const GenParticleCollection* coll, size_t index): GenParticleGenerated(coll, index) {}
  ~GenParticle() {}
};

inline
GenParticle GenParticleCollection::operator[](size_t i) const {
  return GenParticle(this, i);
}

inline
std::vector<GenParticle> GenParticleCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
