// -*- c++ -*-
#ifndef DataFormat_GenParticleGenerated_h
#define DataFormat_GenParticleGenerated_h

#include "DataFormat/interface/Particle.h"

class GenParticleGeneratedCollection: public ParticleCollection<double> {
public:
  explicit GenParticleGeneratedCollection(const std::string& prefix="GenParticles"): ParticleCollection(prefix) {}
  ~GenParticleGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

};


template <typename Coll>
class GenParticleGenerated: public Particle<Coll> {
public:
  GenParticleGenerated() {}
  GenParticleGenerated(const Coll* coll, size_t index): Particle<Coll>(coll, index) {}
  ~GenParticleGenerated() {}

};

#endif
