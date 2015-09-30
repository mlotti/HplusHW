#include "DataFormat/interface/Electron.h"

#include "Framework/interface/BranchManager.h"

void ElectronCollection::setupBranches(BranchManager& mgr) {
  ElectronGeneratedCollection::setupBranches(mgr);
  if (electronIDDiscriminatorIsValid()) {
    mgr.book(prefix()+"_"+fElectronIDDiscriminatorName, &fElectronIDDiscriminator);
  }
}

void ElectronCollection::setElectronIDDiscriminator(const std::string& name) {
  if (name == "")
    return;
  bValidityOfElectronIDDiscr = true;
  checkDiscriminatorNameValidity(name, this->getIDDiscriminatorNames());
  fElectronIDDiscriminatorName = name;
}

bool ElectronCollection::electronIDDiscriminatorIsValid() const {
  return bValidityOfElectronIDDiscr;
}

void ElectronCollection::initialize() {
  fElectronIDDiscriminatorName = "";
  bValidityOfElectronIDDiscr = false;
}