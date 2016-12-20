// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#ifndef DataFormat_GenParticleGenerated_h
#define DataFormat_GenParticleGenerated_h

#include "DataFormat/interface/Particle.h"
#include <vector>

class GenParticleGeneratedCollection {
public:
  using float_type = double;
  explicit GenParticleGeneratedCollection(const std::string& prefix="genParticles")
  : fGenParticles(prefix)
  {

  }
  ~GenParticleGeneratedCollection() {}

  void setupBranches(BranchManager& mgr);

  const std::vector<Particle<ParticleCollection<float_type>>> getGenParticles() const;
protected:
  ParticleCollection<float_type> fGenParticles;


public:


protected:

};

#endif
