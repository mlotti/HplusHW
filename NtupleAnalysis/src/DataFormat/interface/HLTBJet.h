// -*- c++ -*-
#ifndef DataFormat_HLTBJet_h
#define DataFormat_HLTBJet_h

#include "DataFormat/interface/HLTBJetGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

#include <vector>

class HLTBJet;

class HLTBJetCollection: public HLTBJetGeneratedCollection, public ParticleIteratorAdaptor<HLTBJetCollection> {
public:
  using value_type = HLTBJet;

  HLTBJetCollection() {}
  explicit HLTBJetCollection(const std::string& prefix): HLTBJetGeneratedCollection(prefix) {}
  ~HLTBJetCollection() {}

  void setupBranches(BranchManager& mgr);

  HLTBJet operator[](size_t i) const;
  std::vector<HLTBJet> toVector() const;

  friend class HLTBJet;
  friend class HLTBJetGenerated<HLTBJetCollection>;
  friend class Particle<HLTBJetCollection>;

protected:

private:

};

class HLTBJet: public HLTBJetGenerated<HLTBJetCollection> {
public:
  HLTBJet() {}
  HLTBJet(const HLTBJetCollection* coll, size_t index): HLTBJetGenerated(coll, index) {}
  ~HLTBJet() {}
  
};

inline
HLTBJet HLTBJetCollection::operator[](size_t i) const {
  return HLTBJet(this, i);
}

inline
std::vector<HLTBJet> HLTBJetCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
