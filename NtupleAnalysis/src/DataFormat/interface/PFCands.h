// -*- c++ -*-
#ifndef DataFormat_PFCands_h
#define DataFormat_PFCands_h

#include "DataFormat/interface/PFCandsGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

#include <vector>

class PFCands;

class PFCandsCollection: public PFCandsGeneratedCollection, public ParticleIteratorAdaptor<PFCandsCollection> {
public:
  using value_type = PFCands;

  PFCandsCollection() {}
  explicit PFCandsCollection(const std::string& prefix): PFCandsGeneratedCollection(prefix) {}
  ~PFCandsCollection() {}

  void setupBranches(BranchManager& mgr);

  PFCands operator[](size_t i) const;
  std::vector<PFCands> toVector() const;

  friend class PFCands;
  friend class PFCandsGenerated<PFCandsCollection>;
  friend class Particle<PFCandsCollection>;

protected:

private:

};

class PFCands: public PFCandsGenerated<PFCandsCollection> {
public:
  PFCands() {}
  PFCands(const PFCandsCollection* coll, size_t index): PFCandsGenerated(coll, index) {}
  ~PFCands() {}
  
};

inline
PFCands PFCandsCollection::operator[](size_t i) const {
  return PFCands(this, i);
}

inline
std::vector<PFCands> PFCandsCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
