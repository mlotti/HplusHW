#include "DataFormat/interface/Muon.h"

#include "Framework/interface/BranchManager.h"

void MuonCollection::setupBranches(BranchManager& mgr) {
  MuonGeneratedCollection::setupBranches(mgr);
  if (muonIDDiscriminatorIsValid()) {
    mgr.book(prefix()+"_"+fMuonIDDiscriminatorName, &fMuonIDDiscriminator);
  }
}

void MuonCollection::setMuonIDDiscriminator(const std::string& name) {
  if (name == "")
    return;
  bValidityOfMuonIDDiscr = true;
  checkDiscriminatorNameValidity(name, this->getIDDiscriminatorNames());
  fMuonIDDiscriminatorName = name;
}

bool MuonCollection::muonIDDiscriminatorIsValid() const {
  return bValidityOfMuonIDDiscr;
}

void MuonCollection::initialize() {
  fMuonIDDiscriminatorName = "";
  bValidityOfMuonIDDiscr = false;
}