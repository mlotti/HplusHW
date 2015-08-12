// -*- c++ -*-
#ifndef DataFormat_HLTTau_h
#define DataFormat_HLTTau_h

#include "DataFormat/interface/HLTTauGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

#include <vector>

class HLTTau;

class HLTTauCollection: public HLTTauGeneratedCollection, public ParticleIteratorAdaptor<HLTTauCollection> {
public:
  using value_type = HLTTau;

  HLTTauCollection() {}
  explicit HLTTauCollection(const std::string& prefix): HLTTauGeneratedCollection(prefix) {}
  ~HLTTauCollection() {}

  void setupBranches(BranchManager& mgr);

  HLTTau operator[](size_t i) const;
  std::vector<HLTTau> toVector() const;

  friend class HLTTau;
  friend class HLTTauGenerated<HLTTauCollection>;
  friend class Particle<HLTTauCollection>;

protected:

private:

};

class HLTTau: public HLTTauGenerated<HLTTauCollection> {
public:
  HLTTau() {}
  HLTTau(const HLTTauCollection* coll, size_t index): HLTTauGenerated(coll, index) {}
  ~HLTTau() {}
  
};

inline
HLTTau HLTTauCollection::operator[](size_t i) const {
  return HLTTau(this, i);
}

inline
std::vector<HLTTau> HLTTauCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
