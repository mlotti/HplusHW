#include "DataFormat/interface/Particle.h"
#include "Framework/interface/Exception.h"

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

void ParticleCollectionBase::checkDiscriminatorNameValidity(const std::string& name, const std::vector<std::string>& list) const {
  bool myStatus = false;
  for (const auto& p: list) {
    if (p == name) {
      myStatus = true;
    }
  }
  if (!myStatus) {
    std::string msg = "";
    for (const auto& p: list) {
      if (msg == "")
        msg += "  "+p;
      else
        msg += "\n  "+p;
    }
    throw hplus::Exception("ConfigError") << "Asked for discriminator name '" << name << "' but it does not exist. Available options:\n" << msg;
  }
}

ParticleBase::~ParticleBase() {}


