// -*- c++ -*-
#ifndef DataFormat_ElectronGenerated_h
#define DataFormat_ElectronGenerated_h

#include "DataFormat/interface/Particle.h"

class ElectronGeneratedCollection: public ParticleCollection<double> {
public:
  explicit ElectronGeneratedCollection(const std::string& prefix="Electrons"): ParticleCollection(prefix) {}
  ~ElectronGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

protected:

};


template <typename Coll>
class ElectronGenerated: public Particle<Coll> {
public:
  ElectronGenerated() {}
  ElectronGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~ElectronGenerated() {}


};

#endif
