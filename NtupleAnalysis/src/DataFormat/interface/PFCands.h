// -*- c++ -*-
#ifndef DataFormat_PFCands_h
#define DataFormat_PFCands_h

#include "DataFormat/interface/PFcandidateGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

#include <vector>

class PFCands;

class PFCandsCollection: public PFcandidateGeneratedCollection, public ParticleIteratorAdaptor<PFCandsCollection> {
public:
  using value_type = PFCands;

  PFCandsCollection() {}
  explicit PFCandsCollection(const std::string& prefix): PFcandidateGeneratedCollection(prefix) {}
  ~PFCandsCollection() {}

  void setupBranches(BranchManager& mgr);

  PFCands operator[](size_t i) const;
  std::vector<PFCands> toVector() const;

  friend class PFCands;
  friend class PFcandidateGenerated<PFCandsCollection>;
  friend class Particle<PFCandsCollection>;

protected:

private:

};

class PFCands: public PFcandidateGenerated<PFCandsCollection> {
public:
  PFCands() {}
  PFCands(const PFCandsCollection* coll, size_t index): PFcandidateGenerated(coll, index) {}
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
