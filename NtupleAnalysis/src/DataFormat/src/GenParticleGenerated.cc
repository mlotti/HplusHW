
// -*- c++ -*-
// This file has been auto-generated with HiggsAnalysis/NtupleAnalysis/scripts/hplusGenerateDataFormats.py

#include "DataFormat/interface/GenParticleGenerated.h"

#include "Framework/interface/BranchManager.h"

void GenParticleGeneratedCollection::setupBranches(BranchManager& mgr) {
  fGenParticles.setupBranches(mgr);


}

const std::vector<Particle<ParticleCollection<double>>> GenParticleGeneratedCollection::getGenParticles() const {
  std::vector<Particle<ParticleCollection<float_type>>> v;
  for (size_t i = 0; i < fGenParticles.size(); ++i)
    v.push_back(Particle<ParticleCollection<float_type>>(&fGenParticles, i));
  return v;
}

