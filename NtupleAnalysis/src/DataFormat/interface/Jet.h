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

  Jet operator[](size_t i);
  std::vector<Jet> toVector();

  friend class Jet;
  friend class JetGenerated;
  friend class Particle<JetCollection>;

protected:
};

class Jet: public JetGenerated {
public:
  Jet() {}
  Jet(JetCollection* coll, size_t index): JetGenerated(coll, index) {}
  ~Jet() {}
};

inline
Jet JetCollection::operator[](size_t i) {
  return Jet(this, i);
}

inline
std::vector<Jet> JetCollection::toVector() {
  return ParticleCollectionBase::toVector(*this);
}

#endif
