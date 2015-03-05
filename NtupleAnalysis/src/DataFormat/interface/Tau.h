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

  Tau operator[](size_t i);
  std::vector<Tau> toVector();

  friend class Tau;
  friend class TauGenerated;
  friend class Particle<TauCollection>;

protected:
  std::vector<Branch<std::vector<bool>> *> fConfigurableDiscriminators;

private:
  std::vector<std::string> fConfigurableDiscriminatorNames;
};

class Tau: public TauGenerated {
public:
  Tau() {}
  Tau(TauCollection* coll, size_t index): TauGenerated(coll, index) {}
  ~Tau() {}

  bool configurableDiscriminators() {
    for(auto& disc: static_cast<TauCollection *>(fCollection)->fConfigurableDiscriminators) {
      if(!disc->value()[index()])
        return false;
    }
    return true;
  }
};

inline
Tau TauCollection::operator[](size_t i) {
  return Tau(this, i);
}

inline
std::vector<Tau> TauCollection::toVector() {
  return ParticleCollectionBase::toVector(*this);
}

#endif
