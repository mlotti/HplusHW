// -*- c++ -*-
#ifndef DataFormat_ElectronGenerated_h
#define DataFormat_ElectronGenerated_h

#include "DataFormat/interface/Particle.h"

class ElectronGenerated;

class ElectronGeneratedCollection: public ParticleCollection<double> {
public:
  explicit ElectronGeneratedCollection(const std::string& prefix="Electrons"): ParticleCollection(prefix) {}
  ~ElectronGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  ElectronGenerated operator[](size_t i);

  friend class ElectronGenerated;
  friend class Particle<ElectronGeneratedCollection>;

protected:

};


class ElectronGenerated: public Particle<ElectronGeneratedCollection> {
public:
  ElectronGenerated() {}
  ElectronGenerated(ElectronGeneratedCollection* coll, size_t index): Particle<ElectronGeneratedCollection>(coll, index) {}
  ~ElectronGenerated() {}


};

inline
ElectronGenerated ElectronGeneratedCollection::operator[](size_t i) {
  return ElectronGenerated(this, i);
}

#endif
