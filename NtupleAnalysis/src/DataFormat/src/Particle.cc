#include "DataFormat/interface/Particle.h"

ParticleCollectionBase::ParticleCollectionBase(const std::string& prefix):
  fPrefix(prefix)
{}
ParticleCollectionBase::~ParticleCollectionBase() {}

void ParticleCollectionBase::setEnergySystematicsVariation(const std::string& scenario) {
  if(scenario.empty())
    fEnergySystematicsVariation = "";
  else
    fEnergySystematicsVariation = "_"+scenario;
}

ParticleBase::~ParticleBase() {}
