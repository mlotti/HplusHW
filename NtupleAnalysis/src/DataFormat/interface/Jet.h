// -*- c++ -*-
#ifndef DataFormat_Jet_h
#define DataFormat_Jet_h

#include "DataFormat/interface/JetGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

class Jet;

class JetCollection: public JetGeneratedCollection, public ParticleIteratorAdaptor<JetCollection> {
public:
  using value_type = Jet;

  JetCollection() {}
  JetCollection(const std::string& prefix): JetGeneratedCollection(prefix) {}
  ~JetCollection() {}

  void setupBranches(BranchManager& mgr);

  Jet operator[](size_t i) const;
  std::vector<Jet> toVector() const;

  friend class Jet;
  friend class JetGenerated<JetCollection>;
  friend class Particle<JetCollection>;

protected:
};

class Jet: public JetGenerated<JetCollection> {
public:
  Jet() {}
  Jet(const JetCollection* coll, size_t index): JetGenerated(coll, index) {}
  ~Jet() {}
};

inline
Jet JetCollection::operator[](size_t i) const {
  return Jet(this, i);
}

inline
std::vector<Jet> JetCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
