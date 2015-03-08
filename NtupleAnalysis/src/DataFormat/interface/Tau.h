// -*- c++ -*-
#ifndef DataFormat_Tau_h
#define DataFormat_Tau_h

#include "DataFormat/interface/TauGenerated.h"
#include "DataFormat/interface/ParticleIterator.h"

#include <vector>

class Tau;

class TauCollection: public TauGeneratedCollection, public ParticleIteratorAdaptor<TauCollection> {
public:
  using value_type = Tau;

  TauCollection() {}
  explicit TauCollection(const std::string& prefix): TauGeneratedCollection(prefix) {}
  ~TauCollection() {}

  void setConfigurableDiscriminators(const std::vector<std::string>& names) {
    fConfigurableDiscriminatorNames = names;
  }

  void setupBranches(BranchManager& mgr);

  Tau operator[](size_t i) const;
  std::vector<Tau> toVector() const;

  friend class Tau;
  friend class TauGenerated<TauCollection>;
  friend class Particle<TauCollection>;

protected:
  std::vector<const Branch<std::vector<bool>> *> fConfigurableDiscriminators;

private:
  std::vector<std::string> fConfigurableDiscriminatorNames;
};

class Tau: public TauGenerated<TauCollection> {
public:
  Tau() {}
  Tau(const TauCollection* coll, size_t index): TauGenerated(coll, index) {}
  ~Tau() {}

  bool configurableDiscriminators() const {
    for(auto& disc: fCollection->fConfigurableDiscriminators) {
      if(!disc->value()[index()])
        return false;
    }
    return true;
  }
};

inline
Tau TauCollection::operator[](size_t i) const {
  return Tau(this, i);
}

inline
std::vector<Tau> TauCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}

#endif
