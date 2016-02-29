// -*- c++ -*-
#ifndef DataFormat_GenParticle_h
#define DataFormat_GenParticle_h

#include "DataFormat/interface/GenParticleGenerated.h"
//#include "DataFormat/interface/ParticleIterator.h"

class GenParticle;

class GenParticleCollection: public GenParticleGeneratedCollection { //, public ParticleIteratorAdaptor<GenParticleCollection> {
public:
  // using value_type = GenParticle;
  
  GenParticleCollection() {}
  GenParticleCollection(const std::string& prefix): GenParticleGeneratedCollection(prefix) {}
  ~GenParticleCollection() {}

  void setupBranches(BranchManager& mgr);

  //GenParticle operator[](size_t i) const;
  //std::vector<GenParticle> toVector() const;

  //friend class GenParticle;
  //friend class GenParticleGenerated<GenParticleCollection>;
  //friend class Particle<GenParticleCollection>;
};

/*class GenParticle: public GenParticleGenerated<GenParticleCollection> {
public:
 GenParticle() {}
  GenParticle(const GenParticleCollection* coll, size_t index): GenParticleGenerated(coll, index) {}
  ~GenParticle() {}

  short mother() const { return fCollection->fMother->value()[index()]; }
  //short status() const { return fCollection->fStatus->value()[index()]; }
  short tauProng() const { return fCollection->fTauProng->value()[index()]; }
  double tauVisiblePt() const { return fCollection->fTauVisiblePt->value()[index()]; }
  double tauVisiblePhi() const { return fCollection->fTauVisiblePhi->value()[index()]; }
  double tauVisibleEta() const { return fCollection->fTauVisibleEta->value()[index()]; }
  double tauSpinEffectsW() const { return fCollection->fTauSpinEffectsW->value()[index()]; }
  double tauSpinEffectsHpm() const { return fCollection->fTauSpinEffectsHpm->value()[index()]; }
  short associatedWithHpm() const { return fCollection->fAssociatedWithHpm->value()[index()]; }
};

inline
GenParticle GenParticleCollection::operator[](size_t i) const {
  return GenParticle(this, i);
}

inline
std::vector<GenParticle> GenParticleCollection::toVector() const {
  return ParticleCollectionBase::toVector(*this);
}*/

#endif
