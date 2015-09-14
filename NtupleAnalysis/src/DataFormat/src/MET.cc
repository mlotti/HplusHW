#include "DataFormat/interface/MET.h"
#include "Framework/interface/BranchManager.h"


METBase::METBase(const std::string& prefix):
  fPrefix(prefix)
{}
METBase::~METBase() {}

void METBase::setEnergySystematicsVariation(const std::string& scenario) {
  if(scenario.empty())
    fEnergySystematicsVariation = "";
  else
    fEnergySystematicsVariation = ""+scenario;
}

